<template>
  <div class="login-container">
    <input type="text" v-model="username" placeholder="login..." required />
    <input
      type="password"
      v-model="password"
      placeholder="password..."
      required
    />
    <div class="button" @click="onLoginButtonClicked">LOGIN</div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async onLoginButtonClicked() {
      const loginData = { username: this.username, password: this.password };
      const ok = await this.$auth.login(loginData);
      if (!ok) {
        alert("invalid username or password");
      } else {
        this.$router.push("/home");
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.button {
  font-size: 0.9rem;
  padding: 0.5rem;
  background-color: lightgray;
  cursor: pointer;
  box-shadow: 5px 3px 3px 0;
  border-radius: 3px;
  margin-top: 1rem;
}

.button:hover {
  opacity: 0.8;
}
</style>
