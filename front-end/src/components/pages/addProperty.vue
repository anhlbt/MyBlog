<template>
    <div>
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
         <b-form @submit="onSubmitAddPost">
           <!--Step 1-->
           <div v-show="step === 1">
             <b-row>
               <b-col cols="12" md="6">

                  <b-form-input id="input-1" type="text" placeholder="Title" v-model="postForm.title"
                      :state="postForm.title.length >= 10"></b-form-input>

                  <b-form-input id="input-3" type="text" v-model="postForm.area" placeholder="Area or Address street..." required></b-form-input>
                  <b-form-select id="input-5" :options="contract" v-model="postForm.purpose" required></b-form-select>
                  <b-form-select id="input-7" :options="directions" v-model="postForm.direction" required></b-form-select>
                  <!-- <column-group :town="false" @values="regionChange"></column-group> -->

               </b-col>
               <b-col cols="12" md="6">
                <b-form-select id="input-4" :options="types" v-model="postForm.type" required></b-form-select>
                <b-form-input id="input-2" type="text" placeholder="Address" v-model="postForm.address" required></b-form-input>
                <select-group :town="false" @values="regionChange"></select-group>
                
                <b-form-input id="input-6" type="number" placeholder="Price" v-model="postForm.price" required>
                </b-form-input>
               </b-col>
               <b-form-textarea id="input-6" v-model="postForm.description" :state="postForm.description.length >= 20"
                placeholder="Description..."
                rows="4"
              ></b-form-textarea>
             </b-row>
              <b-button class="btn-style1" @click.prevent="next()">Next <i class="fa fa-chevron-right ml-2"></i></b-button>
           </div>
           <!--End Step 1-->

           <!--Step 2-->
            <div v-show="step === 2">
               <b-row>
                 <b-col cols="12" md="6">
                    <b-form-checkbox-group id="checkboxes-7" v-model="postForm.features">
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

                    <b-form-select id="input-8" :options="floors" v-model="postForm.floor_plan"></b-form-select>   
                    <b-form-select id="input-9" :options="bedrooms" v-model="postForm.bedroom" aria-placeholder="bedroom"></b-form-select>
                    <b-form-select id="input-9" :options="bathrooms" v-model="postForm.bathroom"></b-form-select>

                    <b-form-input id="input-10" type="number" v-model="postForm.total_area_sq_m" placeholder="Total Built Area (sq m)" min="0">
                    </b-form-input>
                     <b-form-input id="input-11" type="number" v-model="postForm.used_area_sq_m" placeholder="Used Area (sq m)" required>
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
                      <!-- {{postForm.images = names}} -->
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
                    <b-form-input id="input-url" v-model="postForm.video" :state="postForm.video.length >= 5" placeholder="Property video link"></b-form-input>
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
                  <b-form-checkbox v-model="postForm.promoted" name="checkbox-promote" value="Promoted"
                    unchecked-value="Not Promoted" switch>
                    <b>{{ postForm.promoted }}</b>
                  </b-form-checkbox>
                </b-col>

                <b-col cols="12" md="6">
                  <h5 class="mb-3">Choose post property date & hour</h5>
                  <date-pick
                      v-model="postForm.post_at" :pickTime="true" :format="'YYYY-MM-DD HH:mm'">
                  </date-pick>
                  <!-- <datetime type="datetime" format="yyyy-MM-dd HH:mm:ss" v-model="postForm.post_at"></datetime> -->
                  
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
</template>

