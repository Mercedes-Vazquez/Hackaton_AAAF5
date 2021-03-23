<template>
  <div class="home-page">
    <h1>This is the home page</h1>
    <!-- <HelloWorld :msg="message" />
    <Frecuency />
    <TaskListPage /> -->

  </div>
</template>

<script>
// import HelloWorld from "./HelloWorld.vue";
// import TaskListPage from "../TaskList/TaskListPage.vue";
// import Frecuency from "../TaskList/Frecuency.vue";
export default {
  name: "Home",
  // components: {
  //   HelloWorld,
  //   TaskListPage,
  //   Frecuency,
  // },
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
