import requestHandler from "./requestHandler";

const api = {
  ...requestHandler,

  async getRoutineAccomplishment() {
    return await this.get("/api/frequency");
  },
};

export default api;
