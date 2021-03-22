import requestHandler from "./requestHandler";

const api = {
  ...requestHandler,

  async getTasks() {
    return await this.get("/api/tasks");
  },
};

export default api;
