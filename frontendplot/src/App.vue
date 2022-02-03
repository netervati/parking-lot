<template>
  <div class="container-fluid">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
@import "~bootstrap/dist/css/bootstrap.min.css";
.bg-main{
  background-color: #080F5B;
}
.bg-main-gradient{
  background: rgb(9,13,57);
  background: linear-gradient(0deg, rgba(9,13,57,1) 0%, rgba(8,15,91,1) 100%);
}
html, body{
  font-family: 'Roboto';
}
.form-label{
  font-weight: bolder;
}
</style>
