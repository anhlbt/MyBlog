<template>
  <!-- <section>
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
        <div class="navbar-brand">
          <router-link to="/" class="g-text-underline--none--hover">
            <img
              src="../../assets/logo.png"
              width="30"
              height="30"
              class="d-inline-block align-top"
              alt
            />
          </router-link>
          <router-link to='/' class="g-text-underline--none--hover" >LBTAnh's Blog</router-link>
        </div>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
            <li class="nav-item active">
              <router-link to="/" class="nav-link">
                Home
                <span class="sr-only">(current)</span>
              </router-link>
            </li>
            <li class="nav-item active">
              <router-link to="/realestate" class="nav-link">
                RealEstate
                <span class="sr-only">(current)</span>
              </router-link>
            </li>            
            <li
              class="nav-item active" 
              v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')"
            >
              <router-link to="/admin" class="nav-link">Admin</router-link>
            </li>            
          </ul>

          <form
            v-if="sharedState.is_authenticated"
            class="form-inline navbar-left mr-auto"
            @submit.prevent="onSubmitSearch"
          >
            <input
              v-model="searchForm.body"
              id="searchBody"
              class="form-control mr-sm-2"
              type="search"
              placeholder="Search"
            />
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </form>

          <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
            <li class="nav-item g-mr-20">
              <router-link v-bind:to="{ path: '/notifications/comments' }" class="nav-link">
                <i
                  class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"
                ></i> Notifications
                <span
                  id="new_notifications_count"
                  style="visibility: hidden;"
                  class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10"
                >0</span>
              </router-link>
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdown"
                role="button"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                <img
                  v-bind:src="sharedState.user_avatar"
                  class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded"
                />
                {{ sharedState.user_name }}
              </a>
              <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                <router-link
                  v-bind:to="{ path: `/user/${sharedState.user_id}` }"
                  class="dropdown-item"
                >
                  <i class="icon-star g-pos-rel g-top-1 g-mr-5"></i> Your profile
                </router-link>
                <router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item">
                  <i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource
                </router-link>
                <router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item">
                  <i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings
                </router-link>
                <div class="dropdown-divider"></div>
                <a v-on:click="handlerLogout" class="dropdown-item" href="#">
                  <i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> Sign out
                </a>
              </div>
            </li>
          </ul>
          <ul v-else class="nav navbar-nav navbar-right">
            <li class="nav-item">
              <router-link to="/login" class="nav-link">
                <i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> Sign in
              </router-link>
            </li>
          </ul>
        </div>
        
      </nav>     
    </div>  
  </section> -->

  <div>
    <div id="menu1">
      <b-container>
        <b-row>
          <div id="main-nav" class="w-full">
            <b-col cols="12">
              <b-navbar toggleable="lg">
                <b-navbar-brand href="/"><img width="120" src="@/assets/images/real-estate.png" alt=""></b-navbar-brand>

                <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

                <b-collapse id="nav-collapse" is-nav>

                  <!-- Right aligned nav items -->
                  <b-navbar-nav class="ml-auto">
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                      <ul class="navbar-nav mr-auto mt-2 mt-lg-0"> 
                        <!-- <router-link v-bind:to="{ name: 'propertiesFullWidth', params: { searchProperties: form} }"> -->
                        <li class="nav-item dropdown" @mouseover="()=>{this.$refs.dropdown.visible = true;}" @mouseleave="()=>{this.$refs.dropdown.visible = false;}">
                          <b-dropdown ref="dropdown" :split-to="{ name: 'propertiesFullWidth2' , params: { searchProperties: {purpose:'Sale', type: 'Apartment'} }}"
                           text="For sale" class="m-2 nav-link"
                            toggle-class="text-decoration-none"
                            variant="none" no-caret>
                          <template slot="button-content">
                            <i class="icon-real-estate-034">&nbsp;</i>For sale 
                          </template>                                  
                            <b-dropdown-item
                              tag="li"
                              v-for="itemSale in listSales"
                              :key="itemSale.id"
                              :to="{ path: `/propertiesFullWidth/${itemSale.purpose}/${itemSale.type}` }">
                              <p :class="itemSale.icon ">&nbsp;&nbsp;{{itemSale.type}}</p>
                            </b-dropdown-item> 
                            <!-- <b-dropdown-item @click="changeRout({searchProperties:{purpose:'Sale', type: 'Apartment'}})" tag="li">Aparments</b-dropdown-item> -->
                          </b-dropdown>
                        </li> 
                        <li class="nav-item dropdown" @mouseover="()=>{this.$refs.dropdown1.visible = true;}" @mouseleave="()=>{this.$refs.dropdown1.visible = false;}">

                          <b-dropdown ref="dropdown1" :split-to="{ name: 'propertiesFullWidth2', params: { searchProperties: {purpose:'Rent', type: 'Apartment'} }}" text="For rent" class="m-2"
                              toggle-class="text-decoration-none"
                              variant="none" no-caret>
                            <template slot="button-content">
                              <i class="icon-real-estate-035">&nbsp;</i>For rent 
                            </template>
                            <b-dropdown-item
                              tag="li"
                              v-for="itemRent in listRents"
                              :key="itemRent.id"
                              :to="{ path: `/propertiesFullWidth/${itemRent.purpose}/${itemRent.type}` }">
                              <p :class="itemRent.icon">&nbsp;&nbsp;{{itemRent.type}}</p>
                            </b-dropdown-item>                               
                          </b-dropdown>
                        </li> 
                          

                    
                        <!-- <router-link to="/" tag="li"><a>About company</a></router-link> -->
                        
                        
                        <!-- <div class="collapse navbar-collapse" id="navbarSupportedContent"> -->
                        <!-- <ul class="navbar-nav mr-auto mt-2 mt-lg-0">  -->
                        <li class="nav-item"><router-link to="/posts" tag="li"><a>News</a></router-link></li>        
                        <li class="nav-item"><router-link to="/contact" class="icon-communication-109 nav-link"><a>&nbsp;Contact</a></router-link></li>
                        <li
                          class="nav-item active" 
                          v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')"
                        >
                          <router-link to="/admin" class="nav-link icon-education-073 fa-lg">&nbsp;Admin</router-link>
                        </li>            
                      </ul>

                      <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
                        <!-- <li class="nav-item g-mr-20">
                          <router-link v-bind:to="{ path: '/notifications/comments' }" class="nav-link">
                            <i
                              class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"
                            ></i> Notifications
                            <span
                              id="new_notifications_count"
                              style="visibility: hidden;"
                              class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10"
                            >0</span>
                          </router-link>
                        </li> -->
                        <li class="nav-item dropdown">
                          <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="navbarDropdown"
                            role="button"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false"
                          >
                            <img
                              v-bind:src="sharedState.user_avatar"
                              class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded"
                            />
                            {{ sharedState.user_name }}
                          </a>
                          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <router-link v-bind:to="{ path: '/notifications/comments' }" class="dropdown-item">
                              <i class="icon-education-033 g-color-red g-font-size-16 g-pos-rel g-top-1 g-mr-5"
                              ></i> Notifications
                              <span
                                id="new_notifications_count"
                                style="visibility: hidden;"
                                class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10"
                              >0</span>
                            </router-link>                                           
                            <router-link
                              v-bind:to="{ path: `/user/${sharedState.user_id}` }"
                              class="dropdown-item"
                            >
                              <i class="icon-star g-pos-rel g-top-1 g-mr-5"></i> Your profile
                            </router-link>                                     
                            <router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item">
                              <i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource
                            </router-link>
                            <router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item">
                              <i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings
                            </router-link>
                            <div class="dropdown-divider"></div>
                            <a v-on:click="handlerLogout" class="dropdown-item" href="#">
                              <i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> Sign out
                            </a>
                          </div>
                        </li>
                      </ul>
                      <ul v-else class="nav navbar-nav navbar-right">
                        <li class="nav-item">
                          <router-link to="/login" class="nav-link">
                            <i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> Sign in
                          </router-link>
                        </li>
                      </ul>                                                                
                    </div>
                  </b-navbar-nav>
                  <router-link @click.native="onAddProperty" id="addProperty" class="btn-style1 add-property-btn" :to="{name:'AddProperty'}" tag="a"> Add property <img width="20" src="@/assets/images/add.png" alt=""></router-link>
                </b-collapse>
                    <!--Wishlist icon-->

                <span class="fav-icon ml-5" @click="modalShow = !modalShow"><img width="30" src="@/assets/images/icons/heart.png" alt=""><sup class="fav-count">{{lst_favorite.length}}</sup></span>
                <b-modal v-model="modalShow" hide-footer title="Your favorite properties">
                    <ul class="wishlist">
                        <li class="single-property" v-for="(item, id) in lst_favorite" :key="id">
                            <span class="delete-fav mr-3" v-b-tooltip.hover title="Delete from favorite" @click="removeToFav">×</span>
                            <img width="100" :src="item.propertyImage" />
                            <router-link class="property-title close" :to="`/properties/${item.propertyId}`" @click="hide()" > 
                            <h3>{{ item.propertyTitle }}</h3>
                            </router-link>
                            <hr>
                        </li>
                    </ul>
                </b-modal>
                    <!--End wishlist icon-->
                    
                </b-navbar>

            </b-col>
          </div>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
