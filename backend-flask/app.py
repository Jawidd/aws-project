from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.notifications_activities import *


# Importing libraries for logging and tracing
#   Using Rollbar for error logging
#   Using Honeycomb for tracing
#   Using AWS X-Ray for tracing
# Importing libraries for AWS X-Ray
from aws_xray_sdk.core import xray_recorder 
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
# Importing libraries for Honeycomb
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# OpenTelemetry + Honeycomb configuration
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
# importing libraries for rollbar
import os
import rollbar
import rollbar.contrib.flask


#importing libraries for Cognito JWT token verification
from lib.cognito_jwt_token import token_required
#importing libraries for Cognito JWT token verification
from lib.cognito_jwt_token import token_required, CognitoJwtToken



app = Flask(__name__)


#Logging and Tracing configuration
#   X-Ray- Configure X-Ray with Flask
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='cruddur-backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
#   Honeycomb- Initialize autmomatic instrumentation with Flask and Requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
#   Rollbar configuration
from flask import got_request_exception
with app.app_context():
    """init rollbar module"""
    rollbar.init(
        # access token
        os.getenv('ROLLBAR_ACCESS_TOKEN'),
        # environment name - any string, like 'production' or 'development'
        'flasktest',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)
    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
#Rollbar test route for DEBUGGING!!
@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!(TESTING ROLLBAR)','warning')
    return 'Hello World (TESTING ROLLBAR)'


#CORS configuration
frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since,authorization",
  methods="OPTIONS,GET,HEAD,POST"
)




@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbroenn'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200


@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return




@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET'])
@cross_origin()
def data_home():
    claims = None
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        try:
            token = auth_header.split(' ')[1]
            cognito_jwt_token = CognitoJwtToken(
                user_pool_id=os.getenv('REACT_APP_USER_POOL_ID'),
                user_pool_client_id=os.getenv('REACT_APP_USER_POOL_CLIENT_ID'),
                region=os.getenv('REACT_APP_AWS_REGION')
            )
            if cognito_jwt_token.verify(token):
                claims = cognito_jwt_token.claims
        except:
            pass  # Ignore auth errors, proceed as unauthenticated
    
    data = HomeActivities.run(user_claims=claims)
    return data, 200





@app.route("/api/activities/notifications", methods=['GET'])
@xray_recorder.capture('notifications_activities')
def data_notifications():
  user_handle = 'andrewbrown'
  notifications_service = NotificationsActivities(request)
  model = notifications_service.run(user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200


@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  claims = None
  auth_header = request.headers.get('Authorization')
  
  if auth_header:
    try:
      token = auth_header.split(' ')[1]
      cognito_jwt_token = CognitoJwtToken(
        user_pool_id=os.getenv('REACT_APP_USER_POOL_ID'),
        user_pool_client_id=os.getenv('REACT_APP_USER_POOL_CLIENT_ID'),
        region=os.getenv('REACT_APP_AWS_REGION')
      )
      if cognito_jwt_token.verify(token):
        claims = cognito_jwt_token.claims
    except:
      pass  # Ignore auth errors, let service handle unauthenticated state
  
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, ttl, claims)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200


  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

#
@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  claims = None
  auth_header = request.headers.get('Authorization')
  
  if auth_header:
    try:
      token = auth_header.split(' ')[1]
      cognito_jwt_token = CognitoJwtToken(
        user_pool_id=os.getenv('REACT_APP_USER_POOL_ID'),
        user_pool_client_id=os.getenv('REACT_APP_USER_POOL_CLIENT_ID'),
        region=os.getenv('REACT_APP_AWS_REGION')
      )
      if cognito_jwt_token.verify(token):
        claims = cognito_jwt_token.claims
    except:
      pass
  
  message = request.json['message']
  model = CreateReply.run(message, claims, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

#

if __name__ == "__main__":
  app.run(debug=True)