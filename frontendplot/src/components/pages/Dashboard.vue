<template>
    <div class="row">
        <div class="col-lg-12">
            <p v-text="apiMsg"></p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Dashboard',
    data(){
        return {
            apiMsg: '',
            jwtToken: ''
        }
    },
    methods:{
        async retrieveData(){
            const response = await this.$http.get(' ',
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: this.jwtToken}})
            this.apiMsg = response.data
        }
    },
    // mounted(){
    //     this.jwtToken = localStorage.getItem('plot-ok')
    //     this.retrieveData()
    // }
}
</script>

<style scoped>

</style>