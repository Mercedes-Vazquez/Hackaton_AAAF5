<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </div>
</template>

<style scoped>
#nav {
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 2rem;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
