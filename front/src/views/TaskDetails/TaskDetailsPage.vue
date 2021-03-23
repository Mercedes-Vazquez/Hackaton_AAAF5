<template>
  <div>
    <div>
      <h2>{{ tasks[current_tasks_index].title }}</h2>
      <p>{{ tasks[current_tasks_index].description }}</p>
    </div>
    <div @click="onHintButtonClicked">Pista</div>
    <div @click="onNextButtonClicked">Siguiente</div>
    <HintDialog
      :show="showDialog"
      :hint="tasks[current_tasks_index].hint"
      @close-dialog="closeDialog"
    ></HintDialog>
  </div>
</template>

<script>
import api from "@/services/api";
import HintDialog from "./HintDialog.vue";

export default {
  name: "TaskDetails",
  components: {
    HintDialog,
  },
  data() {
    return {
      current_tasks_index: 0,
      tasks: [],
      showDialog: false,
    };
  },
  methods: {
    async getTasks() {
      const id = this.$route.params.id;
      console.log(id);
      this.tasks = await api.getTasksByGoalId(id);
    },
    onNextButtonClicked() {
      if (this.current_tasks_index == this.tasks.length - 1) {
        const goalId = this.$route.params.id;
        this.$router.push(`/goal/${goalId}/feedback`);
      }
      this.current_tasks_index += 1;
    },
    onHintButtonClicked() {
      this.showDialog = true;
    },
    closeDialog() {
      this.showDialog = false;
    },
  },
  async created() {
    await this.getTasks();
  },
};
</script>

<style scoped></style>
