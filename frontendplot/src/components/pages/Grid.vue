<template>
    <div class="row">
        <nav class="navbar navbar-light bg-light shadow-sm">
            <form>
                <button id="plotEntry" :class="toolClass('plotEntry')" v-on:click="activateTool('plotEntry')" :disabled="cursorSearching==true" type="button"><b><i class="fas fa-door-open"></i> Plot Entry</b></button>
                <button id="deleteEntry" :class="toolClass('deleteEntry')" v-on:click="activateTool('deleteEntry')" :disabled="cursorSearching==true" type="button"><b><i class="fas fa-times"></i> Delete Entry</b></button>
                <button id="plotSlot" :class="toolClass('plotSlot')" v-on:click="activateTool('plotSlot')" :disabled="cursorSearching==true" type="button"><b><i class="fas fa-th-large"></i> Plot Slot</b></button>
                <button id="deleteSlot" :class="toolClass('deleteSlot')" v-on:click="activateTool('deleteSlot')" :disabled="cursorSearching==true" type="button"><b><i class="fas fa-eraser"></i> Delete Slot</b></button>
            </form>
        </nav>
        <div id="lot-canvas" class="col-lg-12 table-responsive">
            <canvas class="mt-5" id="lot-grid" :width="canvasWidth" :height="canvasHeight"></canvas>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Home',
    data(){
        return {
            canvasWidth: 1280, //64 * 20
            canvasHeight: 640, //64 * 10
            gridSize: 64,
            fontSize: 32,
            toolOptions: {
                plotEntry: false,
                deleteEntry: false,
                plotSlot: false,
                deleteSlot: false,
            },
            toolActive: false,
            cursorSearching: false
        }
    },
    methods:{
        activateTool(id){
            let toolOptions = this.toolOptions
            for (let [key] of Object.entries(toolOptions)){
                if (key != id){
                    toolOptions[key] = false
                }   
            }
            this.toolOptions[id] = !this.toolOptions[id]
            this.toolActive = this.toolOptions[id]
        },
        toolClass(id){
            if (this.toolOptions[id] == true){
                return "btn tool-option active"
            }
            else{
                return "btn tool-option"
            }
        },
        async retrieveData(){
            const response = await this.$http.get("parking",
                {
                headers: {
                    Accept: "application/json",
                    "Content-type": "application/json"
                    }   
                }
            )
            this.entrance = response.data.entrance
            this.slot = response.data.slot
            this.renderParking()
        },
        async renderParking(){
            let entrance = this.entrance
            let slot = this.slot
            let gridSize = this.gridSize
            let fontSize = this.fontSize
            let fontXPos = fontSize / 2
            let fontYPos = fontSize * 1.25
            this.lotContext.clearRect(0,0,this.canvasWidth,this.canvasHeight)

            for (let y = 0, yTotal = this.canvasHeight; y < yTotal; y++){
                for (let x = 0, xTotal = this.canvasWidth; x < xTotal; x++){
                    let gridX = x * gridSize
                    let gridY = y * gridSize

                    this.lotContext.beginPath()
                    this.lotContext.lineWidth = 1;
                    this.lotContext.strokeStyle = '#ADA7A7';
                    this.lotContext.rect(gridX, gridY, gridSize, gridSize)
                    this.lotContext.stroke()
                }
            }

            for (let entry in entrance){
                let entryX = entrance[entry][0] * this.gridSize + fontXPos
                let entryY = entrance[entry][1] * this.gridSize + fontYPos
                this.lotContext.fillStyle = '#212529';
                this.lotContext.fillText('\uf52b', entryX, entryY);
            }

            for (let point in slot){
                let entryX = slot[point][0] * this.gridSize + fontXPos
                let entryY = slot[point][1] * this.gridSize + fontYPos
                // let slotSize = slot[point][2]
                let occupied = slot[point][3]
                this.lotContext.fillStyle = occupied == '0' ? 'green' : 'red';
                this.lotContext.fillText('\uf009', entryX, entryY);
            }
        },
        async getCursorPosition(event) {
            this.cursorSearching = true
            let rect = this.lotCanvas.getBoundingClientRect();
            let x = Math.floor((event.clientX - rect.left) / this.gridSize);
            let y = Math.floor((event.clientY - rect.top) / this.gridSize);
            let entrance = this.entrance
            let slot = this.slot
            let getEntrance = null
            let getSlot = null
            let reloadRender = false
            for (let entry in entrance){
                if  (entrance[entry][0] == x){
                    if (entrance[entry][1] == y){
                        getEntrance = {}
                        getEntrance.id = entry
                        getEntrance.data = entrance[entry]
                        break
                    }
                }
            }

            for (let point in slot){
                if  (slot[point][0] == x){
                    if (slot[point][1] == y){
                        getSlot = slot[point]
                        break
                    }
                }
            }

            if (this.toolOptions.plotEntry == true){
                if (!getEntrance){
                    this.entrance['D'] = [x,y]
                    reloadRender = true
                }
            }
            else if (this.toolOptions.deleteEntry == true){
                if (getEntrance){
                    delete this.entrance[getEntrance.id]
                    reloadRender = true
                }
            }
            else{
                if (getEntrance){
                    console.log(getEntrance)
                }
                if (getSlot){
                    console.log(getSlot)
                }
            }

            if (reloadRender == true){
                await this.renderParking()
                this.cursorSearching = false
            }
            else{
                this.cursorSearching = false
            }
        },
        setCanvas(){
            this.lotCanvas = document.getElementById('lot-grid')
            this.lotContext = this.lotCanvas.getContext('2d')
            this.lotContext.font = `600 ${this.fontSize}px "Font Awesome 5 Free"`;
            let component = this
            this.lotCanvas.addEventListener('mousedown', function(e) {
                if (component.cursorSearching == false){
                    component.getCursorPosition(e)
                }
            })
            setTimeout(()=>{
                this.retrieveData()
            },5)
        }
    },
    mounted(){
        this.setCanvas()
    }
}
</script>

<style scoped>
    #lot-canvas{
        height: 85vh;
        background-color: #F0F0F0;
    }
    .tool-option{
        transition: 0.5s background-color;
    }
    .tool-option:hover{
        background-color: rgb(218, 218, 218);
    }
    .tool-option.active{
        background-color: rgb(218, 218, 218);
    }
</style>