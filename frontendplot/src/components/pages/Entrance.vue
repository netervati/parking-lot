<template>
    <div class="row">
        <Menu />

        <div class="col-12 mt-3">
            <div class="card">
                <div class="card-body registry">
                    <div class="table-responsive-sm overflow-x">
                        <table class="table table-sm table-condensed table-bordered">
                            <thead>
                                <tr class="text-center">
                                    <th>Actions</th>
                                    <th>Label</th>
                                    <th>Created On</th>
                                    <th>Updated On</th>
                                    <th>Created By</th>
                                    <th>Updated By</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Menu from '../layout/Menu.vue'

export default {
    name: 'Entrance',
    data(){
        return{
            moduleTitle: ''
        }
    },
    components:{
        Menu
    },
    mounted(){
        this.moduleTitle = this.$route.name
    }
}
</script>