from src.lib.web import create_app, request, create_access_token, json_response

from config import config

from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.repository.goal_repository import GoalRepository
from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository

app = create_app(config)

goal_repository = GoalRepository(config)
user_repository = UserRepository(
    config, get_current_user_id=app.get_current_user_id)
goal_interactor = GoalInteractor(config, goal_repository, user_repository)
user_interactor = UserInteractor(config, user_repository, goal_repository)


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


@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json()
    user_interactor.register_user(data)
    return "", 200


@app.route("/api/users", methods=["GET"])
def assigned_users_get(id):
    return json_response(user_interactor.get_all_assigned_users()), 200


@app.route("/api/users/<id>", methods=["PATCH"])
def user_profile_update_patch(id):
    data = request.get_json()
    user_interactor.update_user_profile(id, data)
    return "", 200


@app.route("/api/users/assign", methods=["POST"])
def assign_user_post():
    data = request.get_json()
    user_interactor.assign_user(data)
    return "", 200


@app.route("/api/users/unassign", methods=["POST"])
def unassign_user_post():
    data = request.get_json()
    user_interactor.unassign_user(data)
    return "", 200


@app.route("/api/goals", methods=["GET"])
def all_goals_get():
    return json_response(goal_interactor.get_current_users_daily_goals()), 200


@app.route("/api/goals/<goal_id>", methods=["PUT"])
def goal_by_id_put():
    data = request.get_json()
    goal_interactor.save_goal(data)
    return "", 200


@app.route("/api/goals/<goal_id>", methods=["DELETE"])
def goal_by_id_delete(goal_id):
    goal_interactor.delete_goal_by_id(goal_id)
    return "", 200


@app.route("/api/goals/<goal_id>/tasks", methods=["GET"])
def all_tasks_by_goal_id_get(goal_id):
    return json_response(goal_interactor.get_all_tasks_by_goal_id(goal_id)), 200


@app.route("/api/goals/<goal_id>/tasks/<task_id>", methods=["DELETE"])
def task_by_id_delete(task_id):
    goal_interactor.delete_task_by_id(task_id)
    return "", 200


@app.route("/api/goals/<goal_id>/tasks/<task_id>", methods=["PUT"])
def task_by_id_put():
    data = request.get_json()
    goal_interactor.save_task(data)
    return "", 200


@app.route("/api/frequency", methods=["GET"])
def routine_accomplishment_get():
    return json_response(user_interactor.get_current_users_routine_accomplishment()), 200


@app.route("/api/log/update", methods=["POST"])
def update_log_post():
    data = request.get_json()
    return json_response(user_interactor.update_current_user_log(data)), 200


@app.route("/api/points", methods=["GET"])
def points_get():
    return json_response(user_interactor.get_current_users_points()), 200


@app.route("/api/users/<user_id>/goals/<date>", methods=["GET"])
def all_goals_by_date_and_user_id_get(user_id, date):
    goals = goal_interactor.get_goals_by_date_and_assigned_user_id(
        date, user_id)
    return json_response(goals), 200


@app.route("/api/users/<user_id>/progress", methods=["GET"])
def progress_by_user_id_get(user_id):
    progress = goal_interactor.get_progress_by_user_id(user_id)
    return json_response(progress), 200
