<template>
    <div class="row mt-5">
        <div class="d-none d-md-block col-md-1 col-lg-2"></div>
        <div class="col-12 col-md-10 col-lg-8">
            <div class="card">
                <div v-text="token" class="card-body">
                    
                </div>
            </div>
        </div>
        <div class="d-none d-md-block col-md-1 col-lg-2"></div>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data(){
        return {
            token: ''
        }
    },
    methods: {
        async submitLogin(){
            const response = await this.$http.post('/auth/', 
            { username: 'test', password: 'test' },
            { headers: { Accept: 'application/json', 'Content-type': 'application/json'}})
            localStorage.setItem('plot-ok',response.data.token)
        }
    },
    mounted(){
    }
}
</script>