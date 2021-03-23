<template>
  <div v-show="show">
    <p>{{ hint }}</p>
    <div @click="onAcceptButtonClicked">Aceptar</div>
  </div>
</template>

<script>
export default {
  name: "HintDialog",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    hint: {
      type: String,
      required: true,
    },
  },
  methods: {
    onAcceptButtonClicked() {
      this.$emit("close-dialog");
    },
  },
};
</script>

<style scoped>

</style>
