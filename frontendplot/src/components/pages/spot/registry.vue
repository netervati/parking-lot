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
                                <option value="3">Label (Desc)</option>
                                <option value="4">Label (Asc)</option>
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
                                    <th>Label</th>
                                    <th>Size</th>
                                    <th>Availability</th>
                                    <th>Created On</th>
                                    <th>Updated On</th>
                                    <th>Created By</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white">
                                <tr v-for="data in registryData" v-bind:key="data">
                                    <td class="text-center">
                                        <button v-on:click="openData(data.id)" title="Edit Record" class="btn btn-sm btn-outline-primary m-1"><i class="bi bi-pencil-square"></i></button>
                                        <button v-on:click="requestDelete(data.id)" title="Delete Record" class="btn btn-sm btn-outline-danger m-1"><i class="bi bi-trash-fill"></i></button>
                                    </td>
                                    <td>{{data.label}}</td>
                                    <td>
                                        <span v-if="data.size == 1" class="badge bg-secondary w-100">Small</span>
                                        <span v-else-if="data.size == 2" class="badge bg-warning w-100">Medium</span>
                                        <span v-else class="badge bg-info w-100">Large</span>
                                    </td>
                                    <td class="text-center">
                                        <b class="text-success" v-if="data.open == true">Free</b>
                                        <b class="text-danger" v-else>Occupied</b>
                                    </td>
                                    <td>{{data.created_on}}</td>
                                    <td>{{data.updated_on}}</td>
                                    <td>{{data.created_by}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
    name: 'SpotRegistry',
    data(){
        return{
            registryData: [],
            allowPrev: false,
            allowNext: false,
            curPage: 0,
            curSort: 1,
            curSearch: ''
        }
    },
    methods:{
        async retrieveData(){
            const response = await this.$http.get('/spot/registry/', 
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
            this.$router.push({ path: '/spot/f', query: { action: 1 } })
        },
        openData(value){
            this.$router.push({ path: '/spot/f', query: { id: value, action: 2 } })
        },
        async deleteData(value){
            const response = await this.$http.post('/spot/form/', {id: value, action: '3'},
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
            this.$router.replace({path: '/spot', query:{page: this.curPage} })
            this.retrieveData()
        },
        goNext(){
            this.curPage++
            this.allowPrev = true
            this.$router.replace({path: '/spot', query:{page: this.curPage} })
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