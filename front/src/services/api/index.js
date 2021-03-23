import requestHandler from "./requestHandler";

const api = {
  ...requestHandler,

  async getRoutineAccomplishment() {
    return await this.get("/api/frequency");
  },
  async updateLog() {
    const data = { timestamp: new Date().toISOString() };
    return await this.post("/api/log/update", data);
  },
  async getPoints() {
    return await this.get("/api/points");
  },
  async getGoals() {
    return await this.get("/api/goals");
  },
  async getUsers() {
    return await this.get("/api/users");
  },
  async registerUser(data) {
    return await this.post("/api/users", data);
  },
  async saveUserProfile(data, user_id) {
    return await this.patch(`/api/users/${user_id}`, data);
  },
  async assignUser(data) {
    return await this.post("/api/users/assign", data);
  },
  async unassignUser(data) {
    return await this.post("/api/users/unassign", data);
  },
  async getGoalsByDate(user_id, date) {
    return await this.get(`/api/users/${user_id}/goals/${date}`);
  },
  async saveGoal(goal_id, data) {
    return await this.put(`/api/goals/${goal_id}`, data);
  },
  async deleteGoal(goal_id) {
    return await this.delete(`/api/goals/${goal_id}`);
  },
  async getTaskByGoalId(goal_id) {
    return await this.get(`/api/goals/${goal_id}/tasks`);
  },
  async saveTask(goal_id, task_id, data) {
    return await this.get(`/api/goals/${goal_id}/tasks/${task_id}`, data);
  },
  async deleteTask(goal_id, task_id) {
    return await this.delete(`/api/goals/${goal_id}/tasks/${task_id}`);
  },
  async getUserProgress(user_id) {
    return await this.get(`/api/users/${user_id}/progress`);
  },
};

export default api;
