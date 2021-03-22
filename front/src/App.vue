<template>
  <div id="app">
    <Header></Header>
    <div id="main">
      <router-view />
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from "@/views/_common/Header.vue";
import Footer from "@/views/_common/Footer.vue";

export default {
  name: "App",
  components: {
    Header,
    Footer,
  },
};
</script>

<style>
#main {
  flex: 1;
}
</style>
