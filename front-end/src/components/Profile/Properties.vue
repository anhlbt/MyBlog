<template>
  <div>
    <!-- Modal: Edit Post -->
    <div data-backdrop="static" class="modal fade" id="editPostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editPostModalTitle">Update Property</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          
            <!-- <form id="editPostForm" @submit.prevent="onSubmitUpdatePost" @reset.prevent="onResetUpdatePost">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editPostForm.titleError}">
                <input type="text" v-model="editPostForm.title" class="form-control" id="editPostFormTitle" placeholder="Title">
                <small class="form-control-feedback" v-show="editPostForm.titleError">{{ editPostForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editPostForm.description" class="form-control" id="editPostFormSummary" placeholder="Summary">
              </div>
              <div class="form-group">
                <textarea v-model="editPostForm.address" class="form-control" id="editPostFormBody" rows="5" placeholder="Content"></textarea>
                <small class="form-control-feedback" v-show="editPostForm.bodyError">{{ editPostForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form> -->
          </div>
            <!-- editPostForm -->
            <b-container id="add-property">
              <b-row>
                <!--Form Steps-->
                <div class="add-property-steps">
                  <p :class="this.step === 1 ? 'active-step' : ''">Main Informations</p>
                  <p :class="this.step === 2 ? 'active-step' : ''">Details</p>
                  <p :class="this.step === 3 ? 'active-step' : ''">Media</p>
                  <p :class="this.step === 4 ? 'active-step' : ''">Final details</p>
                </div>
                <!--End Form Steps-->
              </b-row>
              <b-row>
                <b-form id="editPostForm" @submit="onSubmitUpdatePost">
                  <!--Step 1-->
                  <div v-show="step === 1">
                    <b-row>
                      <b-col cols="12" md="6">

                        <b-form-input id="input-1" type="text" placeholder="Title" v-model="editPostForm.title"
                            :state="editPostForm.title.length >= 10"></b-form-input>

                        <b-form-input id="input-3" type="text" v-model="editPostForm.area" placeholder="Area or Address street..." required></b-form-input>
                        <b-form-select id="input-5" :options="contract" v-model="editPostForm.purpose" required></b-form-select>
                        <b-form-select id="input-7" :options="directions" v-model="editPostForm.direction" required></b-form-select>
                        <!-- <column-group :town="false" @values="regionChange"></column-group> -->

                      </b-col>
                      <b-col cols="12" md="6">
                      <b-form-select id="input-4" :options="types" v-model="editPostForm.type" required></b-form-select>
                      <b-form-input id="input-2" type="text" placeholder="Address" v-model="editPostForm.address" required></b-form-input>
                      <select-group :town="false" @values="regionChange"></select-group>
                      
                      <b-form-input id="input-6" type="number" placeholder="Price" v-model="editPostForm.price" required>
                      </b-form-input>
                      </b-col>
                      <b-col cols="9">
                        <b-form-textarea id="input-6" v-model="editPostForm.description" :state="editPostForm.description.length >= 20"
                        placeholder="Description..."
                        rows="4"
                        ></b-form-textarea>
                      </b-col>

                    </b-row>
                    <b-button class="btn-style1" @click.prevent="next()">Next <i class="fa fa-chevron-right ml-2"></i></b-button>
                  </div>
                  <!--End Step 1-->

                  <!--Step 2-->
                  <div v-show="step === 2">
                      <b-row>
                        <b-col cols="12" md="6">
                          <b-form-checkbox-group id="checkboxes-7" v-model="editPostForm.features">
                            <b-form-checkbox value="parking">Parking</b-form-checkbox>
                            <b-form-checkbox value="garage">Garage</b-form-checkbox>
                            <b-form-checkbox value="yard">Yard</b-form-checkbox>
                            <b-form-checkbox value="barbeque">Barbeque</b-form-checkbox>
                            <b-form-checkbox value="airconditioning">Air conditioning</b-form-checkbox>
                            <b-form-checkbox value="videosurveillance">Video surveilance</b-form-checkbox>
                            <b-form-checkbox value="terrace">Terrace</b-form-checkbox>
                            <b-form-checkbox value="centralheating">Central Heating</b-form-checkbox>
                          </b-form-checkbox-group>
                        </b-col>
                        <b-col cols="12" md="6">

                          <b-form-select id="input-8" :options="floors" v-model="editPostForm.floor_plan"></b-form-select>   
                          <b-form-select id="input-9" :options="bedrooms" v-model="editPostForm.bedroom" aria-placeholder="bedroom"></b-form-select>
                          <b-form-select id="input-9" :options="bathrooms" v-model="editPostForm.bathroom"></b-form-select>

                          <b-form-input id="input-10" type="number" v-model="editPostForm.total_area_sq_m" placeholder="Total Built Area (sq m)" min="0">
                          </b-form-input>
                            <b-form-input id="input-11" type="number" v-model="editPostForm.used_area_sq_m" placeholder="Used Area (sq m)" required>
                          </b-form-input>

                        </b-col>
                      </b-row>
                    <b-button class="btn-style1" @click.prevent="prev()"><i class="fa fa-chevron-left mr-2"></i> Previous</b-button>
                    <b-button class="btn-style1" @click.prevent="next()">Next <i class="fa fa-chevron-right ml-2"></i></b-button>
                  </div>
                  <!--End Step 2-->

                  <!--Step 3-->
                  <div v-show="step === 3">
                    <b-row>
                      <!--Images Upload-->
                      <b-col cols="12" md="6">
                        <h5>Add property image(s)</h5>
                        <vue-dropzone id="dropzone" ref="myVueDropzone" :options="config" v-on:vdropzone-success="uploadSuccess"
                        v-on:vdropzone-error="uploadError"></vue-dropzone>
                        <b-button class="btn-style1" @click="removeAllFiles">Remove all files <i class="fa fa-chevron-right ml-2"></i></b-button>                        
                          
                          <b-form-file type="file" id="lst_file" class="mt-3" v-on:change="onFileChange" ref="images-input" multiple accept="image/jpeg, image/png, image/gif">
                          <template slot="file-name" slot-scope="{ names }">
                            <!-- {{editPostForm.images}} -->
                            <b-badge variant="dark">{{ names[0] }}</b-badge>
                            <b-badge v-if="names.length > 1" variant="dark" class="ml-1">
                              + {{ names.length - 1 }} More images
                            </b-badge>
                          </template>
                      </b-form-file>
                      <b-button @click="clearFiles" variant="outline-danger" class="mb-5 mt-1">Delete images</b-button>
                      <!--End Images Upload-->

                      <!--PDF Upload-->
                      <h5>Add property PDF file(s)</h5>
                      <b-form-file class="mt-3" ref="pdf-input" multiple accept=".pdf">
                          <template slot="file-name" slot-scope="{ names }">
                            <b-badge variant="dark">{{ names[0] }}</b-badge>
                            <b-badge v-if="names.length > 1" variant="dark" class="ml-1">
                              + {{ names.length - 1 }} More pdf files
                            </b-badge>
                          </template>
                      </b-form-file>
                      <b-button @click="clearPdf" variant="outline-danger" class="mb-5 mt-1">Delete PDF</b-button>
                      <!--End PDF Upload-->


                      </b-col>
                      <b-col cols="12" md="6">
                        <!--Property Video Link-->
                        <h5>Property video link</h5>
                          <b-form-input id="input-url" v-model="editPostForm.video" :state="editPostForm.video.length >= 5" placeholder="Property video link"></b-form-input>
                        <!--End Property Video Link-->
                      </b-col>
                    </b-row>
                    <b-button class="btn-style1" @click.prevent="prev()"><i class="fa fa-chevron-left mr-2"></i> Previous</b-button>
                    <b-button class="btn-style1" @click.prevent="next()">Next <i class="fa fa-chevron-right ml-2"></i></b-button>
                  </div>
                  <!--End Step 3-->

                  <!--Step 4-->
                  <div v-show="step === 4">
                    <b-row >
                      <b-col cols="12" md="6">
                        <h5 class="mb-3">Promoted property status</h5>
                        <b-form-checkbox v-model="editPostForm.promoted" name="checkbox-promote" value="Promoted"
                          unchecked-value="Not Promoted" switch>
                          <b>{{ editPostForm.promoted }}</b>
                        </b-form-checkbox>
                      </b-col>

                      <b-col cols="12" md="6">
                        <h5 class="mb-3">Choose post property date & hour</h5>
                          <date-pick
                            v-model="editPostForm.post_at" :pickTime="true" :format="'YYYY-MM-DD HH:mm:ss'">
                          </date-pick>
                      </b-col>
                    </b-row>
                    <b-button class="btn-style1" @click.prevent="prev()"><i class="fa fa-chevron-left mr-2"></i> Previous</b-button>
                    <b-button class="btn-outline-style1 mt-3" block type="submit">Post Property</b-button>
                  </div>
                  <!--End Step 4-->
                </b-form>
              </b-row>
            </b-container>        
    
          
        </div>
      </div>
    </div>

    <!-- 用户的文章列表 -->
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> User Properties <small v-if="properties">(Total {{ properties._meta.total_items }} article, {{ properties._meta.total_pages }} Page)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 1 per page
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 5 per page
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 10 per page
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 20 per page
            </router-link>
            
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="properties" class="card-block g-pa-0" >

        <property v-for="(property, index) in properties.items" v-bind:key="index"
          v-bind:property="property"
          v-on:edit-property="onEditPost(property)"
          v-on:delete-property="onDeletePost(property)">
        </property>

      </div>
      <!-- End Panel Body -->
    </div>
  
    <!-- Pagination #04 -->
    <div v-if="properties">
      <pagination
        v-bind:cur-page="properties._meta.page"
        v-bind:per-page="properties._meta.per_page"
        v-bind:total-pages="properties._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import store from '../../store'
import Property from '../Base/Property'
import Pagination from '../Base/Pagination'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../../assets/bootstrap-markdown/js/marked.js'
import DatePick from 'vue-date-pick';
import SelectGroup from "../v-region/SelectGroup"
import ColumnGroup from "../v-region/ColumnGroup"
import vueDropzone from "vue2-dropzone";
export default {
  name: 'Properties',  // this is the name of the component
  components: {
    Property,
    Pagination,
    DatePick,
    SelectGroup,
    ColumnGroup,
    vueDropzone,
  },
  data () {
    return {
      fileCount : 0,
      base_url: this.$axios.defaults.baseURL,
      config: {url:this.$axios.defaults.baseURL +"/api/upload/",
              headers: { 'Authorization': 'Bearer ' + window.localStorage.getItem('madblog-token')},
              thumbnailWidth: 150,
              maxFilesize: 8,
              maxFiles: 8,
              addRemoveLinks: false,

              },
      num_files: null,  
      file: null,
      step:1,
      showDismissibleAlert: false,
      types: [{ text: 'Select property type', value: null }, 'Apartment', 'Studio', 'House', 'Commercial', 'Land', 'Office', 'Other'],
      contract: [{text: 'Select contract type', value: null}, 'Sale', 'Rent', "Other"],
      floors: [{ text: 'Select floor', value: null }, 'Ground floor', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '10/10'],
      bedrooms: [{ text: 'Select bedrooms number', value: null }, '1', '2', '3', '4', '5', '6', '7', '8', 'more than 8'],
      bathrooms: [{ text: 'Select bathrooms number', value: null }, '1', '2', '3', '4', '5', '6', '7', '8', 'more than 8'],
      directions: [{text: 'Select direction', value: null}, 'Đông', 'Tây', "Nam", "Bắc", "Đông-Bắc", "Tây-Bắc", "Đông-Nam", "Tây-Nam", "Khác"],

      sharedState: store.state,
      properties: '',

      editPostForm:{
        id: "",
        title : "",
        slug :"",
        price :"",

        promoted :"",
        features :[],
        purpose :null,
        type : null,
        area: null,
        images :[],
        bedroom :null,
        bathroom :null,
        city :"",
        city_slug :"",
        address :"",
        province:"",
        district:"",
        ward: "",
        total_area_sq_m: "",
        used_area_sq_m: "",
        direction: "",        
        agent_id :"",
        description :"",
        video :"",
        floor_plan :null,
        latitude :"",
        longtitude :'',
        nearby:"",
        created_at :"",
        updated_at :"",
        post_at: this.getCurrentTime(),
        views :0,
        errors: 0,
        titleError: null,
        bodyError: null
        
        },

    }
  },
  methods: {

    getCurrentTime(){
      var currentdate = new Date(); 
      var datetime = currentdate.getFullYear() + "-"
          + (currentdate.getMonth()+1)  + "-" 
          + currentdate.getDate() + " "  
          + currentdate.getHours() + ":"  
          + currentdate.getMinutes();
      return datetime    
    },

    regionChange(data) {
      // console.log(data)
      this.editPostForm.address = [data.area, data.city, data.province].map(function (e) {return (e != null? e.value :"");}).join(", "); 
      this.editPostForm.province = data.province.value;
      this.editPostForm.district = data.city.value;
      this.editPostForm.ward = data.area.value;

    },
    ////browse simple files
    onFileChange(e) {
      this.num_files = e.target.files || e.dataTransfer.files;
      if (!this.num_files.length)
          return;
      for (let i = 0; i < this.num_files.length; i++) {
              this.createFile(this.num_files[i]); //files[0]
          };
    },

    createFile(file) {
        let reader = new FileReader();
        let vm = this;
        reader.onload = (e) => {
            vm.file = e.target.result;
        };
        reader.readAsDataURL(file);
    },
    onSubmitUpdatePost2(e){
      e.preventDefault()
      var data = new FormData();
      let files = this.num_files;
      if (this.num_files)
      {
        for (let i = 0; i < this.num_files.length; i++) {
            data.append('file', document.getElementById('lst_file').files[i]);//files[0]
            
        };
      }
      this.$axios.post('/api/upload',data).then((response) => {

        this.editPostForm.images = (response.data);     
        this.onSubmitUpdatePost(e)
      }).catch((error) => console.log(error));
    },
    //// End browse simple files/////
    removeAllFiles () {
      this.$refs.myVueDropzone.removeAllFiles();
      this.editPostForm.images = [];
      console.log('After remove all files: ' + this.editPostForm.images);
      },
      
    afterComplete (file) {
      console.log('file.name', file.name)
      
      },
    uploadSuccess(file, response) {
      
      this.editPostForm.images.push(response);
      console.log('File Successfully Uploaded with file name: ' + this.editPostForm.images);
      console.log('file.name', file.name)
      //this.$refs.myVueDropzone.dropzone.files
      if ('undefined' !== typeof this.$refs.myVueDropzone.dropzone) {
        this.fileCount = this.editPostForm.images.length
      } else {
        this.fileCount = 0;
      }
      console.log("file count: ", this.fileCount)
    },
    uploadError(file, message) {
        console.log('An Error Occurred');
    },


    handleClick() {
      this.showDismissibleAlert = true
    },
    prev() {
    this.step--;
    },
    next() {
    this.step++;
    },
    onSubmit(evt) {
    evt.preventDefault()
    alert(JSON.stringify(this.editPostForm))
    },
    clearFiles() {
      this.$refs['images-input'].reset();
    },
    clearPdf() {
      this.$refs['pdf-input'].reset();
    },


    getProperties () {
      let page = 1
      let per_page = 10
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      const path = `/api/properties/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data


        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },

    getUserPosts (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/properties/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.properties = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onEditPost (property) {
      // Don't use object reference assignment: this.editPostForm = property
      // This is the same property object, and the user's operations in editPostForm will be bound to the property in both directions, and you will see that the blog under modal is also changing
      // If the user modifies some data, but clicks cancel, you must reload the blog list once in onResetUpdatePost(), otherwise the user will see the modified but unsubmitted asymmetric information
      console.log('assign', property.features)
      this.editPostForm = Object.assign({}, property)
      console.log('assign', this.editPostForm)
    },
    onSubmitUpdatePost () {
      console.log("this.form.features", this.editPostForm.features)
      this.editPostForm.errors = 0  // 重置
      //// Remove errors before each submission, otherwise errors will accumulate
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editPostForm.title) {
        this.editPostForm.errors++
        this.editPostForm.titleError = 'Title is required.'
        // / boostrap4 modal depends on jQuery and is not compatible with the two-way binding of vue.js. So you have to manually add warning styles and error messages
        $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
      } else {
        this.editPostForm.titleError = null
      }

      if (!this.editPostForm.address) {
        this.editPostForm.errors++
        this.editPostForm.bodyError = 'Address is required.'
        // / boostrap4 modal depends on jQuery and is not compatible with the two-way binding of vue.js. So you have to manually add warning styles and error messages
        // Add a warning style to the content of the bootstrap-markdown editor instead of adding it to #property_body
        $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
      } else {
        this.editPostForm.bodyError = null
      }

      if (this.editPostForm.errors > 0) {
        // When the form validation fails, the execution will not continue, that is, the back-end API will not be called through axios
        return false
      }

      const path = `/api/properties/${this.editPostForm.id}`
        const payload = {
          title : this.editPostForm.title,
          slug : this.editPostForm.slug,
          price :this.editPostForm.price,

          promoted :this.editPostForm.promoted,
          features : this.editPostForm.features,
          purpose :this.editPostForm.purpose,
          type : this.editPostForm.type,
          area: this.editPostForm.area,
          images : this.editPostForm.images,
          bedroom :this.editPostForm.bedroom,
          bathroom :this.editPostForm.bathroom,
          city :this.editPostForm.city,
          city_slug :this.editPostForm.city_slug,
          address : this.editPostForm.address,
          province: this.editPostForm.province,
          district: this.editPostForm.district,
          ward: this.editPostForm.ward,
          total_area_sq_m: this.editPostForm.total_area_sq_m,
          used_area_sq_m: this.editPostForm.used_area_sq_m,
          direction: this.editPostForm.direction,          
          agent_id :this.editPostForm.agent_id,
          description : this.editPostForm.description,
          video : this.editPostForm.video,
          floor_plan :this.editPostForm.floor_plan,
          latitude : this.editPostForm.latitude,
          longtitude : this.editPostForm.longtitude,
          nearby: this.editPostForm.nearby,
          // created_at: this.editPostForm.created_at,
          // updated_at: this.editPostForm.updated_at,
          // post_at: this.editPostForm.post_at,
          views : this.editPostForm.views,

        }
      this.$axios.put(path, payload)
        .then((response) => {
          //Hide Modal first
          $('#editPostModal').modal('hide')

          // handle success
          this.getUserPosts(this.$route.params.id || this.sharedState.user_id)
          this.$toasted.success('Successed update the property.', { icon: 'fingerprint' })
          this.editPostForm.title = '',
          this.editPostForm.description = '',
          this.editPostForm.address = ''
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.editPostForm.titleError = error.response.data.message[field]
              $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
            } else if (field == 'address') {
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
      // 先移除错误
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editPostModal').modal('hide')
      // this.getUserPosts(this.$route.params.id)
      this.$toasted.info('Cancelled, the property is not update.', { icon: 'fingerprint' })
    },
    onDeletePost (property) {
      this.$swal({
        title: "Are you sure?",
        text: "The operation will be completely deleted [ " + property.title + " ], Please be careful",
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
              // A dynamic parameter must be added, otherwise the User component will not re-execute getUser() and the Posts count will not be updated if the routing does not change
              this.$router.push({ path: this.$route.fullPath, query: { timestamp: Number(new Date()) } })
              // this.getUserPosts(this.$route.params.id || this.sharedState.user_id)
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
    }
  },
  created () {
    const user_id = this.$route.params.id || this.sharedState.user_id
    this.getUserPosts(user_id)
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#editPostFormBody").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // Use Font Awesome icon
        language: 'zh'
      })
    })
  },
  // When the route changes (such as changing the query parameters page and per_page) reload the data
  beforeRouteUpdate (to, from, next) {
    next()
    const user_id = to.params.id || this.sharedState.user_id
    this.getUserPosts(user_id)
  }
}
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
@import "./../../assets/scss/main";
#add-property {
  padding: 60px 0;
  .add-property-steps {
    display: flex;
    width: 100%;
    justify-content: space-between;
    margin-bottom: 60px;

    p {
      font-size: 18px;
      padding: 10px;
      border-radius: 10px;
      border: 1px solid $color1;
      width: 200px;
      text-align: center;
      margin-bottom: 35px;
    }

    .active-step {
      border: 1px dashed $color1;
      background: $color1-light;
      color: #000;
      box-shadow: 0 2px 15px 0 $color1-light;
    }
  }

  form {
    width: 100%;

    input, select, textarea {
      // margin: 20px 0;
      margin-bottom: 20px;
      padding-left: 20px;
      
    }

    .custom-checkbox {
      display: block;
      text-align: left;
      margin: 5px 0;
    }
  }
}

.modal-lg {
    max-width: 90% !important;
}

@media(max-width: 768px) {
  #add-property {
    padding: 30px;
    .add-property-steps {
      flex-direction: column;
      p {
        margin: 10px auto;
        width: 100%;
      }
    }
  }
}
</style>