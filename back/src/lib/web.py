from flask import Flask, jsonify, request  # type: ignore
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    verify_jwt_in_request,
    get_jwt_identity,
)

import jsonpickle  # type: ignore


def json_response(response):
    return jsonify(jsonpickle.pickler.Pickler(unpicklable=False).flatten(response))


def create_app(config):
    from src.lib.web import json_response
    from src.lib.errors import ApplicationError
    from config import config

    app = Flask(__name__)

    @app.errorhandler(ApplicationError)
    def handle_exception(e):
        return json_response(e.data), e.status_code

    if "JWT_SECRET_KEY" in config:
        app.config["JWT_SECRET_KEY"] = config["JWT_SECRET_KEY"]
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.get(
            "JWT_ACCESS_TOKEN_EXPIRES", 3600 * 2
        )

        JWTManager(app)

        def get_current_user_id():
            verify_jwt_in_request(optional=True)
            return get_jwt_identity()

        app.get_current_user_id = get_current_user_id
    else:
        app.get_current_user_id = lambda: None

    return app
