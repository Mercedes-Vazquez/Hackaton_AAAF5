<template>
  <div>
    <h2>Tareas diarias</h2>
    <div v-for="goal in goals" :key="goal.id" @click="onGoalClicked(goal)">
      <div>{{ goal.date }}</div>
      <div>{{ goal.title }}</div>
      <div>{{ goal.category }}</div>
      <div>{{ goal.status }}</div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "Home",
  data() {
    return {
      routineAccomplishment: [],
      goals: [],
    };
  },
  methods: {
    async getRoutineAccomplishment() {
      this.routineAccomplishment = await api.getRoutineAccomplishment();
    },
    async getGoals() {
      this.goals = await api.getGoals();
    },
    async onGoalClicked(goal) {
      this.$router.push(`/goal/${goal.id}`);
    },
  },
  async created() {
    await this.getRoutineAccomplishment();
    await this.getGoals();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
</style>
