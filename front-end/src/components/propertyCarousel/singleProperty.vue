<template>
    <div>
        <b-container fluid class="single-property-slide">
            <b-row>
                <b-col cols="12" md="6">
                    <div class="my-5" v-swiper:mySwiper="swiperOption">
                        <div class="swiper-wrapper" >
                            <div class="swiper-slide" v-for="(img, id) in property.images" :key="id">
                                <div class="wrap">
                                    <img :src="base_url+'/api/static/'+img" alt="" height="500" width="100%">
                                </div>
                            </div>
                        </div>
                            <div class="swiper-button-prev" slot="button-prev"></div>
                            <div class="swiper-button-next" slot="button-next"></div>
                    </div>
                    
                    <div class="property-info">
                        <h2 class="my-5">Property ID {{id}}</h2>
                        <h1>{{ property.title }}</h1>
                        <h4>{{ property.price }}</h4>  
                    </div>  
                </b-col>

                <b-col cols="12" md="6" class="mt-5">
                    <b-row class="property-main-info">
                        <div class="quick-features">
                            <a href="#request-tour" class="btn-outline-style1">Request tour</a>
                            <a href="#more-info" class="btn-outline-style1">More info</a>
                            <a href="#similar-properties" class="btn-outline-style1">Similar properties</a>
                            <favorite 
                             :title="property.title"
                            :image="base_url+'/api/static/'+property.images[0]"
                            :id="property.id"
                            />

                            <div id="like-property" class="row">
                                <div class="col-lg-4">
                                <button v-on:click="onLikeOrUnlikePost(property)" v-bind:class="btnOutlineColor" class="btn btn-block g-rounded-50 g-py-12 g-mb-10">
                                    <i class="icon-heart g-pos-rel g-top-1 g-mr-5"></i> like<span v-if="property.likers_id && property.likers_id.length > 0"> | {{ property.likers_id.length }}</span>
                                </button>
                                </div>
                                <div class="col-lg-8">
                                <ul v-if="property.likers" class="list-inline mb-0">
                                    <li class="list-inline-item"
                                    v-for="(liker, index) in property.likers" v-bind:key="index">
                                    <router-link
                                        v-bind:to="{ path: `/user/${liker.id}` }"
                                        v-bind:title="liker.name || liker.username">
                                        <img class="g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3" v-bind:src="liker.avatar" v-bind:alt="liker.name || liker.username">
                                    </router-link>
                                    </li>
                                </ul>
                                </div>
                            </div>  

                        </div>
                    </b-row>
                    <b-row class="property-main-info mt-5">
                        <b-col cols="12" md="6">
                            <div class="property-details">
                                <p v-b-tooltip.hover title="Property Type"><img class="mr-3" width="40" src="@/assets/images/icons/building.png" alt=""> <b>{{property.type }}</b></p>
                                <p v-b-tooltip.hover title="Property Floor"><img class="mr-3" width="40" src="@/assets/images/icons/floor.png" alt=""> <b>{{property.floor_plan }}</b></p>
                                <p v-b-tooltip.hover title="Property Location"><img class="mr-3" width="40" src="@/assets/images/icons/location.png" alt=""> <b>{{property.area }}</b></p>
                                <p v-b-tooltip.hover title="Property Rooms"><img class="mr-3" width="40" src="@/assets/images/icons/rooms.png" alt=""> <b>{{property.bedroom }}</b></p>
                                <p v-b-tooltip.hover title="Property Agency"><img class="mr-3" width="40" src="@/assets/images/icons/agency.png" alt=""> <b>{{property.agency_id }}</b></p>
                            </div>
                        </b-col>
                        <b-col cols="12" md="6">
                            <h5 class="mb-5">Property Extra Features</h5>
                            <div v-for="(singleFeature, id) in property.features" :key="id">
                                <p><img class="mr-3" width="30" src="@/assets/images/icons/check.png" alt=""><b>{{ singleFeature }}</b></p>
                            </div>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import store from './../../store'
