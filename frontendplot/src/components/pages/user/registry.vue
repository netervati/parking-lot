<template>
    <div class="card mt-3">
        <div class="card-body border-top border-primary">
            <div class="row">
                <div class="col-12">
                    <div class="row">
                        <div class="col-12 col-md-4">
                            <div class="input-group input-group-sm mb-3">
                                <span class="input-group-text" id="addon-search"><i class="fas fa-search"></i></span>
                                <input type="text" class="form-control" placeholder="Search text..." aria-label="Username" aria-describedby="addon-search">
                            </div>
                        </div>
                        <div class="col-6 col-sm-3 col-md-2">
                            <select class="form-select form-select-sm mb-3" aria-label="Select Sort">
                                <option disabled>Select Sort</option>
                                <option selected value="1">Created On (Desc)</option>
                                <option value="2">Created On (Asc)</option>
                                <option value="3">Name (Desc)</option>
                                <option value="4">Name (Asc)</option>
                            </select>
                        </div>
                        <div class="col-6 col-sm-3 col-md-2">
                            <button class="btn btn-sm btn-outline-dark w-100">Filter</button>
                        </div>
                        <div class="col-12 col-sm-6 col-md-4">
                            <nav aria-label="Page navigation example">
                                <ul class="pagination pagination-sm float-end">
                                    <li class="page-item disabled"><a class="page-link" href="#">Previous</a></li>
                                    <li class="page-item"><a class="page-link" href="#">1</a></li>
                                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                                    <li class="page-item"><a class="page-link" href="#">4</a></li>
                                    <li class="page-item"><a class="page-link" href="#">5</a></li>
                                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
                <div class="col-12 registry">
                    <div class="table-responsive-sm overflow-x">
                        <table class="table table-sm table-bordered registry-table w-100">
                            <thead>
                                <tr class="text-center bg-light">
                                    <th>Actions</th>
                                    <th>Username</th>
                                    <th>Created On</th>
                                    <th>Updated On</th>
                                </tr>
                            </thead>
                            <tbody v-for="data in registryData" v-bind:key="data"  class="bg-white">
                                <tr>
                                    <td class="text-center">
                                        <button v-on:click="openData(data.username)" title="Edit Record" class="btn btn-sm btn-outline-primary m-1"><i class="fas fa-edit"></i></button>
                                        <button title="Delete Record" class="btn btn-sm btn-outline-danger m-1"><i class="fas fa-trash"></i></button>
                                    </td>
                                    <td class="text-center">{{data.username}}</td>
                                    <td class="text-center">{{data.created_on}}</td>
                                    <td class="text-center">{{data.updated_on}}</td>
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
export default {
    name: 'UserRegistry',
    data(){
        return{
            registryData: []
        }
    },
    methods:{
        async retrieveData(){
            const response = await this.$http.get(' ', 
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')} })
            if (response.data['users']){
                this.registryData = response.data['users']
            }  
            else{
                if (response.data['error'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
            }
        },
        openData(value){
            this.$router.push({ path: '/user/f', query: { id: value, action: '2' } })
        }
    },
    mounted(){
        this.retrieveData()
    }
}
</script>