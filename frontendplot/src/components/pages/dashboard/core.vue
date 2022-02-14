<template>
    <div class="row">
        <Menu />
        <div class="col-12">
            <h4><b v-text="moduleTitle"></b></h4>
        </div>
        <div class="col-12">
            <div class="row">
                <div class="col-12 col-md-4 mt-3">
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
                <div class="col-12 col-md-4 mt-3">
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
                <div class="col-12 col-md-4 mt-3">
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
            <div class="row">
                <div class="col-12 col-md-8 mt-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="table-responsive overflow">
                                <BarChart :chartData="barChartData" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-4 mt-3">
                    <div class="card">
                        <div class="card-body text-center">
                            <small>Vehicle Types</small>
                            <DoughnutChart :chartData="doughnutChartData" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>

<script>
import Menu from '../../layout/menu.vue'
import Footer from '../../layout/footer.vue'
import { BarChart, DoughnutChart } from 'vue-chart-3';
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

export default {
    name: 'Dashboard',
    components:{
        Menu, BarChart, DoughnutChart, Footer
    },
    data(){
        return{
            moduleTitle: '',
            stats: {
                freeSpots: 0,
                todayProfit: 0,
                currentParked: 0
            },
            barChartData: {
                labels: ['12am', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm'],
                datasets: [
                    {
                        label: 'Peak Hours',
                        backgroundColor: ['#77CEFF', '#0079AF', '#123E6B', '#97B0C4', '#A5C8ED'],
                    },
                ],
            },
            doughnutChartData: {
                labels: ['Small', 'Medium', 'Large',],
                datasets: [
                    {
                        label: 'Vehicle Types',
                        backgroundColor: ['#FFC300', '#C70039', '#581845'],
                    },
                ],
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
            this.barChartData.datasets[0].data = response.data['stats']['peakHours']
            this.doughnutChartData.datasets[0].data = response.data['stats']['vehicleType']
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