<template>
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
                                <router-link to="/" tag="li"><a>Home</a></router-link>
                                <b-dropdown split split-href="/properties/propertiesFullWidth" text="For rent" class="m-2">
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Apartments</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Studios</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Houses</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Commercial</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Land</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Office</b-dropdown-item></router-link>
                                </b-dropdown>

                                <b-dropdown split split-href="/properties/propertiesFullWidth" text="For sale" class="m-2">
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Apartments</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Studios</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Houses</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Commercial</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Land</b-dropdown-item></router-link>
                                    <router-link to="/properties/propertiesFullWidth" tag="li"><b-dropdown-item>Office</b-dropdown-item></router-link>
                                </b-dropdown>

                                <router-link to="/" tag="li"><a>About company</a></router-link>
                                <router-link to="/contact" tag="li"><a>Contact</a></router-link>

                            </b-navbar-nav>
                            <router-link class="btn-style1 add-property-btn" to="addProperty" tag="a"> Add property <img width="30" src="@/assets/images/add.png" alt=""></router-link>
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
import store2 from '../../store/index.js';
import favorite from '@/components/otherSections/favorite.vue';


    export default {
        data() {
            return {
                lst_favorite: store2.state.favorite,
                modalShow: false,
                dismissSecs: 5,
                dismissCountDown: 0
            }
        },

        methods: {
            hideModal() {
                this.modalShow = false
            },
            removeToFav() {
                store2.commit('removeToFav', this.item)
            },

        }
    }
</script>

<style lang="scss" scoped>

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
            font-size: 18px;
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