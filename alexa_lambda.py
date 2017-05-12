import planner
import json


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, card_output, output, reprompt_text, should_end_session, photo=None):
    if reprompt_text:
        reprompt_text = "<speak>" + reprompt_text + "</speak>"
    response = {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + output + "</speak>"
        },
        'card': {
            'type': 'Standard',
            'title': title,
            'text': card_output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    # if photo:
    #   response['card']['image'] = photo
    print(response)
    return response


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome to Trip Planner"
    speech_output = "Welcome to the Trip Planner. " \
                    "Please ask me to plan your trip to a city by saying, " \
                    "Plan me a trip to Los Angeles"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the city you plan to visit by saying, " \
                    "Plan me a trip to Seattle"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "See your later"
    speech_output = "Thank you for trying Trip Planner. Good luck on that trip!\n" \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, speech_output, None, should_end_session))


def create_current_city_attributes(attributes, city):
    attributes["currentCity"] = city
    return attributes


def create_duration_attributes(attributes, duration):
    attributes["currentDuration"] = duration
    return attributes


# def get_color_from_session(intent, session):
#   session_attributes = {}
#   reprompt_text = None

#   if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
#       favorite_color = session['attributes']['favoriteColor']
#       speech_output = "Your favorite color is " + favorite_color + \
#                       ". Goodbye."
#       should_end_session = True
#   else:
#       speech_output = "I'm not sure what your favorite color is. " \
#                       "You can say, my favorite color is red."
#       should_end_session = False

#   # Setting reprompt_text to None signifies that we do not want to reprompt
#   # the user. If the user does not respond or says something that is not
#   # understood, the session will end.
#   return build_response(session_attributes, build_speechlet_response(
#       intent['name'], speech_output, reprompt_text, should_end_session))

def get_trip_from_session(intent, session):
    should_end_session = False
    session_attributes = {}
    if session.get('attributes', {}):
        session_attributes = {}

    city = None
    duration = None

    if 'city' in intent['slots'] and 'value' in intent['slots']['city']:
        city = intent['slots']['city']['value']
        session_attributes = create_current_city_attributes(session_attributes, city)
    elif 'city' in session_attributes:
        city = session_attributes['city']

    if 'Time' in intent['slots'] and 'value' in intent['slots']['Time']:
        duration = intent['slots']['Time']['value']
        session_attributes = create_duration_attributes(session_attributes, duration)
    elif 'currentDuration' in session_attributes:
        duration = session_attributes['currentDuration']


    if not city:
        speech_output = "I'm not sure what city you referred to. " \
                        "Please try again."
        reprompt_text = "Can you please tell me which city you are planning visit?"
        card_title = "Which City?"
        card_response = "Please tell me which city you are planning to visit"
    elif not duration:
        print("City", city)
        speech_output = "How many hours do you want to tour " + city + "?"
        reprompt_text = "How many hours do you want the trip to last?"
        card_title = "How long?"
        card_response = "How many hours do you want to spend in " + city + "?"
    else:
        print("Duration", duration)
        try:
            (speech_output, card_response, photo) = planner.get_route_sequence(city, duration)
            reprompt_text = None
            card_title = duration + "hr trip in " + city
            should_end_session = True
        except Exception as e:
            speech_output = "I'm not sure what city you referred to. " \
                            "Please try again."
            reprompt_text = "Can you please tell me which city you are planning visit?"
            card_title = "Which City?"
            card_response = "Please tell me which city you are planning to visit?"


    return build_response(session_attributes, build_speechlet_response(
        card_title, card_response, speech_output, reprompt_text, should_end_session, photo=None))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "FullDayTripIntent":
        return get_trip_from_session(intent, session)
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.663404a2-321c-45c3-8365-9e260b16bcf4"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
