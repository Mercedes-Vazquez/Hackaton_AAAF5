<template>
  <div class="json-editor" :class="is_error && 'json_error'">
    <textarea @keyup="changed = true" v-model="text"></textarea>
    <button v-if="changed" @click="onChange">Aceptar</button>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      text: "",
      is_error: false,
      changed: false,
    };
  },
  methods: {
    onChange(e) {
      const text = this.text;
      console.log("input", text, e.target.value);
      try {
        const data = JSON.parse(text);
        console.log("data ok", text, data);
        this.$emit("input", data);
        this.$emit("change", data);
        this.is_error = false;
        console.log("error no");
      } catch (e) {
        this.is_error = true;
        console.log("error yeyes");
      }
    },
  },
  watch: {
    value: {
      handler: function (newVal) {
        this.text = JSON.stringify(newVal, null, 2);
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
div.json-editor textarea {
  width: 100%;
  height: 100%;
}
div.json-editor.json_error textarea {
  border: 1px solid red;
}
</style>
