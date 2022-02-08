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
                                            <label for="label" class="form-label">Label</label>
                                            <input v-model="formData.label" type="text" class="form-control" id="label" name="label" placeholder="Enter a Label...">
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="size" class="form-label">Size</label>
                                            <select v-model="formData.size" class="form-select" id="size" name="size" aria-label="Select Spot size">
                                                <option disabled>Select Spot size</option>
                                                <option value="1">Small spot</option>
                                                <option value="2">Medium spot</option>
                                                <option value="3">Large spot</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-12 mb-3"><hr><small><i>The data below refers to the distance of this spot from the given Entrance/s.</i></small></div>
                                    <div class="col-12">
                                        <div class="row">
                                            <div class="col-6"><label class="form-label">Entrances</label></div>
                                            <div class="col-6"><label class="form-label">Distance</label></div>
                                        </div>
                                    </div>
                                    <div v-for="data in subformData" v-bind:key="data" class="col-12">
                                        <div class="row">
                                            <div class="col-6">
                                                <div class="mb-3">
                                                    <input v-model="data.entrance_name" type="text" class="form-control" disabled>
                                                </div>
                                            </div>
                                            <div class="col-6">
                                                <div class="mb-3">
                                                    <input v-model="data.distance" type="number" class="form-control" name="distance">
                                                </div>
                                            </div>
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

export default {
    name: 'SpotForm',
    data(){
        return{
            formId: '',
            formAction: '',
            formData: {},
            subformData: {},
            editPass: false
        }
    },
    methods:{
        async getSubRecord(){
            const params = {
                id: this.formId
            }
            if (this.formAction == 1){
                const response = await this.$http.get('/spot/entrances/',
                { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}, params: params })
                if (!response.data['entrance']){
                    if (response.data['response'] == 401){
                        localStorage.removeItem('plotid')
                        this.$router.push({ name: 'Login'})
                    }
                    return
                }  
                this.subformData = response.data['entrance']
            }
        },
        async retrieveRecord(){
            const params = {
                id: this.formId
            }
            const response = await this.$http.get('/spot/form/',
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}, params: params })
            if (!response.data['record']){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return
            }
            this.formData = response.data['record'][0]
            if (this.formAction == 2){
                this.subformData = response.data['subrecord']
            }
        },
        async submitRecord(e){
            e.preventDefault()
            const formData = this.formData
            formData['action'] = this.formAction
            formData['id'] = this.formId
            delete formData['distance']
            formData['subdata'] = this.subformData
            const response = await this.$http.post('/spot/form/', formData,
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}})
            if (response.data['response'] != 200){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return this.popup('error', 'Error.', 'Your record was not saved.', 1500)
            }
            this.$router.push({ path: '/spot', query: { prevaction: this.formAction, submit: 1 } })
        },
        upLevel(){
            this.$router.push({ path: '/spot' })
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
        if (this.formAction == 2){
            this.retrieveRecord()
        }
        else{
            this.getSubRecord()
        }
    }
}
</script>