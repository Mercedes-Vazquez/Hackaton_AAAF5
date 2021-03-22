<template>
  <div>
    <h1>Cosas que tengo pendientes</h1>
    <div class="task-list">
      <div class="task-item" v-for="task in tasks" :key="task.id">
        <span v-if="task.pending">&#x2610;</span>
        <span v-else>&#x2611;</span>
        {{ task.text }}
      </div>
    </div>
    <hr />
    <pre>route.params:<br>{{JSON.stringify($route.params, null, 2)}}</pre>
    <pre>data:<br>{{JSON.stringify($data, null, 2)}}</pre>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "Home",
  data() {
    return {
      tasks: [],
    };
  },
  methods: {
    async getTasks() {
      this.tasks = await api.getTasks();
    },
  },
  created() {
    this.getTasks();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
</style>
