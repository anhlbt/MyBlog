<template>
  <!-- You can find this swiper instance object in current component by the "mySwiper"  -->
  <div class="my-5" id="week-deal" v-swiper:mySwiper="swiperOption">
    <h2 class="my-5">Deals of the week</h2>
    <div class="swiper-wrapper my-5">
      <div class="swiper-slide week-deal-card" v-for="(property, id) in properties.items" :key="id">
        <div class="wrap">
            <b-row>
                <b-col cols="12" md="6">
                    <img width="550" :src="base_url+'/api/static/'+property.images[0]">
                    <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
                    <span class="type-badge">{{property.type }}</span>
                    <span class="contract-badge">{{property.purpose }}</span>
                </b-col>
                <b-col cols="12" md="6">
                   <favorite 
                    :title="property.title"
                    :image="base_url+'/api/static/'+property.images[0]"
                    :id="property.id"
                  />
                    <router-link class="property-title" v-bind:to="{ name: 'PropertyDetail', params: { id: property.id } }">
                      <h5 class="my-2">{{ property.title }}</h5>
                    </router-link>
                    <h4 class="text-left pl-3 mb-3"><b>{{ property.price }}</b></h4>
                     <b-row class="promoted-property-info text-left">
                    <b-col class="ml-2">
                      <p v-b-tooltip.hover title="Property Type"><img class="mr-3" width="30" src="@/assets/images/icons/building.png" alt=""> <b>{{property.type }}</b></p>
                      <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="30" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor_plan }}</b></p>
                    </b-col>
                    <b-col>
                       <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="30" src="@/assets/images/icons/location.png" alt=""> <b>{{property.area }}</b></p>
                      <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="30" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.bedroom }}</b></p>
                    </b-col>
                </b-row>
                 <router-link class="property-title" v-bind:to="{ name: 'PropertyDetail', params: { id: property.id } }">
                <b-button class="btn-outline-style1 mt-5" block type="submit" >More details</b-button>
                </router-link>
                </b-col>
            </b-row>
        </div>
      </div>
    </div>
        <div class="swiper-button-prev" slot="button-prev"></div>
        <div class="swiper-button-next" slot="button-next"></div>
  </div>
</template>

<script>
import favorite from '@/components/otherSections/favorite.vue';
  export default {
    components: {
      favorite,
    },

    data () {
      return {
        properties: "",
        base_url: this.$axios.defaults.baseURL,


        swiperOption: {
          loop: true,
          slidesPerView: '1',
          spaceBetween: 45,
          autoplay: false,

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
          },
            controller: {
            inverse: true,
          },
          breakpoints: {
              768: {
                  slidesPerView: 1,
                  spaceBetween: 10
              },
              675: {
                  slidesPerView: 1,
                  spaceBetween: 20
              }
          }
         
        }
      }
    },

    methods: {

      getPosts () {
        let page = 1
        let per_page = 10
        if (typeof this.$route.query.page != 'undefined') {
          page = this.$route.query.page
        }

        if (typeof this.$route.query.per_page != 'undefined') {
          per_page = this.$route.query.per_page
        }
        //get all post
        //const path = `/api/posts/?page=${page}&per_page=${per_page}`
        const path = `/api/properties/`
        this.$axios.get(path)
          .then((response) => {
            // handle success
            this.properties = response.data
          })
          .catch((error) => {
            // handle error
            this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
          })
      },
    },

    
    // Reload data when routing changes
    created () {
      this.getPosts()
    },
  }
</script>


<style lang="scss" scoped>
    #week-deal {
        padding: 0 10px;
        margin: 0 20px;
    }
</style>