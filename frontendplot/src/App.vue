<template>
  <div class="container-fluid">
    <Menu class="mb-3" />
    <router-view/>
  </div>
</template>

<script>
import Menu from './components/layout/Menu.vue'

export default {
  name: 'App',
  components:{
    Menu
  }
}
</script>

<style>
@import "~bootstrap/dist/css/bootstrap.min.css";
</style>
