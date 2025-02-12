import azure.functions as func
import logging
import json
import os
import datetime
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas, BlobClient
from openai import AzureOpenAI
import fitz
import urllib.parse


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="imagetomarkdown")
def imagetomarkdown(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked GPT4o Skill.')
    try:
        body = json.dumps(req.get_json())

        if body:
            logging.info(body)
            result = image_to_markdown_compose_response(body)
            logging.info("Result to return to custom skill: " + result)
            return func.HttpResponse(result, mimetype="application/json")
        else:
            return func.HttpResponse(
                "Invalid body",
                status_code=400
            )
    except ValueError as e:
        return func.HttpResponse(
             "Invalid body: " + str(e),
             status_code=400
        )
        
@app.route(route="pdftoimage")
def pdftoimage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked PDF to Images Skill.')
    try:
        body = json.dumps(req.get_json())

        if body:
            logging.info(body)
            result = pdf_to_image_compose_response(body)
            logging.info("Result to return to custom skill: " + result)
            return func.HttpResponse(result, mimetype="application/json")
        else:
            return func.HttpResponse(
                "Invalid body",
                status_code=400
            )
    except ValueError as e:
        return func.HttpResponse(
             "Invalid body: " + str(e),
             status_code=400
        )
        
def pdftoimages(record_id, pdf_url, blob_connection_string):
    
    # Create a BlobClient using the URL
    blob_client = BlobClient.from_blob_url(pdf_url)
    pdf_bytes = blob_client.download_blob().readall()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    image_sas_urls = []

    for page_num in range(len(pdf_document)):
        logging.info("Next Page")
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        
        parsed_url = urllib.parse.urlparse(pdf_url)
        pdf_name = os.path.basename(parsed_url.path).replace(".pdf", "")

        
        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_client = blob_service_client.get_container_client("customskillimages")
        
        if not container_client.exists():
            container_client.create_container()
            
        
        blob_client = container_client.get_blob_client(blob=f'{pdf_name}/page{page_num}.jpg')
        image_bytes = pix.tobytes("jpg")
        blob_client.upload_blob(image_bytes, overwrite=True)
        
        account_key = get_account_key_from_connection_string(blob_connection_string)
        sas_token = generate_blob_sas(
            account_key=account_key,
            account_name=blob_service_client.account_name,
            container_name=container_client.container_name,
            blob_name=blob_client.blob_name,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30))
        
        image_sas_urls.append({"sas_url": f"{blob_client.url}?{sas_token}"})
        
    image_record = {
        "recordId": record_id,
        "data": {
            "image_sas_urls": image_sas_urls
            }   
        }
        
    return image_record


def pdf_to_image_compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    blob_connection_string = os.environ["BLOB_STORAGE_ACCOUNT_CONNECTION_STRING"]
    
    for value in values:
        try:
            logging.info("Next Doc")
            url = value["data"]["docUrl"]+value["data"]["docSAS"]
            logging.info("url")
            image_sas_urls = pdftoimages(value["recordId"], url, blob_connection_string)  
        except ValueError as error:
            image_sas_urls = {
                "recordId": value["recordId"],
                "errors": [ { "message": "Error:" + str(error) }   ]       
            }     
        results["values"].append(image_sas_urls)

    return json.dumps(results, ensure_ascii=False, cls=DateTimeEncoder)


def image_to_markdown_compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        try:
            logging.info("Next Doc")
            url = value["data"]["image_sas_url"]
            logging.info("url")
            chunks = image_to_markdown(value["recordId"], url)  
        except NameError as error:
            chunks = {
                "recordId": value["recordId"],
                "errors": [ { "message": "Error:" + str(error) }   ]       
            }     
        results["values"].append(chunks)

    return json.dumps(results, ensure_ascii=False, cls=DateTimeEncoder)


    
def image_to_markdown(recordId, url):
    
    # Extract Markdown for the page.
    markdown = generate_markdown(url)
        
    # Ensure the markdown starts with "Page " followed by a number
    if not markdown.startswith("Page ") or not markdown.split('\n')[0].replace("Page ", "").strip().isdigit():
        raise ValueError("Markdown does not start with 'Page ' followed by a number")
        
    page_number = markdown.split('\n')[0].replace("Page ", "").strip()
           
    chunk_record = {
        "recordId": recordId,
        "data": {
            "page_number": page_number,
            "markdown": markdown
        }
    }
    
    return chunk_record

# Function to extract account key from connection string
def get_account_key_from_connection_string(connection_string):
    parts = connection_string.split(';')
    for part in parts:
        if part.startswith('AccountKey='):
            return part[len('AccountKey='):]
    return None

def generate_markdown(image_url):
    """
    Gpt-4o model
    """
    
    system_prompt = """
    You are an AI assistance that extracts text from the image. You are especially good at extracting tables.
    Start your response with the page number of the image. 
    Example Page:
    
    Page 123
    
    Monthly Savings
    | Month    | Savings |Details      |
    | -------- | ------- |------------ |
    | January  | $250    | for holiday |
    | February | $80     | pension     |
    | March    | $420    | new cat     |
    
    Savings were significantly lower in February. This is surprising because it is a short month and contributing to pension shuld be a priority.
    """
    
    client = AzureOpenAI(
        azure_endpoint=os.environ['OPENAI_API_ENDPOINT'],
        api_key=os.environ['OPENAI_API_KEY'],
        api_version='2023-05-15',
        )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from the image"},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ],
        max_tokens=2000,
        temperature=0.0,
    )
    
    return response.choices[0].message.content


class DateTimeEncoder(json.JSONEncoder):
    #Override the default method    
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        
        