import favorite from '../otherSections/favorite.vue';

    export default {
        props: {
                id: Number,
                title: String,
        },
        components: {
            favorite,
        },

        data() {
            return {
                sharedState: store.state,
                comments: '',
                showToc: true,
                base_url: this.$axios.defaults.baseURL,
               swiperOption: {
                loop: true,
                slidesPerView: '1',
                spaceBetween: 25,
                autoplay: true,

                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev'
                },
                    controller: {
                    inverse: true,
                },
                
            },

                property: "",
                
                // id: this.$route.params.id,

            }
        },

        // computed: {
        //     property() {
        //         return this.properties.find(property => property.id == this.id);
        //     }
        // },
        computed: {
            btnOutlineColor: function () {
            if (this.sharedState.is_authenticated) {
                if (this.property.likers_id && this.property.likers_id.indexOf(this.sharedState.user_id) != -1) {
                return 'u-btn-outline-red'
                } else {
                return 'u-btn-outline-primary'
                }
            } else {
                return 'u-btn-outline-primary'
            }
        },


        },        

        methods: {
            getPost (id) {
              if (typeof id == String){
                id = Number(id)

            }

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

            onEditPost (property) {

            this.editPostForm = Object.assign({}, property)
            },
            onSubmitUpdatePost () {
            this.editPostForm.errors = 0  // 重置
            $('#editPostForm .form-control-feedback').remove()
            $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

            if (!this.editPostForm.title) {
                this.editPostForm.errors++
                this.editPostForm.titleError = 'Title is required.'
                $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
                $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
            } else {
                this.editPostForm.titleError = null
            }

            if (!this.editPostForm.body) {
                this.editPostForm.errors++
                this.editPostForm.bodyError = 'Body is required.'
                $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
                $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
            } else {
                this.editPostForm.bodyError = null
            }

            if (this.editPostForm.errors > 0) {
                return false
            }

            const path = `/api/properties/${this.editPostForm.id}`
            const payload = {
                title: this.editPostForm.title,
                summary: this.editPostForm.summary,
                body: this.editPostForm.body
            }
            this.$axios.put(path, payload)
                .then((response) => {
                $('#editPostModal').modal('hide')

                // handle success
                this.getPost(this.editPostForm.id)
                this.$toasted.success('Successed update the property.', { icon: 'fingerprint' })
                this.editPostForm.title = '',
                this.editPostForm.summary = '',
                this.editPostForm.body = ''
                })
                .catch((error) => {
                // handle error
                for (var field in error.response.data.message) {
                    if (field == 'title') {
                    this.editPostForm.titleError = error.response.data.message[field]
                    $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
                    $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
                    } else if (field == 'body') {
                    this.editPostForm.bodyError = error.response.data.message[field]
                    $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
                    $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
                    } else {
                    this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
                    }
                }
                })
            },
            onResetUpdatePost () {
            $('#editPostForm .form-control-feedback').remove()
            $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
            //  
            $('#editPostModal').modal('hide')
            // this.getPosts()
            this.$toasted.info('Cancelled, the property is not update.', { icon: 'fingerprint' })
            },
            onDeletePost (property) {
            this.$swal({
                title: "Are you sure?",
                text: "This operation will be completely deleted [ " + property.title + " ], please be carefully",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!'
            }).then((result) => {
                if(result.value) {
                const path = `/api/properties/${property.id}`
                this.$axios.delete(path)
                    .then((response) => {
                    // handle success
                    this.$swal('Deleted', 'You successfully deleted this property', 'success')
                    if (typeof this.$route.query.redirect == 'undefined') {
                        this.$router.push('/')
                    } else {
                        this.$router.push(this.$route.query.redirect)
                    }
                    })
                    .catch((error) => {
                    // handle error
                    console.log(error.response.data)
                    this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
                    })
                
                } else {
                this.$swal('Cancelled', 'The property is safe :)', 'error')
                }
            })
            },
            onLikeOrUnlikePost (property) {
            if (!this.sharedState.is_authenticated) {
                this.$toasted.error('You need to log in to collect articles ...', { icon: 'fingerprint' })
                this.$router.replace({
                path: '/login',
                query: { redirect: this.$route.path + '#like-property' }
                })
            }

            let path = ''
            if (property.likers_id.indexOf(this.sharedState.user_id) != -1) {
                // The currently logged-in user has already favorited this article, click again to cancel the favorite
                path = `/api/properties/${property.id}/unlike`
            } else {
                path = `/api/properties/${property.id}/like`
            }
            this.$axios.get(path)
                .then((response) => {
                // handle success
                this.getPost(this.$route.params.id)
                this.$toasted.success(response.data.message, { icon: 'fingerprint' })
                })
                .catch((error) => {
                // handle error
                console.log(error.response.data)
                this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
                })
            },

            tocAllRight: function (tocHtmlStr) {
            // console.log("toc is parsed :", tocHtmlStr);
            // You must wait for vue-markdown to generate TOC before using jquery to manipulate DOM!!!
            // Non-default list style
            $('.toc').find('ul').addClass('u-list-inline');
            // 2, 3 level directory indentation
            $('.toc ul li ul li').addClass('g-ml-15');
            $('.toc ul li ul li ul li').addClass('g-ml-15');
            // Link color, hover color
            $('.toc').find('a').addClass('u-link-v5 g-color-aqua g-color-red--hover')
            }
        },
        created () {
 
            this.getPost(this.id)

            // Initialize the bootstrap-markdown editor
            $(document).ready(function() {
            $("#editPostFormBody, #commentFormBody, #editCommentFormBody").markdown({
                autofocus:false,
                savable:false,
                iconlibrary: 'fa',  // 使用Font Awesome图标
                language: 'en'
            })
            })
            // Use jquery.sticker.js plug-in to make TOC fixed position
            $(document).ready(function(){
            $("#sticker").sticky({ topSpacing: 10 });
            })
            // tooltip
            $(document).ready(function(){
            $('[data-toggle="tooltip"]').tooltip(); 
            })
            // After clicking the reply comment link, move and display the comment form
            $(document).ready(function() {
            $('body').on('click', '.comment-reply-link', function() {
                // Click on the reply link to this comment
                var $comment = $(this).closest('.comment-item');
                // Add the comment box below the comment you want to reply to
                $comment.after($('#addCommentForm'));
                // If it is a secondary comment, the comment box should be indented to the right
                if ($comment.hasClass('g-ml-40')) {
                $('#addCommentForm').addClass('g-ml-40')
                } else {
                $('#addCommentForm').removeClass('g-ml-40')
                }
                // Cursor in the comment box
                $('#commentFormBody').focus()
            })
            })
        },
        // Reload data when routing changes
        beforeRouteUpdate (to, from, next) {
            next()
            this.getPost(to.params.id)

        },


    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
/*Carousel*/
  .swiper-slide {
    background-size: cover;
    background-position: center;
    
  }
  .gallery-top {
    height: 80%!important;
    width: 100%;
  }
  .gallery-thumbs {
    height: 20%!important;
    box-sizing: border-box;
    padding: 10px 0;
  }
  .gallery-thumbs .swiper-slide {
    width: 25%;
    height: 100%;
    opacity: 0.4;
  }
  .gallery-thumbs .swiper-slide-active {
    opacity: 1;
  }

  /*End Carousel*/

  /*Property Info*/
    .property-info {
        border-bottom: 1px dotted $color1-light;
        display: flex;
        justify-content: space-between;
        align-items: center;
        }

  .property-main-info {
      background: $color1-light;
      padding: 20px;
      margin: 0 30px;
      box-shadow: -1px 2px 10px 0 rgba(0, 0, 0, 0.2);
      -webkit-box-shadow: -1px 2px 10px 0 rgba(0, 0, 0, 0.2);
      -moz-box-shadow: -1px 2px 10px 0 rgba(0, 0, 0, 0.2);

      .quick-features {
          display: flex;
          justify-content: space-between;
          align-items: center;

          .btn-outline-style1 {
              margin: auto 20px;
              &:hover {
                  text-decoration: none;
              }
          }
      }
    .property-details {
        border-right: 2px dotted #fff;


        p {
            margin: 30px 0;
        }
    }
  } 
 /*End Property Info*/
 
 @media(max-width: 768px) {
     .property-main-info {
         margin-bottom: 20px!important;
         .property-details {
         border-right: 0!important;
        }
     }
     
     .quick-features {
         flex-direction: column!important;
         width: 100%!important;
         a {
             margin: 10px auto!important;
         }
     }
 }
</style>