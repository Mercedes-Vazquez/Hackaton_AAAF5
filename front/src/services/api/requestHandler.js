export default {
  prefix: "",
  status: null,
  authToken: null,
  async request(method, url, data = undefined, expectJSON = true) {
    const response = await (this.fetch || fetch)(this.prefix + url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: this.authToken ? `Bearer ${this.authToken}` : undefined,
      },
      body: data ? JSON.stringify(data) : undefined,
    });
    this.status = response.status;

    if (response.ok) {
      if (expectJSON) {
        return await response.json();
      } else {
        return await response.text();
      }
    }
  },

  async get(url) {
    return await this.request("GET", url);
  },

  async post(url, data, expectJSON = false) {
    return await this.request("POST", url, data, expectJSON);
  },

  async put(url, data, expectJSON = false) {
    return await this.request("PUT", url, data, expectJSON);
  },

  async delete(url) {
    return await this.request("DELETE", url);
  },
};
