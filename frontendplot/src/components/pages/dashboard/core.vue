<template>
    <div class="row">
        <Menu />
        <div class="col-12">
            <h4><b v-text="moduleTitle"></b></h4>
        </div>
        <div class="col-12 mt-3">
            <div class="row">
                <div class="col-4">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-4">
                                    <h3><i class="bi bi-truck"></i></h3>
                                </div>
                                <div class="col-8 text-end">
                                    <h3><b v-text="stats.currentParked"></b></h3>
                                </div>
                                <div class="col-12 text-end">
                                    <p>Customers parked</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-4">
                                    <h3><i class="bi bi-cone-striped"></i></h3>
                                </div>
                                <div class="col-8 text-end">
                                    <h3><b v-text="stats.freeSpots"></b></h3>
                                </div>
                                <div class="col-12 text-end">
                                    <p>Available spots</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-4">
                                    <h3><i class="bi bi-cash-coin"></i></h3>
                                </div>
                                <div class="col-8 text-end">
                                    <h3><b v-text="stats.todayProfit"></b></h3>
                                </div>
                                <div class="col-12 text-end">
                                    <p>Today's Profit</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
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
        return{
            moduleTitle: '',
            stats: {
                freeSpots: 0,
                todayProfit: 0,
                currentParked: 0
            }
        }
    },
    methods: {
        async retrieveData(){
            const response = await this.$http.get('/dashboard/', 
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')} })
            if (!response.data['stats']){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return 
            }  
            this.stats = response.data['stats']
        }
    },
    mounted(){
        this.moduleTitle = this.$route.matched[0].name
        this.retrieveData()
    }
}
</script>

<style scoped>

</style>