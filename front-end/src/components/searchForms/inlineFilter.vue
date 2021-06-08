<template>
    <div>
        <div id="search-card">
          <b-container>
             <b-form @submit="getSearchProperties" @reset="onReset">
               <b-row align-v="center" class="mb-3">
                 <b-col cols="12" md="4">
                  <b-form-group>
                    <b-form-radio-group
                      id="btn-radios-2" v-model="searchForm.purpose" :options="purposes"
                      buttons button-variant="outline-primary"
                      name="radio-btn-outline"></b-form-radio-group>
                  </b-form-group>              
                                
                 </b-col>
                  <b-col cols="12" md="6">

                  </b-col>

                  <b-col cols="12" md="2">
                      <b-button class="float-right" variant="light" v-b-tooltip.hover title="Reset filter" small type="reset" ><img width="30" src="@/assets/images/reset.png"></b-button>
                      <b-button variant="light" v-b-tooltip.hover title="Advance filter" small @click="openFilter"><img width="30" src="@/assets/images/filter.png"></b-button>
                  </b-col>
               </b-row>
               <b-row align-v="center">
                  <b-col cols="8">
                    <select-group :town="false" @values="regionChange" v-model="searchForm.selected"></select-group>  
                  </b-col>
                  <b-col cols="4" md="4">
                    <b-form-group id="input-group-7">
                      <b-form-select id="input-4" v-model="searchForm.type" :options="types" required
                      ></b-form-select>
                    </b-form-group>
                  </b-col>
               </b-row>
               
              
              <transition name="fade" mode="out-in">
                  <div class="advance-filter" v-if="filterOpen">
                      <label for="range-2">Price range: <b>0 - {{searchForm.price}} tỷ (VND)</b></label>
              <b-form-input class="my-3" id="range-2" v-model="searchForm.price" type="range" min="1" max="50" step="1"></b-form-input>
                      
                         <b-row>
                           <b-col cols="12" md="6">
                             <b-form-group id="input-group-5">
                               <b-form-select id="input-5" v-model="searchForm.floor" :options="floors"
                              ></b-form-select>
                            </b-form-group>
                           </b-col>
                           <b-col cols="12" md="6">
                              <b-form-group id="input-group-6">
                                <b-form-select id="input-6" v-model="searchForm.bedroom" :options="rooms"
                                ></b-form-select>
                              </b-form-group>
                           </b-col>
                         </b-row>

                        <b-row>
                          <b-col cols="12" md="6">
                            <b-form-group id="input-group-7">
                              <b-form-select id="input-7" v-model="searchForm.agency" :options="agencies"></b-form-select>
                            </b-form-group>
                          </b-col>
                          <b-col cols="12" md="6">
                            <b-form-group id="input-group-8">
                              <b-form-select id="input-8" v-model="searchForm.direction" :options="directions"
                              ></b-form-select>
                            </b-form-group>
                          </b-col>
                        </b-row> 
              
                      <b-form-group label="Property features" id="input-group-9">
                        <b-form-checkbox-group v-model="searchForm.features" id="checkboxes-9">
                          <b-form-checkbox value="parking">Parking</b-form-checkbox>
                          <b-form-checkbox value="garage">Garage</b-form-checkbox>
                          <b-form-checkbox value="yard">Yard</b-form-checkbox>
                          <b-form-checkbox value="barbeque">Barbeque</b-form-checkbox>
                          <b-form-checkbox value="airconditioning">Air conditioning</b-form-checkbox>
                          <b-form-checkbox value="videosurveillance">Video surveilance</b-form-checkbox>
                          <b-form-checkbox value="terrace">Terrace</b-form-checkbox>
                          <b-form-checkbox value="centralheating">Central Heating</b-form-checkbox>
                        </b-form-checkbox-group>
                      </b-form-group>
                    </div>
              </transition>       
              <!--End Advance Filter-->
              <b-button class="btn-outline-style1 mt-3" block type="submit" >Search</b-button>
            </b-form>
          </b-container>
        </div>
    </div>
</template>


