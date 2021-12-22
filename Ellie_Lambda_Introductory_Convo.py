### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests

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


def validate_data(birthdate, term, intent_request):
    
    birthdate = get_slots(intent_request)["birthdate"]
    term = get_slots(intent_request)["term"]
    """
    Validates the data provided by the user.
    """

    # Validate that the user is over 18 years old
    if birthdate is not None:
        birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
        age = relativedelta(datetime.now(), birth_date).years
        if age < 18:
            return build_validation_result(
                False,
                "birthdate",
                "You should be at least 18 years old to use this service, "
                "please provide a different date of birth.",
            )
    
    #Validate term length (short or long)
    if term is not None:
        if term.lower() not in {"short", "long"}:
            return build_validation_result(
                False,
                "term",
                "I don't understand. Please enter short or long."
            )
    return build_validation_result(True, True, None)
    
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

def ellie_conversation(intent_request):
    """
    Performs dialog management and fulfillment for converting from dollars to bitcoin.
    """
    # Gets slots' values
    birthdate = get_slots(intent_request)["birthdate"]
    term_length = get_slots(intent_request)["term"]
    risk_level = get_slots(intent_request)["risk"]
    term_len_num = 0  
   

    # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(birthdate, term_length, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))


    if term_length is not None: 
        if term_length.lower() == "short":
            term_len_num = 10
        elif term_length.lower() == "long":
            term_len_num = 20 
    
    if risk_level is not None: 
        if risk_level.lower() == "none":
            risk_lev_num = 1
        elif risk_level.lower() == "low":
            risk_lev_num = 2
        elif risk_level.lower() == "medium":
            risk_lev_num = 3
        elif risk_level.lower() =="high":
            risk_lev_num = 4
            
    allocation = term_len_num + risk_lev_num 
    
    if allocation in {11, 12, 21, 22}:
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content" : "Your ideal portfolio should be 40% stocks and 60% bonds. Which would you like to explore first?"
                
            })
    elif allocation in {13, 14, 23, 24}: 
     
        return close(
            intent_request["sessionAttributes"],
            "Fulfilled",
            {
                "contentType": "PlainText",
                "content": "Your ideal portfolio should be 80% stocks and 20% bonds. Which would you like to explore first?"
            })
            

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "EllieIntro":
        return ellie_conversation(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
