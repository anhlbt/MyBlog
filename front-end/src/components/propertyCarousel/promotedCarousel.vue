<template>
 
  <div v-swiper:mySwiper="swiperOption">
    <h2 class="my-5">Promoted properties</h2>
    <div class="swiper-wrapper my-5">
      <div class="swiper-slide property-card" v-for="(property, id) in properties.items" :key="id">
        <div class="wrap">
        <img width="250" height="220" :src="base_url+'/api/static/'+property.images[0]"> <!-- property.images.slice(0)-->
        <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
        <span class="type-badge">{{property.type }}</span>
        <span class="contract-badge">{{property.purpose }}</span>
        <favorite 
          :title="property.title"
          :image="base_url+'/api/static/'+property.images[0]"
          :id="property.id"
        />
          <router-link class="property-title" v-bind:to="{ name: 'PropertyDetail', params: { id: property.id } }">
              <h5 class="my-2">{{ property.title }}</h5>
          </router-link>
        <h4 class="text-left pl-3"><b>{{ property.price }}</b></h4>
        <hr>
        <b-row class="promoted-property-info text-left">
          <b-col>
            <p v-b-tooltip.hover title="Property Type"><img class="mr-3" width="20" src="@/assets/images/icons/building.png" alt=""> <b>{{property.type }}</b></p>
            <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="20" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor_plan }}</b></p>
          </b-col>
          <b-col>
            <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="20" src="@/assets/images/icons/location.png" alt=""> <b>{{property.area }}</b></p>
            <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="20" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.bedroom }}</b></p>
          </b-col>
        </b-row>
        <router-link class="property-title" v-bind:to="{ name: 'PropertyDetail', params: { id: property.id } }">
        
        <b-button class="btn-outline-style1 mt-3" block type="submit" >More details</b-button>
        </router-link>
        </div>
      </div>
    </div>
    <div class="swiper-pagination swiper-pagination-bullets"></div> 
  </div>
</template>

<script>
import favorite from '../otherSections/favorite.vue';

// import style (>= Swiper 6.x)
import 'swiper/swiper-bundle.css'

  export default {
    components: {
      favorite,
    },

    data () {
      return {
        properties: null,
        base_url: this.$axios.defaults.baseURL,


        swiperOption: {
          loop: true,
          slidesPerView: '4',
          centeredSlides: false,
          spaceBetween: 5,
          autoplay: false,
          pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true
          },

          autoplay: {
            delay: 6000,
          },

            controller: {
            inverse: true,
          },

           breakpoints: {
              1024: {
                  slidesPerView: 3,
                  loopedSlides: 3,
                  spaceBetween: 10
              },
              768: {
                  slidesPerView: 2,
                  loopedSlides: 2,
                  spaceBetween: 10
              },
              675: {
                  slidesPerView: 1,
                  loopedSlides: 1,
                  spaceBetween: 5
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
            console.log(error.response.data)
            this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
          })
      },

      getPost (id) {
        if (typeof id == String){
                id = Number(id)}
        let q = this.$route.query.q
        let page = 1
        let per_page = 20
        let path
        if (typeof this.$route.query.page != 'undefined') {
            page = this.$route.query.page
        }

        if (typeof this.$route.query.per_page != 'undefined') {
            per_page = this.$route.query.per_page
        }
        
        if (typeof q != 'undefined') {
            path = `/api/search/property-detail/${id}?q=${q}&page=${page}&per_page=${per_page}`
        } else {
            path = `/api/properties/${id}`
        }

        this.$axios.get(path)
            .then((response) => {
            // handle success
            this.property = response.data
            })
            .catch((error) => {
            // handle error
            console.error(error)
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
@import "./../../assets/scss/main";

  .promoted-property-info {
    b {
      font-size: 14px;
    }
  }
</style>