<template>
    <div class="row mt-3">
        <div class="col-12">
            <div class="card">
                <div class="card-body">
                    <div class="row">
                        <div class="col-12">
                            <button class="btn btn-sm btn-outline-secondary" v-on:click="upLevel()"><i class="bi bi-chevron-double-left"></i> Back to Registry</button>
                        </div>
                    </div>
                    <div class="row mt-5">
                        <div class="col-12">
                            <form id="module-form" v-on:submit="submitRecord($event)" >
                                <div class="row">
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="parked_on" class="form-label">Parked On</label>
                                            <datetime format="YYYY-MM-DD H:i:s" v-model="formData.parked_on" id="parked_on" name="parked_on" readonly></datetime>
                                        </div>
                                    </div>
                                    <div class="col-6"></div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="vehicle_plateno" class="form-label">Vehicle Plate No.</label>
                                            <input v-model="formData.vehicle_plateno" type="text" class="form-control" id="vehicle_plateno" name="vehicle_plateno" placeholder="Enter a Vehicle Plate No....">
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="vehicle_size" class="form-label">Size</label>
                                            <select v-model="formData.vehicle_size" class="form-select" id="vehicle_size" name="vehicle_size" aria-label="Select Vehicle size">
                                                <option disabled>Select Vehicle size</option>
                                                <option value="1">Small</option>
                                                <option value="2">Medium</option>
                                                <option value="3">Large</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="entrance_id" class="form-label">Entrance</label>
                                            <select v-model="formData.entrance_id" class="form-select" id="entrance_id" name="entrance_id" aria-label="Select Entrance size">
                                                <option disabled>Select Entrance size</option>
                                                <option v-for="data in entranceData" v-bind:key="data" v-bind:value="data.entrance">{{data.entrance_name}}</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="spot_label" class="form-label">Spot</label>
                                            <input v-model="formData.spot_label" type="text" class="form-control" id="spot_label" name="spot_label" placeholder="Auto-picked" readonly>
                                            <small><i>Spot is picked if it is available and near to the entrance.</i></small>
                                        </div>
                                    </div>
                                    <div class="col-12 mt-5 text-center">
                                        <button type="submit" class="btn btn-outline-success ms-2 me-2"><i class="bi bi-save"></i> Save</button>
                                        <button type="button" class="btn btn-outline-danger ms-2 me-2" v-on:click="upLevel()"><i class="bi bi-stop-circle"></i> Cancel</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2'
import datetime from 'vuejs-datetimepicker';

export default {
    name: 'ParkingForm',
    data(){
        return{
            formId: '',
            formAction: '',
            formData: {parked_on:''},
            entranceData: {},
            editPass: false
        }
    },
    components: { datetime },
    methods:{
        async getEntranceRecord(){
            const response = await this.$http.get('/parking/entrances/',
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')} })
            if (!response.data['entrance']){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return
            }  
            this.entranceData = response.data['entrance']
            if (this.formAction == 2){
                this.retrieveRecord()
            }
        },
        async retrieveRecord(){
            const params = {
                id: this.formId
            }
            const response = await this.$http.get('/parking/form/',
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}, params: params })
            if (!response.data['record']){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return
            }  
            this.formData = response.data['record'][0]
        },
        async submitRecord(e){
            e.preventDefault()
            const formData = this.formData
            formData['action'] = this.formAction
            formData['id'] = this.formId
            formData['parked_on'] = document.getElementById('tj-datetime-input').value
            const response = await this.$http.post('/parking/form/', formData,
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}})
            if (response.data['response'] != 200){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return this.popup('error', 'Error.', 'Your record was not saved.', 1500)
            }
            this.$router.push({ path: '/parking', query: { prevaction: this.formAction, submit: 1 } })
        },
        upLevel(){
            this.$router.push({ path: '/parking' })
        },
        swapPass(){
            this.editPass = !this.editPass
        },
        popup(result, title, msg, timer){
            Swal.fire({
                icon: result,
                title: title,
                text: msg,
                timer: timer
            })
        },
    },
    mounted(){
        this.formId = this.$route.query.id
        this.formAction = this.$route.query.action
        this.getEntranceRecord()
    }
}
</script>

<style scoped>
    .form-date{
        width: inherit;
    }
</style>