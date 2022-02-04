<template>
    <div class="row mt-3">
        <div class="col-12">
            <div class="card">
                <div class="card-body">
                    <div class="row">
                        <div class="col-12">
                            <button class="btn btn-sm btn-outline-secondary" v-on:click="upLevel()"><i class="fas fa-angle-double-left"></i> Back to Registry</button>
                        </div>
                    </div>
                    <div class="row mt-5">
                        <div class="col-6">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input v-model="formData.username" type="text" class="form-control" id="username" placeholder="Enter a username...">
                            </div>
                        </div>
                    </div>
                    <div class="row mt-5">
                        <div class="col-12 text-center">
                            <button class="btn btn-outline-success ms-2 me-2"><i class="fas fa-save"></i> Save</button>
                            <button class="btn btn-outline-danger ms-2 me-2" v-on:click="upLevel()"><i class="fas fa-ban"></i> Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'UserForm',
    data(){
        return{
            formId: '',
            formAction: '',
            formData: {}
        }
    },
    methods:{
        async retrieveData(){
            const params = {
                username: this.formId
            }
            const response = await this.$http.get('/user/getdata/',
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}, params: params })
            if (response.data['record']){
                this.formData = response.data['record'][0]
            }  
            else{
                if (response.data['error'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
            }
        },
        openData(){
            
        },
        upLevel(){
            this.$router.push({ path: '/user' })
        }
    },
    mounted(){
        this.formId = this.$route.query.id
        this.formAction = this.$route.query.action
        this.retrieveData()
    }
}
</script>