<script>
import SelectGroup from "../v-region/SelectGroup"
  export default {
    components:{
      SelectGroup,
    },
    props:{
      searchForm: {
       type: Object,
       value: null
       }

    },
     
        
    data() {
      return {

        properties: null,
        filterOpen: false,
        purposes: [
          { text: 'For Sale', value: 'Sale' },
          { text: 'For Rent', value: 'Rent' },
          
        ],
        filterForm: {

          selected: null,        
          province: "",
          district: "",
          ward: "",
          area: null,
          type: null,
          purpose: "Sale",
          floor: null,
          bedroom: null,
          bathroom: null,
          agency: null,
          agent: null,
          checked: [],
          features: [],
          price: "",
          address: null,
          direction: null,
        },

        types: [{ text: 'Select property type', value: null }, 'Apartment', 'Studio', 'House', 'Commercial', 'Land', 'Office'],
        floors: [{ text: 'Select floor', value: null }, 'Ground floor', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '10/10'],
        rooms: [{ text: 'Select rooms number', value: null }, '1', '2', '3', '4', '5', '6', '7', '8', 'more than 8'],
        agencies: [{ text: 'Select agency', value: null }, 'Nuxt Agency', 'Vue Agency', 'JS Agency', 'Bootstratp Agency'],
        agents: [{ text: 'Select agent', value: null }, 'James', 'Martin', 'Maria', 'Andrew'],
        directions: [{text: 'Select direction', value: null}, 'Đông', 'Tây', "Nam", "Bắc", "Đông-Bắc", "Tây-Bắc", "Đông-Nam", "Tây-Nam", "Khác"],

        show: true
      }
    },
    // computed: {

    // },
    methods: {

      regionChange(data) {
        // console.log(data)
        this.searchForm.address = [data.area, data.city, data.province].map(function (e) {return (e != null? e.value :"");}).join(", "); 
        data.province != null? this.searchForm.province = data.province.value : this.searchForm.province = null
        data.city != null? this.searchForm.district = data.city.value : this.searchForm.district = null
        data.area!= null ? this.searchForm.ward = data.area.value : this.searchForm.ward = null
        
      },      
      openFilter() {
        this.filterOpen = !this.filterOpen
      },
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.searchForm))
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.searchForm.email = ''
        this.searchForm.area = null
        this.searchForm.type = null
        this.searchForm.floor = null
        this.searchForm.room = null
        this.searchForm.agency = null
        this.searchForm.agent = null
        this.searchForm.checked = []
        this.searchForm.features = []
        this.searchForm.price = 0
        this.searchForm.direction = null
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },

      getSearchProperties(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.searchForm))
        if(typeof this.searchProperties != 'undefined')
        {
            // this.form = this.searchForm
            this.searchForm = Object.assign({}, this.searchProperties)
            
        }   
        // console.log("this.form", this.searchForm)     
        const path = '/api/properties_area/'
        const payload = {
              province: this.searchForm.province,
              district: this.searchForm.district,
              ward: this.searchForm.ward,
              type: this.searchForm.type,
              purpose: this.searchForm.purpose,
              floor: this.searchForm.floor,
              bedroom: this.searchForm.bedroom,
              bathroom: this.searchForm.bathroom,
              agency: this.searchForm.agency,
              agent: this.searchForm.agent,
              checked: this.searchForm.checked,
              features: this.searchForm.features,
              price: this.searchForm.price,
              address: this.searchForm.address,
              direction: this.searchForm.direction,
        }
        this.$axios.post(path, payload)
          .then((response) => {
            // handle success
            this.properties = response.data
            this.$toasted.success('Successed search ...', { icon: 'fingerprint' })
            this.changeProperties(evt)
          })
          .catch((error) => {
            // handle error
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
          })

      },   

      // can call in button event @click="changeProperties"
      changeProperties(event) {
        // this.$emit('toPropertiesFullWidth', this.childMessage)
        this.$emit('toPropertiesFullWidth', this.properties)
    },

    },
    
    // created()
    // {
    //   console.log("this.searchForm", this.searchForm)
    //   if(typeof this.searchForm.type != 'undefined')
    //   {
    //     // this.form = this.searchForm
    //     this.filterForm = Object.assign({}, this.searchForm)
    //     // console.log("this.filterForm", this.filterForm)
    //   } 
    // },

    

  }
</script>


<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
@import "./../../assets/scss/main";
  #search-card {
    margin: 65px 0;
    background: $color1-light;
    padding: 30px 0;
  }

 .fade-enter-active, .fade-leave-active {
  transition: opacity .3s ease;
  }
.fade-enter, .fade-leave-to {
  opacity: .4;
}
</style>