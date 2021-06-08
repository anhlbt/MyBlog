<template>
    <div>
    <!--Filter-->
    <b-container>
        <inline-filter :searchForm="form"
        v-on:toPropertiesFullWidth="onAssignProperties"></inline-filter>
        <!-- <inline-filter :searchForm="[(typeof searchProperties != 'undefined')? searchProperties : form]"
        v-on:toPropertiesFullWidth="onAssignProperties" v-model="searchForm"></inline-filter> -->
    </b-container>
     <!-- <b-container v-else>
        <inline-filter v-on:toPropertiesFullWidth="onAssignProperties"></inline-filter>
    </b-container>    -->
    <!--End Filter-->
    <b-container v-cloak>
    
            <!--Grid/list switching icons-->
            <div class="tool-bar">
                <select class="float-left" name="prop-filter" v-model="filter" v-on:change="change(filter)">
                    <!-- <option value="" disabled selected style="display: none;">Please select a filter</option> -->
                    <option value="By Date(Newest)">Sort by Newest</option>
                    <option value="By Date(Oldest)">Sort by Oldest</option>
                    <option value="Price Down">Sort by Price (High to low)</option>
                    <option value="Price Up">Sort by Price (Low to high)</option>
                </select>	
                <a class="list-icon" v-b-tooltip.hover title="List" v-on:click="layout = 'list'" :class="{ 'active': layout == 'list'}" ></a>
                <a class="grid-icon" v-b-tooltip.hover title="Grid" v-on:click="layout = 'grid'" :class="{ 'active': layout == 'grid'}"></a>
            </div>
            <!--End grid/list switching icons-->
            
            <!--Grid-->
            <div v-if="layout === 'grid'" class="grid">
                <b-row>
                    <b-col class="my-3" cols="12" md="4" v-for="(property, id) in properties.items" :key="id">
                        <div class="property-grid-card">
                            <div class="wrap">
                                <img width="300" :src="base_url+'/api/static/'+property.images[0]">
                                <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
                                <span class="type-badge">{{property.type }}</span>
                                <span class="contract-badge">{{property.purpose }}</span>
                                 <favorite 
                                :title="property.title"
                                :image="base_url+'/api/static/'+property.images[0]"
                                :id="property.id"
                                />
                               <router-link class="property-title" :to="`/properties/${property.id}`">
                                   <h5 class="my-2">{{ property.title }}</h5>
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
            </div>
            <!--End Grid-->

            <!--List-->
            <div v-if="layout === 'list'" class="list">
                
               <b-row>
                    <b-col class="my-3" cols="12" v-for="(property, id) in properties.items" :key="id">
                        <div class="">
                        <div class="wrap">
                            <b-row>
                                <b-col cols="12" md="4">
                                    <img width="350" :src="base_url+'/api/static/'+property.images[0]">
                                    <span class="promoted-badge" v-if="property.promoted == 'Promoted'">{{ property.promoted }}</span>
                                    <span class="type-badge">{{property.type }}</span>
                                    <span class="contract-badge">{{property.purpose }}</span>
                                </b-col>
                                <b-col cols="12" md="8">
                                     <favorite 
                                    :title="property.title"
                                    :image="base_url+'/api/static/'+property.images[0]"
                                    :id="property.id"
                                    />
                                    
                                    <router-link class="property-title" :to="`/properties/${property.id}`">
                                        <h5 class="my-2">{{ property.title }}</h5>
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

                                </b-col>
                            </b-row>
                            
                        
                            
                        </div>
                        </div>  
                    </b-col>
                </b-row>  
            </div>
            <!--End List-->

        </b-container>
    </div>
</template>

<script>
import inlineFilter from '@/components/searchForms/inlineFilter.vue';
import favorite from '@/components/otherSections/favorite.vue';

