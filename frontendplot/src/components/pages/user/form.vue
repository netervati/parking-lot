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
                                            <label for="username" class="form-label">Username</label>
                                            <input v-model="formData.username" type="text" class="form-control" id="username" name="username" placeholder="Enter a username...">
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="mb-3">
                                            <label for="password" class="form-label">Password 
                                                <button type="button" :hidden="formAction == 1" class="btn btn-sm btn-dark pt-0 pb-0 ps-1 pe-1" v-on:click="swapPass()" ><i v-if="editPass == false" class="bi bi-lock"></i><i v-else class="bi bi-unlock"></i></button>
                                            </label>
                                            <input type="password" class="form-control" id="password" name="password" placeholder="Enter a password..." :disabled="editPass == false && this.formAction == 2">
                                            <small></small>
                                        </div>
                                    </div>
                                    <div class="col-12">
                                        <div class="mb-3">
                                            <label for="username" class="form-label">Full Name</label>
                                            <input v-model="formData.fullname" type="text" class="form-control" id="fullname" name="fullname" placeholder="Enter a full name...">
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
    name: 'UserForm',
    data(){
        return{
            formId: '',
            formAction: '',
            formData: {},
            editPass: false
        }
    },
    methods:{
        async retrieveRecord(){
            const params = {
                id: this.formId
            }
            const response = await this.$http.get('/user/form/',
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
            const formData = Object.fromEntries(new FormData(e.target));
            formData['action'] = this.formAction
            formData['id'] = this.formId
            if (this.formAction == 2){
                if (this.editPass == false) delete formData.password
            }
            const response = await this.$http.post('/user/form/', formData,
            { headers: { Accept: 'application/json', 'Content-type': 'application/json', Authorization: localStorage.getItem('plotid')}})
            if (response.data['response'] != 200){
                if (response.data['response'] == 401){
                    localStorage.removeItem('plotid')
                    this.$router.push({ name: 'Login'})
                }
                return this.popup('error', 'Error.', 'Your record was not saved.', 1500)
            }
            this.$router.push({ path: '/user', query: { prevaction: this.formAction, submit: 1 } })
        },
        upLevel(){
            this.$router.push({ path: '/user' })
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
    }
}
</script>