<template>
    <div class="card mt-3">
        <div class="card-body border-top border-primary">
            <div class="row">
                <div class="col-12">
                    <div class="row">
                        <div class="col-12 col-md-4">
                            <div class="input-group input-group-sm mb-3">
                                <span class="input-group-text" id="addon-search"><i class="bi bi-search"></i></span>
                                <input v-model="curSearch" type="text" class="form-control" placeholder="Search text..." aria-label="Username" aria-describedby="addon-search">
                            </div>
                        </div>
                        <div class="col-6 col-sm-3 col-md-2">
                            <select v-model="curSort" class="form-select form-select-sm mb-3" aria-label="Select Sort">
                                <option disabled>Select Sort</option>
                                <option selected value="1">Created On (Desc)</option>
                                <option value="2">Created On (Asc)</option>
                                <option value="3">Parked On (Desc)</option>
                                <option value="4">Parked On (Asc)</option>
                                <option value="5">Unparked On (Desc)</option>
                                <option value="6">Unparked On (Asc)</option>
                            </select>
                        </div>
                        <div class="col-6 col-sm-3 col-md-2">
                            <button v-on:click="retrieveData()" class="btn btn-sm btn-outline-dark w-100"> <i class="bi bi-filter-square"></i> Filter</button>
                        </div>
                        <div class="col-6 col-sm-3 col-md-2">
                            <button title="New Record" v-on:click="newData()" class="btn btn-sm btn-success"><i class="bi bi-journal-plus"></i> New</button>
                        </div>
                        <div class="col-6 col-md-2">
                            <nav aria-label="Page navigation example">
                                <ul class="pagination pagination-sm float-end">
                                    <li id="btn-prev" v-bind:class="setPaginationClass('btn-prev')"><a class="page-link" href="#" :disabled="allowPrev == true" v-on:click="goPrev()">Previous</a></li>
                                    <li id="btn-next" v-bind:class="setPaginationClass('btn-next')"><a class="page-link" href="#" :disabled="allowNext == true" v-on:click="goNext()">Next</a></li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
                <div class="col-12 registry">
                    <div class="table-responsive overflow-x">
                        <table class="table table-sm table-bordered registry-table">
                            <thead>
                                <tr class="text-center bg-light">
                                    <th>Actions</th>
                                    <th>Vehicle Plate No.</th>
                                    <th>Vehicle Size</th>
                                    <th>Total Fee</th>
                                    <th>Entrance</th>
                                    <th>Spot</th>
                                    <th>Spot Size</th>
                                    <th>Parked On</th>
                                    <th>Unparked On</th>
                                    <th>Created On</th>
                                    <th>Updated On</th>
                                    <th>Created By</th>
                                    <th>Updated By</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white">
                                <tr v-for="data in registryData" v-bind:key="data">
                                    <td class="text-center">
                                        <button v-if="!data.unparked_on" v-on:click="readyUnpark(data.id)" data-bs-toggle="modal" data-bs-target="#modal-unpark" title="Unpark Vehicle" class="btn btn-sm btn-outline-warning m-1"><i class="bi bi-alarm-fill"></i></button>
                                        <button v-if="!data.unparked_on" v-on:click="requestDelete(data.id)" title="Delete Record" class="btn btn-sm btn-outline-danger m-1"><i class="bi bi-trash-fill"></i></button>
                                    </td>
                                    <td class="text-center">{{data.vehicle_plateno}}</td>
                                    <td>
                                        <span v-if="data.vehicle_size == 1" class="badge bg-secondary w-100">Small</span>
                                        <span v-else-if="data.vehicle_size == 2" class="badge bg-warning w-100">Medium</span>
                                        <span v-else class="badge bg-info w-100">Large</span>
                                    </td>
                                    <td class="text-end">{{data.total_fee}}</td>
                                    <td>{{data.entrance_label}}</td>
                                    <td>{{data.spot_label}}</td>
                                    <td>
                                        <span v-if="data.spot_size == 1" class="badge bg-secondary w-100">Small</span>
                                        <span v-else-if="data.spot_size == 2" class="badge bg-warning w-100">Medium</span>
                                        <span v-else class="badge bg-info w-100">Large</span>
                                    </td>
                                    <td>
                                        <b v-if="data.unparked_on" class="text-success">{{data.parked_on}}</b>
                                        <b v-else class="text-danger">{{data.parked_on}}</b>
                                    </td>
                                    <td><b class="text-success">{{data.unparked_on}}</b></td>
                                    <td>{{data.created_on}}</td>
                                    <td>{{data.updated_on}}</td>
                                    <td>{{data.created_by}}</td>
                                    <td>{{data.updated_by}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <!-- Modal -->
        <div class="modal fade" id="modal-unpark" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Unpark this Vehicle?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <label for="unparked_on" class="form-label">Unparked On</label>
                    <datetime format="YYYY-MM-DD H:i:s" id="unparked_on" name="unparked_on" readonly></datetime>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">No</button>
                    <button type="button" class="btn btn-success" v-on:click="unparkVehicle()" data-bs-dismiss="modal">Yes</button>
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
    name: 'ParkingRegistry',
    components:{
        datetime
    },
    data(){
        return{
            registryData: [],
            allowPrev: false,
            allowNext: false,
            curPage: 0,
            curSort: 1,
            curSearch: '',
            queueUnpark: null
        }
    },
    methods:{
        async retrieveData(){
            const response = await this.$http.get('/parking/registry/', 
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}, params: {page: this.curPage, sort: this.curSort, search:this.curSearch} })
            if (!response.data['records']){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return 
            }  
            let data = response.data['records']
            if (response.data['records'].length <= response.data['limit'] || response.data['records'].length == 0){
                this.allowNext = false
            }
            else{
                this.allowNext = true
                data.pop()
            }
            this.registryData = response.data['records']
        },
        newData(){
            this.$router.push({ path: '/parking/f', query: { action: 1 } })
        },
        readyUnpark(value){
            this.queueUnpark = value
        },
        async unparkVehicle(){
            const response = await this.$http.post('/parking/form/', {id: this.queueUnpark, unparked_on: document.getElementById('tj-datetime-input').value, action: '2'},
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}})
            this.queueUnpark = null
            if (response.data['response'] != 200){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return this.popup('error', 'Error.', 'Vehicle was not unparked.', 1500)
            }
            this.retrieveData()
            return this.popup('success', 'Success.', 'Vehicle was unparked!', 1500)
        },
        async deleteData(value){
            const response = await this.$http.post('/parking/form/', {id: value, action: '3'},
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}})
            if (response.data['response'] != 200){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return this.popup('error', 'Error.', 'Your record was not deleted.', 1500)
            }
            this.retrieveData()
            return this.popup('success', 'Success.', 'Record deleted from the database!', 1500)
        },
        async requestDelete(value){
            let confirm = await Swal.fire({
                title: 'Confirm Action.',
                text: "Are you sure you want to delete this record?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!'
            }).then((result) => {
                if (result.isConfirmed) return true
                return false
            })
            if (confirm == true) this.deleteData(value)
        },  
        goPrev(){
            this.curPage--
            if (this.curPage == 0) this.allowPrev = false
            this.$router.replace({path: '/parking', query:{page: this.curPage} })
            this.retrieveData()
        },
        goNext(){
            this.curPage++
            this.allowPrev = true
            this.$router.replace({path: '/parking', query:{page: this.curPage} })
            this.retrieveData()
        },
        setPaginationClass(e){
            if (e == 'btn-next'){
                if (this.allowNext == true){
                    return 'page-item'
                }
                return 'page-item disabled'
            }
            else{
                if (this.allowPrev == true){
                    return 'page-item'
                }
                return 'page-item disabled'
            }
        },
        popup(result, title, msg){
            Swal.fire({
                icon: result,
                title: title,
                text: msg,
                timer: 1500
            })
        },
    },
    mounted(){
        if (this.$route.query.submit == 1){
            let successmsg = this.$route.query.prevaction == 1 ? 'Record added in the database!' : 'Record edited!'
            this.popup('success', 'Success.', successmsg, 1500)
        }
        this.retrieveData()
    }
}
</script>