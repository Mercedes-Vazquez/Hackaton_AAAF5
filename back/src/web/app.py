from src.lib.web import create_app, request, create_access_token, json_response

from config import config

from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.repository.goal_repository import GoalRepository
from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository

app = create_app(config)

goal_repository = GoalRepository(config)
goal_interactor = GoalInteractor(config, goal_repository)
user_repository = UserRepository(
    config, get_current_user_id=app.get_current_user_id)
user_interactor = UserInteractor(config, user_repository)


@app.route("/")
def home():
    return "magic ..."


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = user_interactor.auth_user(username, password)
    access_token = create_access_token(identity=user.id)
    return json_response({"access_token": access_token, "user": user})


@app.route("/api/goals", methods=["GET"])
def all_goals_get():
    return json_response(goal_interactor.get_all_goals()), 200


@app.route("/api/goals/<id>/tasks", methods=["GET"])
def all_tasks_by_goal_id_get(id):
    return json_response(goal_interactor.get_all_goals(id)), 200


@app.route("/api/frequency", methods=["GET"])
def routine_accomplishment_get(id):
    return json_response(user_interactor.get_current_users_routine_accomplishment()), 200


@app.route("/api/log/update", methods=["POST"])
def update_log_post(id):
    data = request.get_json()
    return json_response(user_interactor.update_current_user_log(data)), 200
