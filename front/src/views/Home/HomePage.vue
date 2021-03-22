<template>
  <div class="home-page">
    <h1>This is the home page</h1>
    <HelloWorld :msg="message" />
  </div>
</template>

<script>
import HelloWorld from "./HelloWorld.vue";

export default {
  name: "Home",
  components: { HelloWorld },
  data() {
    return {
      message: "Hello, world!",
    };
  },
};
</script>

<style scoped>
.home-page {
  text-align: center;
}
</style>
