from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os

# Services
from services import (
    home_activities,
    user_activities,
    create_activity,
    create_reply,
    search_activities,
    message_groups,
    messages,
    create_message,
    show_activity,
    notifications_activities,
    users
)

# JWT
from lib.cognito_jwt_token import require_jwt

# # Logging and tracing
# from aws_xray_sdk.core import xray_recorder 
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
# from opentelemetry import trace
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor

# # Rollbar
# import rollbar
# import rollbar.contrib.flask
# from flask import got_request_exception

app = Flask(__name__)

# -------------------------------
# Tracing and Monitoring
# -------------------------------
# # X-Ray
# xray_recorder.configure(service='cruddur-backend-flask', dynamic_naming=os.getenv("AWS_XRAY_URL"))
# XRayMiddleware(app, xray_recorder)

# # Honeycomb / OpenTelemetry
# provider = TracerProvider()
# provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
# trace.set_tracer_provider(provider)
# FlaskInstrumentor().instrument_app(app)
# RequestsInstrumentor().instrument()

# Rollbar
# with app.app_context():
#     rollbar.init(
#         os.getenv('ROLLBAR_ACCESS_TOKEN'),
#         'flasktest',
#         root=os.path.dirname(os.path.realpath(__file__)),
#         allow_logging_basic_config=False
#     )
#     got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

# CORS
CORS(app, resources={r"/api/*": {"origins": [os.getenv('FRONTEND_URL'), os.getenv('BACKEND_URL')]}},
     expose_headers="location,link",
     allow_headers="content-type,if-modified-since,authorization",
     methods="OPTIONS,GET,HEAD,POST",
     supports_credentials=True)

# -------------------------------
# Rollbar Test
# -------------------------------
# @app.route('/rollbar/test')
# def rollbar_test():
#     rollbar.report_message('Hello World!(TESTING ROLLBAR)','warning')
#     return 'Hello World (TESTING ROLLBAR)'

# -------------------------------
# API Routes
# -------------------------------


@app.route("/api/message_groups", methods=['GET'])
@cross_origin()
@require_jwt()
def data_message_groups(claims):
    user = users.UsersService.get_user_by_cognito_id(claims['username'])
    if not user:
        return {"error": f"User {claims['username']} not found"}, 404
    
    model = message_groups.MessageGroups.run(
        user_uuid=user['uuid'], 
        user_full_name=user['full_name'] or user['preferred_username'] or user['handle'],
        endpoint_url=os.getenv("DYNAMODB_LOCAL_DOCKER_URL")
    )
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)



@app.route("/api/messages/@<string:receiver_handle>", methods=['GET'])
@cross_origin()
@require_jwt()
def data_messages(claims, receiver_handle):
    """Fetch messages for the logged-in user with a specific receiver."""
    
    # Convert handle to UUID
    receiver_user = users.UsersService.get_user_by_handle(receiver_handle)
    if not receiver_user:
        return {"error": f"User {receiver_handle} not found"}, 404
    
    model = messages.Messages.run(
        user_sender_cognito_id=claims['username'],
        user_receiver_uuid=receiver_user['uuid'],
        endpoint_url=os.getenv("DYNAMODB_LOCAL_DOCKER_URL")
    )

    if model.get('errors'):
        return {"errors": model['errors']}, 422

    return model.get('data', []), 200




@app.route("/api/messages", methods=['POST', 'OPTIONS'])
@cross_origin()
@require_jwt()
def data_create_message(claims):
    """Create a new message from sender to receiver."""
    data = request.json or {}
    
    sender_user = users.UsersService.get_user_by_cognito_id(claims['username'])
    receiver_user = users.UsersService.get_user_by_uuid(data.get("user_receiver_handle"))
    
    model = create_message.CreateMessage.run(
        message=data.get("message"),
        sender_user=sender_user,
        receiver_user=receiver_user,
        endpoint_url=os.getenv("DYNAMODB_LOCAL_DOCKER_URL")
    ) 
    return ({"errors": model["errors"]}, 422) if model.get("errors") else (model["data"], 200)



@app.route("/api/activities/home", methods=['GET'])
@cross_origin()
@require_jwt(optional=True)
def data_home(claims):
    return home_activities.HomeActivities.run(user_claims=claims), 200

@app.route("/api/activities/notifications", methods=['GET'])
@xray_recorder.capture('notifications_activities')
@require_jwt()
def data_notifications(claims):
    model = notifications_activities.NotificationsActivities(request).run(claims['username'])
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
    model = user_activities.UserActivities.run(handle)
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

@app.route("/api/activities/search", methods=['GET'])
def data_search():
    model = search_activities.SearchActivities.run(request.args.get('term'))
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
@require_jwt()
def data_activities(claims):
    data = request.json
    model = create_activity.CreateActivity.run(data['message'], data['ttl'], claims)
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
    return show_activity.ShowActivity.run(activity_uuid=activity_uuid), 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
@require_jwt()
def data_activities_reply(claims, activity_uuid):
    model = create_reply.CreateReply.run(request.json['message'], claims, activity_uuid)
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
