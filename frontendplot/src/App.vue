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
@import "~bootstrap-icons/font/bootstrap-icons.css";

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
.table-responsive{
  height: 500px;
}
.registry{
  height: 600px;
}
.registry-table thead tr th{
  font-size: 16px;
}
.registry-table tbody tr td{
  font-size: 14px;
}
.bg-main-light{
  background-color: #F5F9FD;
}
</style>
