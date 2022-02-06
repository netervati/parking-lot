<template>
    <div class="row">
        <Menu />
        <div class="col-12">
            <h4><b v-text="moduleTitle"></b></h4>
        </div>
        <div class="col-12">
            <router-view></router-view>
        </div>
        <Footer />
    </div>
</template>

<script>
import Menu from '../../layout/menu.vue'
import Footer from '../../layout/footer.vue'

export default {
    name: 'User',
    components:{
        Menu,
        Footer
    },
    data(){
        return{
            moduleTitle: ''
        }
    },
    mounted(){
        this.moduleTitle = this.$route.matched[0].name
    }
}
</script>