<template>
    <div class="row bg-main vh-100">
        <div class="col-12">
            <div class="row">
                <div class="d-none d-sm-block col-sm-2 col-md-3 col-lg-4"></div>
                <div class="col-12 col-sm-8 col-md-6 col-lg-4 mt-5">
                    <div class="card mt-5">
                        <div class="card-body p-4 shadow-sm">
                            <p class="text-center">Welcome to the Parking System!<br>Please sign in.</p>
                            <form v-on:submit="submitLogin($event)">
                                <div class="mt-4">
                                    <label for="username" class="form-label">USERNAME</label>
                                    <input type="text" class="form-control-plaintext" id="username" name="username" placeholder="Enter your username here..." aria-describedby="issue-username">
                                    <div id="issue-username" class="form-text"></div>
                                </div>
                                <div class="mt-3">
                                    <label for="password" class="form-label">PASSWORD</label>
                                    <input type="password" class="form-control-plaintext" id="password" name="password" placeholder="Enter your password here..." aria-describedby="issue-password">
                                    <div id="issue-password" class="form-text"></div>
                                </div>
                                <button class="btn btn-primary w-100 mt-5">LOG IN</button>
                            </form>
                        </div>
                    </div>   
                </div>
                <div class="d-none d-sm-block col-sm-2 col-md-3 col-lg-4"></div>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
    name: 'Login',
    data(){
        return {
        }
    },
    methods: {
        async submitLogin(e){
            e.preventDefault()
            const data = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            }
            if (data.username && data.password){
                const response = await this.$http.post('/auth/', data,
                { headers: { Accept: 'application/json', 'Content-type': 'application/json'}})

                if (response.data['token']){
                    this.popup('success', 'Success.','Redirecting user to Parking System...')
                    localStorage.setItem('plotid',response.data['token'])
                    document.getElementById('username').value = ""
                    document.getElementById('password').value = ""
                    let router = this.$router
                    setTimeout(()=>{
                        router.push({ name: 'Dashboard'})
                    },1500)
                }  
                else{
                    this.popup('error', 'Error.',response.data['message'])
                }
            }
            else{
                this.popup('error', 'Error.','Please complete the fields required.')
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
}
</script>
