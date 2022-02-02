<template>
    <div class="row">
        <nav class="navbar p-1 navbar-expand-lg navbar-light bg-warning shadow-sm">
        <div class="container-fluid">
            <router-link class="text-decoration-none" to="/"><a class="navbar-brand"><b>PARKING SYSTEM</b></a></router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="text-decoration-none" to="/"><a class="nav-link"><b>Dashboard</b></a></router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="text-decoration-none" to="/login"><a class="nav-link"><b>Login</b></a></router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    </div>
</template>

<script>
    export default {
        name: 'Menu'
    }
</script>
