<template>
    <div v-html="copyright" class="col-12 text-center mt-5 mb-5"></div>
</template>

<script>
    export default {
        name: 'Footer',
        data(){
            return{
                copyright: ''
            }
        },
        mounted(){
            let curYear = new Date().getFullYear()
            this.copyright =   `Copyright &copy; ${curYear} Ayala Corp.<br> Developed by Christopher I. Tabula`
        }
    }
</script>
