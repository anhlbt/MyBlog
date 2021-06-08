<template>
    <div>
        <div id="search-card" class="card-transparent">
          <h3 class="text-center py-3">Find what you wish</h3>
            <b-form @reset="onReset" >
            <b-form-group>
              <b-form-radio-group
                id="btn-radios-2" v-model="form.purpose" :options="purposes"
                buttons button-variant="outline-primary"
                name="radio-btn-outline"></b-form-radio-group>
            </b-form-group>              
              <select-group :town="false" @values="regionChange" v-model="form.selected"></select-group>
              <b-form-group id="input-group-3">
                <b-form-input type="text" id="input-3" v-model="form.address" required></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-4"><b-form-select id="input-4" v-model="form.type" :options="types" required></b-form-select>
              </b-form-group>
              <label for="range-2">Price range: <b>1 - {{form.price}} tỷ (VND)</b></label>
              <b-form-input id="range-2" v-model="form.price" type="range" min="1" max="50" step="1"></b-form-input>

              <!--Advance Filter-->

              <b-button variant="light" v-b-tooltip.hover title="Advance filter" small @click="openFilter"><img width="30" src="@/assets/images/filter.png"></b-button>
              <transition name="fade" mode="out-in">
                  <div class="advance-filter" v-if="filterOpen">
                      <b-form-group id="input-group-5">
                          <b-form-select id="input-5" v-model="form.floor" :options="floors"></b-form-select>
                      </b-form-group>

                      <b-form-group id="input-group-6">
                        <b-form-select id="input-6" v-model="form.bedroom" :options="rooms"></b-form-select>
                      </b-form-group>

                      <b-form-group id="input-group-7">
                        <b-form-select id="input-7" v-model="form.agency" :options="agencies"></b-form-select>
                      </b-form-group>

                      <b-form-group id="input-group-8">
                        <b-form-select id="input-8" v-model="form.direction" :options="directions"></b-form-select>
                      </b-form-group>
                      <b-form-group label="Property features" id="input-group-9">
                        <b-form-checkbox-group v-model="form.features" id="checkboxes-9">
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


              <b-button class="float-right" variant="light" v-b-tooltip.hover title="Reset filter" small type="reset" ><img width="30" src="@/assets/images/reset.png"></b-button>
              
              <router-link v-bind:to="{ name: 'propertiesFullWidth', params: { searchProperties: form} }">
                <b-button class="btn-outline-style1 mt-3" block type="submit" >Search</b-button>
              </router-link>
          </b-form>
        </div>
    </div>
</template>


<script>
import SelectGroup from "../v-region/SelectGroup"
import propertiesFullWidth from "../pages/propertiesFullWidth"
  export default {
    components: {
        SelectGroup,
        propertiesFullWidth,

      },
    data() {
      return {


        purposes: [
          { text: 'For Sale', value: 'Sale' },
          { text: 'For Rent', value: 'Rent' },
          
        ],

        properties: null,
        filterOpen: false,
        
        form: {

          selected: {
            province: '',
            city: '',
            area: '',
            town: ''
          },          
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
          direction:null,
        },
        types: [{ text: 'Select property type', value: null }, 'Apartment', 'Studio', 'House', 'Commercial', 'Land', 'Office'],
        floors: [{ text: 'Select floor', value: null }, 'Ground floor', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '10/10'],
        rooms: [{ text: 'Select rooms number', value: null }, '1', '2', '3', '4', '5', '6', '7', '8', 'more than 8'],
        agencies: [{ text: 'Select agency', value: null }, 'Nuxt Agency', 'Vue Agency', 'JS Agency', 'Bootstrap Agency'],
        agents: [{ text: 'Select agent', value: null }, 'James', 'Martin', 'Maria', 'Andrew'],
        directions: [{text: 'Select direction', value: null}, 'Đông', 'Tây', "Nam", "Bắc", "Đông-Bắc", "Tây-Bắc", "Đông-Nam", "Tây-Nam", "Khác"],

        show: true
      }
    },
    methods: {
      regionChange(data) {
        // console.log(data)
        this.form.address = [data.area, data.city, data.province].map(function (e) {return (e != null? e.value :"");}).join(", "); 
        data.province != null? this.form.province = data.province.value : this.form.province = null
        data.city != null? this.form.district = data.city.value : this.form.district = null
        data.area!= null ? this.form.ward = data.area.value : this.form.ward = null
      },
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.area = null
        this.form.type = null
        this.form.floor = null
        this.form.bedroom = null
        this.form.agency = null
        this.form.agent = null
        this.form.checked = []
        this.form.features = []
        this.form.price = 0
        this.form.direction = null
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },
      openFilter() {
        this.filterOpen = !this.filterOpen
      }
    }
  }
</script>


<style lang="scss" scoped>
@import "./../../assets/scss/main";
  #search-card {
    margin-top: 50px;
  }

 .fade-enter-active, .fade-leave-active {
  transition: opacity .3s ease;
}
.fade-enter, .fade-leave-to {
  opacity: .4;
}

</style>