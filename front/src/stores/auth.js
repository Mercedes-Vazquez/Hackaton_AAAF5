import Vue from "vue";
import api from "@/services/api";

const authStore = new Vue({
  data() {
    return {
      user: {},
    };
  },
  computed: {
    isUserLogged() {
      return Object.keys(this.user).length != 0;
    },
  },
  methods: {
    async login(loginData) {
      const response = await api.post("/api/auth/login", loginData, true);
      console.log(api.status);
      if (api.status === 200) {
        api.authToken = response.access_token;
        this.user = response.user;
        return true;
      } else {
        api.authToken = null;
        this.user = {};
        return false;
      }
    },
    logout() {
      api.authToken = null;
      this.user = {};
    },
    install(Vue) {
      const that = this;
      Object.defineProperty(Vue.prototype, "$auth", {
        get() {
          return that;
        },
      });
    },
  },
});

Vue.use(authStore);

export default authStore;
