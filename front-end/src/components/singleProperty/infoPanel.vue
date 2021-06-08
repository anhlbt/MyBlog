<template>
    <div>
        <b-row class="property-info-panel" id="more-info"> 
            <b-col cols="12" md="4">
                 <b-button v-b-modal.modal-video class="btn-outline-style2"><i class="fa fa-play"></i> Property Video</b-button>

                <b-modal id="modal-video" size="lg" hide-footer>
                     <video autoplay="true" muted controls infinite>
                        <source src="@/assets/videos/imobiliare.mp4" >
                    </video>
                </b-modal>
            </b-col>
            <b-col cols="12" md="4">
                 <b-button v-b-modal.modal-agent class="btn-outline-style2"><i class="fa fa-envelope"></i> Contact Agent</b-button>

                <b-modal id="modal-agent" centered title="Contact property agent" hide-footer>
                    <contact />
                </b-modal>
            </b-col>
            <b-col cols="12" md="4">
                 <b-button class="btn-outline-style2"><i class="fa fa-file"></i> Download PDF</b-button>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import contact from '@/components/Agents/contact.vue';
    export default {
        components: {
            contact
        }
    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
   .property-info-panel {
       position: sticky;
       top: 0;
       background: $color1-light;
       padding: 20px 0;

       .btn-outline-style1 {
           border-radius: 0;
       }
   }

   @media(max-width: 768px) {
       .property-info-panel {
           div {
               text-align: center;
               button{
                   margin: 10px auto;
               }
           }
       }
   }
</style>