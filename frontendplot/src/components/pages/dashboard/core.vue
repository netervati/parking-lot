<template>
    <div class="row">
        <Menu />
        <div class="col-lg-12">
        </div>
    </div>
</template>

<script>
import Menu from '../../layout/menu.vue'

export default {
    name: 'Dashboard',
    components:{
        Menu
    },
    data(){
        return {
        }
    },
    methods:{
        async retrieveData(){
            const response = await this.$http.get(' ',
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}})
            if (response.data['users']){
                // this.apiMsg = response.data
                console.log(response.data)
            }  
            else{
                localStorage.removeItem('plotid')
                this.$router.push({ name: 'Login'})
            }
        }
    },
    mounted(){
        this.retrieveData()
    }
}
</script>

<style scoped>

</style>