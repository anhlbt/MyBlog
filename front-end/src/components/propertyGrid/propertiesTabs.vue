<template>
    <div id="properties-grid">
         <b-card no-body class="my-5">
            <b-tabs fill>
            <b-tab title="Apartments" active>
                <b-row>
                    <b-col class="my-3" cols="12" md="4" v-for="(property, id) in properties.items" :key="id">
                        <div class="property-grid-card">
                        <div class="wrap">
                            <img width="320" :src="base_url+'/api/static/'+property.images[0]">
                            <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
                            <span class="type-badge">{{property.type }}</span>
                            <span class="contract-badge">{{property.purpose }}</span>
                            <favorite 
                            :title="property.title"
                            :image="base_url+'/api/static/'+property.images[0]"
                            :id="property.id"
                          />
                            <router-link :to="`/properties/${property.id}`">
                            <h5 class="my-2 property-title">{{ property.title }}</h5>
                            </router-link>
                            <h4 class="text-left pl-3"><b>{{ property.price }}</b></h4>
                            <hr>
                            <b-row class="promoted-property-info text-left">
                            <b-col class="ml-2">
                                <p v-b-tooltip.hover title="Property Type"><img class="mr-3" width="20" src="@/assets/images/icons/building.png" alt=""> <b>{{property.type }}</b></p>
                                <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="20" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor_plan }}</b></p>
                            </b-col>
                            <b-col>
                                <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="20" src="@/assets/images/icons/location.png" alt=""> <b>{{property.area }}</b></p>
                                <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="20" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.bedroom }}</b></p>
                            </b-col>
                            </b-row>
                            <b-button class="btn-outline-style1 mt-3" block type="submit" >More details</b-button>
                        </div>
                      </div>  
                    </b-col>
                </b-row>
            </b-tab>
            <b-tab title="Studios">
                 <b-row>
                    <b-col class="my-3" cols="12" md="4" v-for="(property, id) in properties.items" :key="id">
                        <div class="wrap">
                        <div class="property-grid-card">
                            <img width="320" :src="base_url+'/api/static/'+property.images[0]">
                            <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
                            <span class="type-badge">{{property.type }}</span>
                            <span class="contract-badge">{{property.purpose }}</span>
                            <favorite 
                              :title="property.title"
                              :image="base_url+'/api/static/'+property.images[0]"
                              :id="property.id"
                            />
                            <router-link :to="`/properties/${property.id}`">
                            <h5 class="my-2 property-title">{{ property.title }}</h5>
                            </router-link>
                            <h4 class="text-left pl-3"><b>{{ property.price }}</b></h4>
                            <hr>
                            <b-row class="promoted-property-info text-left">
                            <b-col class="ml-2">
                                <p v-b-tooltip.hover title="Property Type"><img class="mr-3" width="20" src="@/assets/images/icons/building.png" alt=""> <b>{{property.type }}</b></p>
                                <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="20" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor_plan }}</b></p>
                            </b-col>
                            <b-col>
                                <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="20" src="@/assets/images/icons/location.png" alt=""> <b>{{property.area }}</b></p>
                                <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="20" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.bedroom }}</b></p>
                            </b-col>
                            </b-row>
                            <b-button class="btn-outline-style1 mt-3" block type="submit" >More details</b-button>
                        </div>
                      </div>  
                    </b-col>
                </b-row>
            </b-tab>
            <b-tab title="Houses">
                <b-row>
                    <b-col class="my-3" cols="12" md="4" v-for="(property, id) in properties.items" :key="id">
                        <div class="wrap">
                            <div class="property-grid-card">
                            <img width="320" :src="base_url+'/api/static/'+property.images[0]">
                            <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
                            <span class="type-badge">{{property.type }}</span>
                            <span class="contract-badge">{{property.purpose }}</span>
                            <favorite 
                              :title="property.title"
                              :image="base_url+'/api/static/'+property.images[0]"
                              :id="property.id"
                            />
                            <router-link :to="`/properties/${property.id}`">
                            <h5 class="my-2 property-title">{{ property.title }}</h5>
                            </router-link>
                            <h4 class="text-left pl-3"><b>{{ property.price }}</b></h4>
                            <hr>
                            <b-row class="promoted-property-info text-left">
                            <b-col class="ml-2">
                                <p v-b-tooltip.hover title="Property Type"><img class="mr-3" width="20" src="@/assets/images/icons/building.png" alt=""> <b>{{property.type }}</b></p>
                                <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="20" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor_plan }}</b></p>
                            </b-col>
                            <b-col>
                                <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="20" src="@/assets/images/icons/location.png" alt=""> <b>{{property.area }}</b></p>
                                <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="20" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.bedroom }}</b></p>
                            </b-col>
                            </b-row>
                             <router-link class="property-title" :to="`/properties/${property.id}`">
                            <b-button class="btn-outline-style1 mt-3" block type="submit" >More details</b-button>
                            </router-link>
                        </div>
                      </div>  
                    </b-col>
                </b-row>
            </b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>

<script>
import favorite from '@/components/otherSections/favorite.vue';

export default {
  components: {
    favorite,
  },
  data() {
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
  },

  // Reload data when routing changes
  created () {
    this.getPosts()
  },
  // Reload data when routing changes
  beforeRouteUpdate (to, from, next) {
    next()
    this.getPost()

    if (to.params.id != from.params.id) {  // For the same article, when you click TOC to jump to all levels of headings, do not clear the TOC
      $('#toc').html('')  // Switch between different articles (click on the previous/next article), if the article content does not have markdown that needs to be parsed, you need to clear the TOC of the article on the previous route, otherwise it will remain
    }
  },  

}
</script>

<style lang="scss" scoped>
    .property-grid-card {
        .wrap {
            padding: 10px;
        }
    }
</style>