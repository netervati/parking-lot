<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-main shadow-sm mb-3">
        <div class="container-fluid">
            <router-link class="text-decoration-none" to="/"><a class="navbar-brand">OOP PARKING LOT</a></router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="text-decoration-none" to="/"><a v-bind:class="setClasses('Dashboard',0)"><i class="bi bi-speedometer2"></i> Dashboard</a></router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="text-decoration-none" to="/parking"><a v-bind:class="setClasses('Parking',0)"><i class="bi bi-truck"></i> Parking</a></router-link>
                    </li>
                    <li class="nav-item dropdown">
                        <a v-bind:class="setParentClasses()" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-folder2-open"></i> Masterfiles</a>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <li><router-link class="text-decoration-none" to="/entrance"><a v-bind:class="setClasses('Entrance',1)"><i class="bi bi-box-arrow-in-right"></i> Entrance</a></router-link></li>
                            <li><router-link class="text-decoration-none" to="/spot"><a v-bind:class="setClasses('Spot',1)" href="#"><i class="bi bi-cone-striped"></i> Spot</a></router-link></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <router-link class="text-decoration-none" to="/user"><a v-bind:class="setClasses('User Accounts',0)"><i class="bi bi-people"></i> User Accounts</a></router-link>
                    </li>
                    <li class="nav-item">
                        <a role="button" v-bind:class="setClasses('',0)" v-on:click="logout()"><i class="bi bi-door-open"></i> Logout</a>
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
                this.$router.push({ path: '/login' })
            },
            setClasses(name,type){
                let defaultclass = type == 0 ? 'nav-link' : 'dropdown-item'
                if (name == this.$route.matched[0].name){
                    return `${defaultclass} active`
                }
                else{
                    return defaultclass
                }
            },
            setParentClasses(){
                let defaultclass = 'nav-link dropdown-toggle'
                if (this.$route.matched[0].name == 'Entrance' || this.$route.matched[0].name == 'Spot'){
                    return `${defaultclass} active`
                }
                else{
                    return defaultclass
                }
            }
        }
    }
</script>
