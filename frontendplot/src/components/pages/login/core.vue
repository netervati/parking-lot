<template>
    <div class="row bg-main vh-100">
        <div class="col-12">
            <div class="row">
                <div class="d-none d-sm-block col-sm-2 col-md-3 col-lg-4"></div>
                <div class="col-12 col-sm-8 col-md-6 col-lg-4 mt-5">
                    <div class="card mt-5">
                        <div class="card-body p-4 shadow-sm">
                            <p class="text-center">Welcome to OOP Parking Lot!<br>Please sign in.</p>
                            <form v-on:submit="submitLogin($event)">
                                <div class="mt-4">
                                    <label for="username" class="form-label">Username</label>
                                    <input type="text" class="form-control" id="username" name="username" placeholder="Enter your username here..." aria-describedby="issue-username">
                                    <div id="issue-username" class="form-text"></div>
                                </div>
                                <div class="mt-3">
                                    <label for="password" class="form-label">Password</label>
                                    <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password here..." aria-describedby="issue-password">
                                    <div id="issue-password" class="form-text"></div>
                                </div>
                                <button id="btn-submit" class="btn btn-primary w-100 mt-5"><i class="bi bi-key"></i> Log in</button>
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
    methods: {
        async submitLogin(e){
            e.preventDefault()
            const formData = Object.fromEntries(new FormData(e.target));
            document.getElementById('btn-submit').disabled = true
            const router = this.$router

            if (!formData['username'] || !formData['password']) return this.popup('error', 'Error.','Please complete the fields required.', 1500)

            const response = await this.$http.post('/auth/', formData,
            { headers: { Accept: 'application/json', 'Content-type': 'application/json'}})

            if (!response.data['token']) return this.popup('error', 'Error.',response.data['message'], 1500)
            localStorage.setItem('plotid',response.data['token'])
            document.getElementById('username').value = ""
            document.getElementById('password').value = ""
            this.popup('success', 'Success.','Redirecting user to Parking System...', 1500)
            setTimeout(() => router.push({ name: 'Dashboard'}),1500)
        },
        popup(result, title, msg, timer){
            document.getElementById('btn-submit').disabled = false
            Swal.fire({
                icon: result,
                title: title,
                text: msg,
                timer: timer
            })
        },
    },
}
</script>
