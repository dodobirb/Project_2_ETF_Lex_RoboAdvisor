### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests
###Required libraries to connect to S3 bucket and read json files
import boto3
import json
import uuid

### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Defines an internal validation message structured as a python dictionary.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


def validate_data(variable1, variable2, variable3, intent_request):
    """
    Validates the data provided by the user.
    """

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def sector_selector(intent_request):
    """
    Performs dialog management and fulfillment for converting from dollars to bitcoin.
    """

    # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))
    
    sector = get_slots(intent_request)["sector"]


    ticker_dict = {"communications": "XLC", "consumer discretionary":"XLY","consumer staples":"XLP",
                        "energy":"XLE", "financial":"XLF", "healthcare": "XLV", "industrials":"XLI", 
                        "materials": "XLB", "real estate":"XLRE", "technology":"XLK", "utilities": "XLU"}
                        
                        
    #BM added code to provide return performance or other indicators we include in the returns.json file
    
    s3 = boto3.client('s3')
    bucket = 'elliejson'
    key = 'returns.json'
    response = s3.get_object(Bucket=bucket,Key=key)

    content = response['Body']

    jsonObject = json.loads(content.read())
    
    for sectors, ticker in ticker_dict.items():
        if sector is not None: 
            if sector.lower() in sectors: 
                sector_name = sector   
                ticker_name = ticker
                
                #BM added to get risk/returns data for the selected sector, ticker. Data loaded from S3 bucket, and source is Jupyter notebook in GitHub Repo
                long_name = str(jsonObject[ticker]["Name"])
                returns_trunc = str(round(jsonObject[ticker]["% Change"],2)) 
                Annualized_StDev_trunc = str(round(jsonObject[ticker]["Annualized_StDev"],2))
                Annualized_Sharpe_Ratio_trunc = str(round(jsonObject[ticker]["Annualized_Sharpe_Ratio"],4))
                Annualized_AvgReturns_trunc = str(round(jsonObject[ticker]["Annualized_AvgReturns"],2))
    
    #record each ETF request to see how often consumer or technology are selected and store in ETF_Request DynamoDB table
    dyn_client = boto3.client('dynamodb')
    TABLE_NAME = 'ETF_Request_2'
    if sector_name.lower() == "consumer":
        id = "1_"+str(uuid.uuid4())
    elif sector_name.lower() == "technology":
        id = "2_"+str(uuid.uuid4())
    else:
        id = "3_"+str(uuid.uuid4())
    
    data = dyn_client.put_item(
        TableName = TABLE_NAME,
        Item={'id': {'S': id }, 'sector':{'S':sector_name}})
                
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Our most popular ETF in the {} sector is {} ({}). The historical risk/return performance was as follows: 10-year return: 
                {}%, annualized risk: {}, Sharp ratio: {}, and annualized average return: {}%. Would you like to see some predictions using this ETF?""".format(sector_name, ticker_name, long_name, 
                returns_trunc, Annualized_StDev_trunc,Annualized_Sharpe_Ratio_trunc, Annualized_AvgReturns_trunc), 
        })

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "EllieETFs":
        return sector_selector(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