import store from "../../store.js";
//If you use axios in JQuery, you need to re-import, you cannot use the Vue global attribute this.$axios defined in main.js
import axios from "axios";
import store2 from '../../store/index.js';
import propertiesFullWidth from "../pages/propertiesFullWidth"



export default {
  name: "Navbar", //this is the name of the component

  data() {
    return {
      Apartment: "Apartment",
      sharedState: store.state,
      lst_favorite: store2.state.favorite,
      searchForm: {
        body: ""
      },
      modalShow: false,
      dismissSecs: 5,
      dismissCountDown: 0,

      listSales:[
        {"id":1, "purpose": "Sale", "type": "Apartment", "icon":"icon-real-estate-011 g-font-size-16" },
        {"id":2, "purpose": "Sale", "type": "Studio" , "icon":"icon-music-021 g-font-size-16"},
        {"id":3, "purpose": "Sale", "type": "House" , "icon":"icon-real-estate-003 g-font-size-16"},
        {"id":4, "purpose": "Sale", "type": "Commercial", "icon":"icon-real-estate-034 g-font-size-16" },
        {"id":5, "purpose": "Sale", "type": "Land", "icon":"icon-real-estate-027 g-font-size-16" },
        {"id":6, "purpose": "Sale", "type": "Office", "icon":"icon-real-estate-077 g-font-size-16" }              
      ],

      listRents:[
        {"id":1, "purpose": "Rent", "type": "Apartment" , "icon":"icon-real-estate-011 g-font-size-16"},
        {"id":2, "purpose": "Rent", "type": "Studio" , "icon":"icon-music-021 g-font-size-16"},
        {"id":3, "purpose": "Rent", "type": "House", "icon":"icon-real-estate-003 g-font-size-16" },
        {"id":4, "purpose": "Rent", "type": "Commercial", "icon":"icon-real-estate-034 g-font-size-16" },
        {"id":5, "purpose": "Rent", "type": "Land", "icon":"icon-real-estate-027 g-font-size-16" },
        {"id":6, "purpose": "Rent", "type": "Office", "icon":"icon-real-estate-077 g-font-size-16" }              
      ]
    };
  },
  components:{
    propertiesFullWidth,
  },

  methods: {

    hideModal() {
        this.modalShow = false
    },
    removeToFav() {
        store2.commit('removeToFav', this.item)
    },

    changeRout(data) {
      console.log('event.target.value ',data)
      this.$router.push({ path: `/propertiesFullWidth/${data.searchProperties.purpose}/${data.searchProperties.type}` , params: { searchProperties: data}})
      // this.$router.push({ name: 'propertiesFullWidth' , params: { searchProperties: data}})

    },
    handlerLogout(e) {
      store.logoutAction();
      this.$toasted.show("You have been logged out.", { icon: "fingerprint" });
      this.$router.push("/login");
    },
    onSubmitSearch() {
      if (!this.searchForm.body) {
        $("#searchBody").attr("placeholder", "keyword required.");
        $("#searchBody").css("background-color", "#fff0f0");

        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false;
      } else {
        $("#searchBody").css("background-color", "");
      }

      // 提供了搜索关键词后，只需要路由到搜索结果页即可，在 SearchResult.vue 中再请求后端 API
      let q = this.searchForm.body;
      let page = 1;
      let per_page = 5;
      if (typeof this.$route.query.page != "undefined") {
        page = this.$route.query.page;
      }

      if (typeof this.$route.query.per_page != "undefined") {
        per_page = this.$route.query.per_page;
      }

      // 路由到搜索结果页
      this.$router.replace({
        path: "/search",
        query: {
          q: q,
          page: page,
          per_page: per_page
        }
      });
    },

    onAddProperty()
    {
        if (!this.sharedState.is_authenticated) {
        this.$toasted.error('You need to log in to collect articles ...', { icon: 'fingerprint' })
        this.$router.replace({
          path: '/login',
          query: { redirect: this.$route.path + '#addProperty' }
        })
      }
    },


  },
  mounted() {
    // 轮询 /api/users/<int:id>/notifications/ 请求用户的新通知
    $(function() {
      let since = 0;
      let total_notifications_count = 0; // 总通知计数
      let unread_recived_comments_count = 0; // 收到的新评论通知计数
      let unread_messages_count = 0; // 收到的新私信通知计数
      let unread_follows_count = 0; // 新粉丝通知计数
      let unread_posts_likes_count = 0; // 新收藏文章的通知计数
      let unread_comments_likes_count = 0; // 新的评论点赞的通知计数
      let unread_followeds_posts_count = 0; // 用户关注的人的新文章通知计数

      setInterval(function() {
        if (window.localStorage.getItem("madblog-token")) {
          // 如果用户已登录，才开始请求 API
          const payload = JSON.parse(
            atob(window.localStorage.getItem("madblog-token").split(".")[1])
          );
          const user_id = payload.user_id;
          const path = `/api/users/${user_id}/notifications/?since=${since}`;
          axios
            .get(path)
            .then(response => {
              // handle success
              for (var i = 0; i < response.data.length; i++) {
                switch (response.data[i].name) {
                  case "unread_recived_comments_count":
                    unread_recived_comments_count = response.data[i].payload;
                    // jQuery设置值 (因为左侧导航栏不是一个组件内)
                    $("#unread_recived_comments_count").text(
                      unread_recived_comments_count
                    );
                    break;

                  case "unread_messages_count":
                    unread_messages_count = response.data[i].payload;
                    $("#unread_messages_count").text(unread_messages_count);
                    break;

                  case "unread_follows_count":
                    unread_follows_count = response.data[i].payload;
                    $("#unread_follows_count").text(unread_follows_count);
                    break;

                  case "unread_posts_likes_count":
                    unread_posts_likes_count = response.data[i].payload;
                    $("#unread_posts_likes_count").text(
                      unread_posts_likes_count
                    );
                    break;

                  case "unread_comments_likes_count":
                    unread_comments_likes_count = response.data[i].payload;
                    $("#unread_comments_likes_count").text(
                      unread_comments_likes_count
                    );
                    break;

                  case "unread_followeds_posts_count":
                    unread_followeds_posts_count = response.data[i].payload;
                    $("#unread_followeds_posts_count").text(
                      unread_followeds_posts_count
                    );
                    break;

                  case "task_progress":
                    $("#" + response.data[i].payload.task_id).text(
                      response.data[i].payload.description +
                        " " +
                        response.data[i].payload.progress +
                        "%"
                    );
                    break;
                }
                since = response.data[i].timestamp;
              }

              total_notifications_count =
                unread_recived_comments_count +
                unread_messages_count +
                unread_follows_count +
                unread_posts_likes_count +
                unread_comments_likes_count +
                unread_followeds_posts_count;
              // 每一次请求之后，根据 total_notifications_count 的值来显示或隐藏徽标
              $("#new_notifications_count").text(total_notifications_count);
              $("#new_notifications_count").css(
                "visibility",
                total_notifications_count ? "visible" : "hidden"
              );
            })
            .catch(error => {
              // handle error
              console.error(error);
            });
        }
      }, 3000);
    });
  },

  // Reload data when routing changes
  beforeRouteUpdate (to, from, next) {
    next()
    console.log(to, from)

  },


};
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/main";
    #main-nav {
        width: 100%;
        ul {
            li {
                display: flex;
                list-style: none!important;
                a {
                    font-size: 15px;
                    color: #000;
                    margin: auto 5px;

                    &:hover {
                        text-decoration: none;
                    }
                }
            }
        }

        .add-property-btn {
            margin-left: 50px;
            float: right;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 16px;
            font-weight: bold;
            &:hover {
                text-decoration: none;
            }

            img {
                margin: auto 10px;
            }
        }

        .fav-count {
            background: #b92a13;
            border-radius: 50%;
            padding: 0 5px;
            color: #fff;
            margin-left: -5px;
        }
    }

    .wishlist {
        padding: 0;
        .single-property {
            list-style: none!important;
            margin: 20px 0;

            .delete-fav {
                color: #b92a13;
                font-size: 30px;
                font-weight: 800;
                cursor: pointer;
            }
        }
    }

@media(max-width: 768px) {
    #main-nav {
        .navbar {
            .add-property-btn {
                margin-left: 0;
                margin-top: 30px;
                float: left;
            }

            .fav-icon {
                margin: 10px;
            }
        }
    }
}        
</style>