<template>
    <nav class="navbar p-1 navbar-expand-lg navbar-dark bg-main shadow-sm mb-3">
        <div class="container-fluid">
            <router-link class="text-decoration-none" to="/"><a class="navbar-brand"><b>PARKING SYSTEM</b></a></router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="text-decoration-none" to="/"><a v-bind:class="setClasses('Dashboard')"><b>Dashboard</b></a></router-link>
                    </li>
                    <li class="nav-item">
                        <a v-on:click="logout()" role="button" v-bind:class="setClasses()"><b>Logout</b></a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    export default {
        name: 'Menu',
        methods:{
            logout(){
                localStorage.removeItem('plotid')
                this.$router.push({ name: 'Login'})
            },
            setClasses(name){
                if (name == this.$route.name){
                    return "nav-link active"
                }
                else{
                    return "nav-link"
                }
            }
        }
    }
</script>
