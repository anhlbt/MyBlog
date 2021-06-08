<template>
  <div class="container">
    <h1>{{ $t('auth.login.sign-in') }}</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
          <div class="form-group" v-bind:class="{'u-has-error-v1': loginForm.usernameError}">
            <label for="username">{{ $t('auth.login.username') }}</label>
            <input type="text" v-model="loginForm.username" class="form-control" id="username" placeholder="">
            <small class="form-control-feedback" v-show="loginForm.usernameError">{{ loginForm.usernameError }}</small>
          </div>
          <div class="form-group" v-bind:class="{'u-has-error-v1': loginForm.passwordError}">
            <label for="password">{{ $t('auth.login.password') }}</label>
            <input type="password" v-model="loginForm.password" class="form-control" id="password" placeholder="">
            <small class="form-control-feedback" v-show="loginForm.passwordError">{{ loginForm.passwordError }}</small>
          </div>
          <button type="submit" class="btn btn-primary">{{ $t('auth.login.sign-in') }}</button>
        </form>
      </div>
    </div>
    <br>
    <p>{{ $t('auth.login.new-user') }} <router-link to="/register">{{ $t('auth.login.click-register') }}</router-link></p>
    <p>
        {{ $t('auth.login.forgot-pass') }}
        <router-link v-bind:to="{ name: 'ResetPasswordRequest' }">{{ $t('auth.login.click-reset') }}</router-link>
    </p>
    <!-- <v-facebook-login app-id="510247036061913"></v-facebook-login> -->
    <div class="login">
      <v-facebook-login
        v-model="model"
        app-id="510247036061913"
        @sdk-init="handleSdkInit"
      ></v-facebook-login>
      <button @click="getPosts()">GET POSTS</button>
    </div>
  </div>
</template>

<script>
import store from '../../store'
import VFacebookLogin from 'vue-facebook-login-component'
export default {
  name: 'Login',  //this is the name of the component
  components:
  {
    VFacebookLogin
  },

  data () {
    return {

      FB: {},
      model: {},
      scope: {},
      userId: null,

      sharedState: store.state,
      loginForm: {
        username: '',
        password: '',
        errors: 0,  // Whether the form is validated on the front end, 0 means there is no error, and the validation is passed
        usernameError: null,
        passwordError: null
      }
    }
  },
  methods: {

    getUserId() {
      return new Promise((resolve) => {
        this.FB.api("/me", (response) => {
          this.userId = response.id;
          resolve(this.userId);
          console.log(this.userId);
        });
      });
    },
    getCertainGroup() {
      this.FB.api("/548739628937538", (response) => {
        console.log(response);
      });
    },
    getUserGroups(userId) {
      this.FB.api(`/${userId}/groups`, (response) => {
        console.log(response);
      });
    },
    getPosts() {
      console.log("model status", this.model)
      console.log("access token ", this.FB.getAuthResponse())
      this.getUserId().then((userId) => {
        this.getUserGroups(userId);
      });
      this.getCertainGroup();
      

      console.log(this.FB.getUserID())
      let UID = this.FB.getUserID()
      console.log(this.FB.api(
        UID,
        {'fields': 'id,name,email,picture'},
        function (response) {
          if (response && !response.error) {
            /* handle the result */
            console.log(response)
          }
        }
      ))
    },
    testData(scope) {
      console.log(scope.connected);
    },
    // handleSdkInit({ FB, scope }) {
    //   this.FB = FB;
    //   this.scope = scope;
    // },
    handleSdkInit ({ FB, scope }) {
      this.FB = FB
      this.scope = scope
      console.log(this.FB.getUserID())
      let UID = this.FB.getUserID()
      console.log(this.FB.api(
        UID,
        {'fields': 'id,name,email'},
        function (response) {
          if (response && !response.error) {
            /* handle the result */
            console.log(response)
          }
        }
      ))
    },

    onSubmit (e) {
      this.loginForm.errors = 0  // Reset
      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        // When the form validation fails, the execution will not continue, that is, the back-end API will not be called through axios
        return false
      }

      const path = '/api/tokens'
      // Axios needs to set the auth attribute in config to implement Basic Auth.
      this.$axios.post(path, {}, {
        auth: {
          'username': this.loginForm.username,
          'password': this.loginForm.password
        }
      }).then((response) => {
          // handle success
          window.localStorage.setItem('madblog-token', response.data.token)
          store.loginAction()

          this.$toasted.success(`Welcome ${this.sharedState.user_name}!`, { icon: 'fingerprint' })

          if (typeof this.$route.query.redirect == 'undefined') {
            this.$router.push('/')
          } else {
            this.$router.push(this.$route.query.redirect)
          }
        })
        .catch((error) => {
          // handle error
          // console.log('failed', error.response);
          if (typeof error.response != 'undefined') {
            if (error.response.status == 401) {
              this.loginForm.usernameError = 'Invalid username or password.'
              this.loginForm.passwordError = 'Invalid username or password.'
            } else {
              console.log(error.response)
            }
          }
        })
    }
  }
}
</script>