export default {
    data() {
        return {
            filter: "By Date(Newest)",
            layout: 'list',
            base_url: this.$axios.defaults.baseURL,
            properties: null,
        
            form: {
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
        }
    },
    components: {
        inlineFilter,
        favorite
    },
    
    props:{
        searchProperties:{
            type:Object,
            value: null,
        }
    },    
    copmputed: { 
    },
    
    methods:{
        checkSearchForm()
        {
            if(typeof this.searchProperties != 'undefined')
            {
                // this.form = this.searchForm
                this.form = Object.assign({}, this.searchProperties)
                console.log("this.searchProperties ", this.searchProperties)
            }

            else if(typeof this.$route.params != 'undefined')
            {
                this.form.purpose = this.$route.params.purpose
                this.form.type = this.$route.params.type
                // this.searchProperties = Object.assign({}, this.form)
                console.log("this.$route.params ", this.form)
            } 
        },

        
      getSearchProperties() {
   
        const path = '/api/properties_area/'
        const payload = {
              province: this.form.province,
              district: this.form.district,
              ward: this.form.ward,
              type: this.form.type,
              purpose: this.form.purpose,
              floor: this.form.floor,
              bedroom: this.form.bedroom,
              bathroom: this.form.bathroom,
              agency: this.form.agency,
              agent: this.form.agent,
              checked: this.form.checked,
              features: this.form.features,
              price: this.form.price,
              address: this.form.address,
              direction: this.form.direction,
        }
        this.$axios.post(path, payload)
          .then((response) => {
            // handle success
            this.properties = response.data
            console.log( "this.properties ", this.properties )
            this.$toasted.success('Successed search ...', { icon: 'fingerprint' })

          })
          .catch((error) => {
            // handle error
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
          })

      },

      onAssignProperties(value){
          console.log('childProperties', value)
          this.properties = Object.assign({}, value)
      },

    //change function is used in <select> with v-model, option value call a sort method
        change: function(par) {
        switch (par) {
            case "Price Up":
            return this.sortByPriceUp();
            break;
            case "Price Down":
            return this.sortByPriceDown();
            break;
            case "Sort Alphabeticly A-Z":
            return this.sortAlpha();
            break;
            case "Sort Alphabeticly Z-A":
            return this.sortAlphaZ();
            break;
            case "By Date(Newest)":
            return this.sortByDateNew();
            break;
            case "By Date(Oldest)":
            return this.sortByDateOld();
            break;
            case "By ID":
            return this.sortByid();
            break;
        }
        },
    //just a sort() functions combined
        sortByPriceUp: function() {
        this.properties.items.sort(function(a, b) {
            return a.price - b.price;
        })
        },
        sortByPriceDown: function() {
        this.properties.items.sort(function(a, b) {
            return b.price - a.price;
        })
        },
        sortByid: function() {
        this.properties.items.sort(function(a, b) {
            return a.id - b.id;
        })
        },
        sortAlpha: function() {
        this.properties.items.sort(function(a, b) {
            var x = a.title.toLowerCase();
            var y = b.title.toLowerCase();
            if (x < y) {
            return -1;
            }
            if (x > y) {
            return 1;
            }
            return 0;
        });
        },
        sortAlphaZ: function() {
        this.properties.items.sort(function(a, b) {
            var x = a.title.toLowerCase();
            var y = b.title.toLowerCase();
            if (y < x) {
            return -1;
            }
            if (y > x) {
            return 1;
            }
            return 0;
        });
        },
        sortByDateNew: function() {
        this.properties.items.sort(function(a, b) {
            return new Date(b.post_at) - new Date(a.post_at);
        });
        },
        sortByDateOld: function() {
        this.properties.items.sort(function(a, b) {
            return new Date(a.post_at) - new Date(b.post_at);
        });
        }

    },
    created () {
        this.checkSearchForm()
      this.getSearchProperties()
      
    },
    // Reload data when routing changes
    beforeRouteUpdate (to, from, next) {
        next()
        // console.log("to ... from :", to, from)
        this.checkSearchForm()
        this.getSearchProperties()

  },

}
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
@import "./../../assets/scss/main";

[v-cloak] {
		
		display: none;
}

/* The tool bar */
.tool-bar {
    background: $color1-light;
	box-shadow: 0 1px 1px #ccc;
	line-height: 1;
	margin: 0 auto;
	padding: 10px;
	position: relative;
	text-align: right;
    width: 100%;
    
    select {
        padding: 4px 10px;
        &:focus {
            outline: none!important;
        }
    }
}

.tool-bar a {
	background: rgba( 0, 0, 0, 0.40 ) center center no-repeat;
	border: 1px solid #e4e4e4;
	border-right: 1px solid #908f8f;
	border-bottom: 1px solid #908f8f;
	cursor: pointer;
	display: inline-block;
	height: 32px;
	margin-right: 5px;
	text-decoration: none;
	width: 32px;
}


.tool-bar a.active {
	background-color: rgba( 0, 0, 0, 0.80 );
	border: 1px solid #908d8d;
	border-right: 1px solid #e2e2e2;
	border-bottom: 1px solid #e2e2e2;
}

.tool-bar a.active:hover {
	cursor: default;
}

.tool-bar a.list-icon {
	background-image: url( "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkYzNkFCQ0ZBMTBCRTExRTM5NDk4RDFEM0E5RkQ1NEZCIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkYzNkFCQ0ZCMTBCRTExRTM5NDk4RDFEM0E5RkQ1NEZCIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RjM2QUJDRjgxMEJFMTFFMzk0OThEMUQzQTlGRDU0RkIiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RjM2QUJDRjkxMEJFMTFFMzk0OThEMUQzQTlGRDU0RkIiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7h1bLqAAAAWUlEQVR42mL8////BwYGBn4GCACxBRlIAIxAA/4jaXoPEkMyjJ+A/g9MDJQBRhYg8RFqMwg8RJIUINYLFDmBUi+ADQAF1n8ofk9yIAy6WPg4GgtDMRYAAgwAdLYwLAoIwPgAAAAASUVORK5CYII=" );
}

.tool-bar a.grid-icon  {
	background-image: url( "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjBEQkMyQzE0MTBCRjExRTNBMDlGRTYyOTlBNDdCN0I4IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjBEQkMyQzE1MTBCRjExRTNBMDlGRTYyOTlBNDdCN0I4Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MERCQzJDMTIxMEJGMTFFM0EwOUZFNjI5OUE0N0I3QjgiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MERCQzJDMTMxMEJGMTFFM0EwOUZFNjI5OUE0N0I3QjgiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4MjPshAAAAXklEQVR42mL4////h/8I8B6IGaCYKHFGEMnAwCDIAAHvgZgRyiZKnImBQsACxB+hNoDAQyQ5osQZIT4gH1DsBZABH6AB8x/JaQzEig++WPiII7Rxio/GwmCIBYAAAwAwVIzMp1R0aQAAAABJRU5ErkJggg==" );
}

/* Grid layout */
.grid {
	list-style: none;
	margin: 0 auto;
	padding: 20px;
	text-align: left;
	width: 100%;
}

.grid li {
	display: inline-block;
	position: relative;
	width: 50%;
}

.grid li:after {
	content: "";
	display: block;
	padding-bottom: 52%;
}

.grid li a {
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	border: 2px solid #fff;
	height: 99%;
	position: absolute;
	width: 98%;
}

.grid li a:hover {
	border: 2px solid #000;
	box-shadow:         inset 0 0 90px -10px rgba( 0, 0, 0, 1 );
	-moz-box-shadow:    inset 0 0 90px -10px rgba( 0, 0, 0, 1 );
	-webkit-box-shadow: inset 0 0 90px -10px rgba( 0, 0, 0, 1 );
}

/* List layout */
.list {
	list-style: none;
	margin: 0 auto;
	padding: 0;
	text-align: left;
	width: 100%;
}

.list li {
	border-bottom: 1px solid #fff;
	overflow: hidden;
	padding: 20px;
	transition: background 0.2s linear;
}

.list li:hover {
	background-color: #fff;
}

.list li a {
	display: table;
	width: 100%;
}


.list li img {
	border: none;
	display: table-cell;
	height: 120px;
	vertical-align: middle;
	width: 120px;
}

.list li:hover p {
	color: #0096d4;
}

.list li p {
	color: #000;
	display: table-cell;
	font-weight: 700;
	padding: 0 0 0 15px;
	vertical-align: middle;
	width: 100%;
}

/*Properties animation*/
/*End properties animation*/
</style>