<script>
import DatePick from 'vue-date-pick';
import SelectGroup from "../v-region/SelectGroup"
import ColumnGroup from "../v-region/ColumnGroup"
import Datetime from 'vue-datetime';
import vueDropzone from "vue2-dropzone";


    export default {
      components: {
             DatePick,
             SelectGroup,
            //  ColumnGroup,
            //  datetime: Datetime,
             vueDropzone

           },

      data() {
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
          // file: null,
          step:1,
          showDismissibleAlert: false,
          types: [{ text: 'Select property type', value: null }, 'Apartment', 'Studio', 'House', 'Commercial', 'Land', 'Office', 'Other'],
          contract: [{text: 'Select contract type', value: null}, 'Sale', 'Rent', "Other"],
          floors: [{ text: 'Select floor', value: null }, 'Ground floor', '1/10', '2/10', '3/10', '4/10', '5/10', '6/10', '7/10', '8/10', '9/10', '10/10'],
          bedrooms: [{ text: 'Select bedrooms number', value: null }, '1', '2', '3', '4', '5', '6', '7', '8', 'more than 8'],
          bathrooms: [{ text: 'Select bathrooms number', value: null }, '1', '2', '3', '4', '5', '6', '7', '8', 'more than 8'],
          directions: [{text: 'Select direction', value: null}, 'Đông', 'Tây', "Nam", "Bắc", "Đông-Bắc", "Tây-Bắc", "Đông-Nam", "Tây-Nam", "Khác"],


          postForm:{
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
            
            }
          }

        },
        methods:{
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
            this.postForm.address = [data.area, data.city, data.province].map(function (e) {return (e != null? e.value :"");}).join(", "); 
            data.province != null? this.postForm.province = data.province.value : this.postForm.province = null
            data.city != null? this.postForm.district = data.city.value : this.postForm.district = null
            data.area!= null ? this.postForm.ward = data.area.value : this.postForm.ward = null

          },
          //// upload images
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
          //onSubmitAddPost
          onSubmitAddPost2(e){
            e.preventDefault()
            
            var data = new FormData();
            let files = this.num_files;
            for (let i = 0; i < this.num_files.length; i++) {
                data.append('file', document.getElementById('lst_file').files[i]);//files[0]
                
            };
            
            this.$axios.post('/api/upload',data).then((response) => {
   
              this.postForm.images = (response.data);
              
              this.onSubmitAddPost(e)
            }).catch((error) => console.log(error));
          },
          // end upload images

          //listen vue-dropzone

          removeAllFiles () {
            this.$refs.myVueDropzone.removeAllFiles();
            this.postForm.images = [];
            console.log('After remove all files: ' + this.postForm.images);
            },
            
          afterComplete (file) {
            console.log('file.name', file.name)
            
            },
          uploadSuccess(file, response) {
            
            this.postForm.images.push(response);
            console.log('File Successfully Uploaded with file name: ' + this.postForm.images);
            console.log('file.name', file.name)
            //this.$refs.myVueDropzone.dropzone.files
            if ('undefined' !== typeof this.$refs.myVueDropzone.dropzone) {
              this.fileCount = this.postForm.images.length
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
          alert(JSON.stringify(this.postForm))
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


          //add new post
          onSubmitAddPost (e) {
            e.preventDefault()
            alert(JSON.stringify(this.postForm))
            
            // let tmp = this.upload()
            // this.upload()
            // console.log("this.postForm.images", this.postForm.images)
     

            this.postForm.errors = 0  // 重置

            if (!this.postForm.title) {
              this.postForm.errors++
              this.postForm.titleError = 'Title is required.'
            } else {
              this.postForm.titleError = null
            }

            if (!this.postForm.description) {
              this.postForm.errors++
            } else {
              this.postForm.bodyError = null
            }

            if (this.postForm.errors > 0) {
              // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
              return false
            }

            const path = '/api/properties'
            const payload = {
              title : this.postForm.title,
              slug : this.postForm.slug,
              price :this.postForm.price,

              promoted :this.postForm.promoted,
              features : this.postForm.features,
              purpose :this.postForm.purpose,
              type : this.postForm.type,
              area: this.postForm.area,
              images : this.postForm.images,
              bedroom :this.postForm.bedroom,
              bathroom :this.postForm.bathroom,
              city :this.postForm.city,
              city_slug :this.postForm.city_slug,
              address : this.postForm.address,
              province: this.postForm.province,
              district: this.postForm.district,
              ward: this.postForm.ward,
              total_area_sq_m: this.postForm.total_area_sq_m,
              used_area_sq_m: this.postForm.used_area_sq_m,
              direction: this.postForm.direction,
              agent_id :this.postForm.agent_id,
              description : this.postForm.description,
              video : this.postForm.video,
              floor_plan :this.postForm.floor_plan,
              latitude : this.postForm.latitude,
              longtitude : this.postForm.longtitude,
              nearby: this.postForm.nearby,
              // created_at: this.postForm.created_at,
              // updated_at: this.postForm.updated_at,
              // post_at: this.postForm.post_at,
              views : this.postForm.views,

            }
            this.$axios.post(path, payload)
              .then((response) => {
                // handle success
                this.getProperties()
                this.$toasted.success('Successed add a new post.', { icon: 'fingerprint' })
                this.postForm.title = '',
                this.postForm.description = '',
                this.postForm.price = ''
              })
              .catch((error) => {
                // handle error
                for (var field in error.response.data.message) {
                  if (field == 'title') {
                    this.postForm.titleError = error.response.data.message[field]
                  } else if (field == 'description') {
                    this.postForm.bodyError = error.response.data.message[field]
                  } else {
                    this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
                  }
                }
              })
          },
          onEditPost (post) {
            // Don't use object reference assignment： this.editPostForm = post
            // This is the same post object, and the user's operations in editPostForm will be bound to the post in both directions, and you will see that the blog under modal is also changing
            // If the user modifies some data, but clicks cancel, you must reload the blog list once in onResetUpdatePost(), otherwise the user will see the modified but unsubmitted asymmetric information
            this.editPostForm = Object.assign({}, post)
          },
          onSubmitUpdatePost () {
            this.editPostForm.errors = 0  //reset
            // Remove errors before each submission, otherwise errors will accumulate
            $('#editPostForm .form-control-feedback').remove()
            $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

            if (!this.editPostForm.title) {
              this.editPostForm.errors++
              this.editPostForm.titleError = 'Title is required.'
              // boostrap4 modal relies on jQuery and is not compatible with the two-way binding of vue.js. So you have to manually add warning styles and error messages
              $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
            } else {
              this.editPostForm.titleError = null
            }

            if (!this.editPostForm.body) {
              this.editPostForm.errors++
              this.editPostForm.bodyError = 'Body is required.'
              // 
              // Add a warning style to the contents of the bootstrap-markdown editor instead of #postFormBody
              $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
            } else {
              this.editPostForm.bodyError = null
            }

            if (this.editPostForm.errors > 0) {
              // When the form validation fails, the execution will not continue, that is, the back-end API will not be called through axios
              return false
            }

            const path = `/api/posts/${this.editPostForm.id}`
            const payload = {
              title: this.editPostForm.title,
              summary: this.editPostForm.summary,
              body: this.editPostForm.body
            }
            this.$axios.put(path, payload)
              .then((response) => {
                // Hide first Modal
                $('#editPostModal').modal('hide')

                // handle success
                this.getPosts()
                this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
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
            //Remove errors first
            $('#editPostForm .form-control-feedback').remove()
            $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
            // Hide first Modal
            $('#editPostModal').modal('hide')
            // this.getPosts()
            this.$toasted.info('Cancelled, the post is not update.', { icon: 'fingerprint' })
          },
          onDeletePost (post) {
            this.$swal({
              title: "Are you sure?",
              text: "This operation will be completely deleted [ " + post.title + " ], Please be careful",
              type: "warning",
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Yes, delete it!',
              cancelButtonText: 'No, cancel!'
            }).then((result) => {
              if(result.value) {
                const path = `/api/posts/${post.id}`
                this.$axios.delete(path)
                  .then((response) => {
                    // handle success
                    this.$swal('Deleted', 'You successfully deleted this post', 'success')
                    // this.$toasted.success('Successed delete the post.', { icon: 'fingerprint' })
                    this.getPosts()
                  })
                  .catch((error) => {
                    // handle error
                    console.log(error.response.data)
                    this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
                  })
              } else {
                this.$swal('Cancelled', 'The post is safe :)', 'error')
              }
            })
          }



        },

      // created(){
      //   this.getToken()
      // },

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