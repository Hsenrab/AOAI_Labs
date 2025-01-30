import azure.functions as func
import logging
import json
import os
import datetime
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="extracttomarkdown")
def extracttomarkdown(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked FormRecognizer Skill.')
    try:
        body = json.dumps(req.get_json())

        if body:
            logging.info(body)
            result = compose_response(body)
            logging.info("Result to return to custom skill: " + result)
            return func.HttpResponse(result, mimetype="application/json")
        else:
            return func.HttpResponse(
                "Invalid body",
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )

def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    endpoint = os.environ["OPENAI_API_ENDPOINT"]
    key = os.environ["OPENAI_API_KEY"]
    
    for value in values:
        images = pdf2images(value)
        markdown_output = generate_markdown(images)
        results["values"].append(markdown_output)

    return json.dumps(results, ensure_ascii=False, cls=DateTimeEncoder)
    
def pdf2images(file):
    return ""


def generate_markdown(images):
    markdown = """
# Example Markdown

## Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
| Value 7  | Value 8  | Value 9  |
"""
    return markdown


class DateTimeEncoder(json.JSONEncoder):
    #Override the default method    
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()