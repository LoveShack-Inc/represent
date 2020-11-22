<template>
  <div id="app">
    <repp-nav title="Repp"></repp-nav>
    <router-view/>
  </div>

</template>

<script>
import ReppNav from './components/ReppNav.vue'

export default {
  name: 'App',
  components: {
    ReppNav,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
