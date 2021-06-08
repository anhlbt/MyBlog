<template>
 <b-container id="similar-properties">
     <div v-swiper:mySwiper="swiperOption">
      <div class="similar-title">
          <h2 class="my-5">Similar Properties</h2>
            <span><b>{{ properties.items.length }}</b> suggested properties</span>
      </div>
    <div class="swiper-wrapper my-5">
      <div class="swiper-slide property-card p-2" v-for="(property, id) in properties.items" :key="id">
        <div class="wrap">
        <img width="250" height="200" :src="base_url+'/api/static/'+property.images[0]">
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
            <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="20" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor }}</b></p>
          </b-col>
          <b-col>
            <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="20" src="@/assets/images/icons/location.png" alt=""> <b>{{property.location }}</b></p>
            <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="20" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.rooms }}</b></p>
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
 </b-container>
  
</template>

<script>
import favorite from '../otherSections/favorite.vue';

  export default {
    components: {
      favorite,
    },

    data () {
      return {
        base_url: this.$axios.defaults.baseURL,
        properties: null,
   

        swiperOption: {
          loop: true,
          slidesPerView: '2',
          spaceBetween: 2,
          autoplay: false,
          pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true
          },

          autoplay: {
            delay: 6000,
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
      // getImage(path_image){

      //   const path = `/api/static/${path_image}`
      //   this.$axios.get(path).then((response) => {
      //   }).catch(error => console.log(error))
      // }

      
    },

    // Reload data when routing changes
    created () {
      this.getPosts()
    },

  }
</script>


<style lang="scss" scoped>
  .similar-title {
          display: flex;
          align-items: center;
          justify-content: space-between;
      }

 
</style>