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
    users,
    update_profile,
    user_short,
    like_activity,
    trending_activities,
    avatar_webhook
)

# JWT
from lib.cognito_jwt_token import require_jwt, CognitoJwtToken, extract_access_token, TokenVerifyError

# Initialize JWT token handler
cognito_jwt_token = CognitoJwtToken(
    user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"), 
    user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
    region=os.getenv("AWS_DEFAULT_REGION")
)

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

# CORS configuration
default_origins = [
    "http://localhost:3000",
    "https://localhost:3000"
]

# Allow prod domains when provided through env (ECS sets FRONTEND_URL/BACKEND_URL)
env_origins = [
    os.getenv("FRONTEND_URL"),
    os.getenv("BACKEND_URL")
]

allowed_origins = [origin for origin in default_origins + env_origins if origin]

CORS(
    app,
    origins=allowed_origins,
    expose_headers="location,link",
    allow_headers=["content-type", "if-modified-since", "authorization"],
    methods=["OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE"],
    supports_credentials=True
)

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

@app.route("/api/health-check")
def health_check():
    return {"success-from app.py V3.1 health-check route": True}, 200

@app.route("/api/activities/trending", methods=['GET'])
def data_trending():
    return trending_activities.TrendingActivities.run(), 200


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
        endpoint_url=os.getenv("DYNAMODB_URL")
    )
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

@app.route("/api/users/without_conversations", methods=['GET'])
@cross_origin()
@require_jwt()
def data_users_without_conversations(claims):
    user = users.UsersService.get_user_by_cognito_id(claims['username'])
    if not user:
        return {"error": f"User {claims['username']} not found"}, 404
    
    # Get existing conversation participants
    existing_uuids = message_groups.MessageGroups.get_conversation_participants(
        user['uuid'], 
        endpoint_url=os.getenv("DYNAMODB_URL")
    )
    
    users_list = users.UsersService.get_users_without_conversations(
        user['uuid'], 
        existing_uuids
    )
    return users_list, 200


@app.route("/api/messages/user/<string:uuid>", methods=['GET'])
@cross_origin()
@require_jwt()
def data_messages(claims, uuid):
    """Fetch messages for the logged-in user with a specific receiver."""
    app.logger.info(f"Fetching messages for {uuid}")
    
    # Convert handle to UUID
    receiver_user = users.UsersService.get_user_by_uuid(uuid)
    if not receiver_user:
        return {"error": f"User {uuid} not found"}, 404
    
    model = messages.Messages.run(
        user_sender_cognito_id=claims['username'],
        user_receiver_uuid=receiver_user['uuid'],
        endpoint_url=os.getenv("DYNAMODB_URL")
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

    # CHANGED: use the new field
    receiver_uuid = data.get("user_receiver_uuid")

    receiver_user = users.UsersService.get_user_by_uuid(receiver_uuid)
    
    model = create_message.CreateMessage.run(
        message=data.get("message"),
        sender_user=sender_user,
        receiver_user=receiver_user,
        endpoint_url=os.getenv("DYNAMODB_URL")
    ) 

    return (
        {"errors": model["errors"]}, 422
    ) if model.get("errors") else (
        model["data"], 200
    )



@app.route("/api/activities/home", methods=['GET'])
@cross_origin()
@require_jwt(optional=True)
def data_home(claims):
    return home_activities.HomeActivities.run(user_claims=claims), 200

# @xray_recorder.capture('notifications_activities')
@app.route("/api/activities/notifications", methods=['GET'])
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
@require_jwt(optional=True)
def data_show_activity(claims, activity_uuid):
    return show_activity.ShowActivity.run(activity_uuid=activity_uuid, user_claims=claims), 200

@app.route("/api/activities/@<string:handle>/status/<string:activity_uuid>", methods=['GET'])
@require_jwt(optional=True)
def data_show_activity_by_handle(claims, handle, activity_uuid):
    return show_activity.ShowActivity.run(activity_uuid=activity_uuid, user_claims=claims), 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
@require_jwt()
def data_activities_reply(claims, activity_uuid):
    model = create_reply.CreateReply.run(request.json['message'], claims, activity_uuid)
    return (model['errors'], 422) if model['errors'] else (model['data'], 200)

@app.route("/api/activities/<string:activity_uuid>/like", methods=['POST','OPTIONS'])
@cross_origin()
@require_jwt()
def data_activities_like(claims, activity_uuid):
    try:
        model = like_activity.LikeActivity.run(activity_uuid, claims)
        if model.get('errors'):
            return {"errors": model['errors']}, 422
        return model, 200
    except Exception as e:
        app.logger.error(f"Error in like endpoint: {str(e)}")
        return {"errors": [str(e)]}, 500

@app.route("/api/users/@<string:handle>/short", methods=['GET'])
def data_users_short(handle):
  app.logger.info(f"Getting user short data for handle: {handle}")
  data = user_short.UserShort.run(handle)
  app.logger.info(f"User short data result: {data}")
  return data, 200

@app.route("/api/profile/me", methods=['GET'])
@cross_origin()
@require_jwt()
def data_profile_me(claims):
  from lib.db import db
  try:
    sql = """
    SELECT uuid, handle, full_name as display_name, bio, created_at, avatar_url, cognito_user_id
    FROM public.users 
    WHERE cognito_user_id = %(cognito_user_id)s
    """
    
    with db.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql, {'cognito_user_id': claims['sub']})
        result = cur.fetchone()
        
        if result:
          return {
            'uuid': str(result[0]),
            'handle': result[1],
            'display_name': result[2],
            'bio': result[3] or '',
            'created_at': str(result[4]),
            'avatar_url': result[5],
            'cognito_user_id': result[6]
          }, 200
        else:
          return {'error': 'User not found'}, 404
          
  except Exception as e:
    app.logger.error(f"Error getting profile: {str(e)}")
    return {'error': str(e)}, 500

@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  
  app.logger.info(f"Profile update request: bio='{bio}', display_name='{display_name}'")
  
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    app.logger.info(f"Updating profile for user: {cognito_user_id}")
    
    model = update_profile.UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    
    app.logger.info(f"Update result: {model}")
    
    if model['errors'] is not None:
      app.logger.error(f"Profile update errors: {model['errors']}")
      return {"errors": model['errors']}, 422
    else:
      app.logger.info(f"Profile updated successfully: {model['data']}")
      return model['data'], 200
  except TokenVerifyError as e:
    app.logger.debug(e)
    return {"error": "Unauthorized"}, 401
  except Exception as e:
    app.logger.error(f"Profile update exception: {str(e)}")
    return {"error": str(e)}, 500

@app.route("/api/webhooks/avatar", methods=['POST'])
def handle_avatar_webhook():
  data = request.json or {}
  thumbnail_key = data.get("thumbnail")
  if not thumbnail_key:
    return {"error": "thumbnail_missing"}, 400

  cognito_user_id = avatar_webhook.extract_cognito_user_id(thumbnail_key)
  if not cognito_user_id:
    return {"error": "invalid_thumbnail_key"}, 400

  avatar_url = avatar_webhook.build_public_url(thumbnail_key)
  result = avatar_webhook.AvatarWebhook.update_avatar(cognito_user_id, avatar_url)

  if result['errors']:
    return {"errors": result['errors']}, 422

  return {
    "avatar_url": avatar_url,
    "user": result['data']
  }, 200

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app.run()
