import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="divide")
def divide(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked divide Skill.')
    try:
        body = json.dumps(req.get_json())

        if body:
            logging.info(body)
            values = json.loads(body)['values']
            new_values = []
            for value in values:
                logging.info(value)
                input_value = value['data']['function_name_input']
                new_values.append({
                    "recordId": value['recordId'],
                    "data": {"function_name_new_list": [
                        {
                            "item": input_value+"_new_1"
                        },
                        {
                            "item": input_value+"_new_2"
                        },
                        {
                            "item": input_value+"_new_3"
                        },
                        {
                            "item": input_value+"_new_4"
                        }
                        ]},
                    "errors": None,
                    "warnings": None
                })
            output = {}   
            output["values"] = new_values
            result = json.dumps(output, ensure_ascii=False)
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
        
@app.route(route="onetoone")
def onetoone(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked onetoone Skill.')
    try:
        body = json.dumps(req.get_json())

        if body:
            logging.info(body)
            values = json.loads(body)['values']
            new_values = []
            for value in values:
                logging.info(value)
                input_value = value['data']['function_name_input']
                new_values.append({
                    "recordId": value['recordId'],
                    "data": {"function_name_new_field": input_value+"_new"},
                    "errors": None,
                    "warnings": [{"message": "some warning message"}]
                })
            output = {}   
            output["values"] = new_values
            result = json.dumps(output, ensure_ascii=False)
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
        
        
@app.route(route="mergepairs")
def mergepairs(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoked mergepairs Skill.')
    try:
        body = json.dumps(req.get_json())

        if body:
            logging.info(body)
            values = json.loads(body)['values']
            new_values = []
            for value in values:
                logging.info(value)
                input_value = value['data']['input']
                new_values.append({
                    "recordId": value['recordId'],
                    "data": {"merged_list": [
                        input_value+"_new_1",
                        input_value+"_new_2",
                        input_value+"_new_3",
                        input_value+"_new_4"]},
                    "errors": None,
                    "warnings": None
                })
            output = {}   
            output["values"] = new_values
            result = json.dumps(output, ensure_ascii=False)
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