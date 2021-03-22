<template>
  <div class="test-page">
    <h1>This is the test page</h1>
    <JsonEditor v-model="data"></JsonEditor>
    <h1>This is the test page</h1>
    <pre>{{ JSON.stringify($data, null, 2) }}</pre>
  </div>
</template>

<script>
import JsonEditor from "@/views/_common/util/JsonEditor.vue";

export default {
  name: "TestPage",
  components: { JsonEditor },
  data() {
    return {
      data: {},
    };
  },
};
</script>
