import Vue from 'vue'
import axios from 'axios'
import router from './router'
import store from './store'


// Basic configuration
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'http://116.85.19.23:5000';
} else {
  axios.defaults.baseURL = 'https://0.0.0.0:5000'; //172.16.2.215   192.168.1.239  localhost
}
// axios.defaults.baseURL = 'http://127.0.0.1:5000'
// axios.defaults.timeout = 5000  //Timeout (ms)
// axios.defaults.retry = 2  // number of retries
// axios.defaults.retryDelay = 100  // Time between retries (milliseconds)

// Request interceptor
// Add a request interceptor
axios.interceptors.request.use(function (config) {
  // Do something before request is sent
  const token = window.localStorage.getItem('madblog-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, function (error) {
  // Do something with request error
  return Promise.reject(error)
})


// Add a response interceptor
axios.interceptors.response.use(function (response) {
  // Do something with response data
  return response
}, function (error) {
  // Do something with response error
  if (error.response) {
    // Match different response codes
    switch (error.response.status) {
      case 401:
        //Clear Token and authenticated status
        store.logoutAction()
        // Jump to login page
        if (router.currentRoute.path !== '/login') {
          Vue.toasted.error('401: Authentication has expired, please log in first', { icon: 'fingerprint' })
          router.replace({
            path: '/login',
            query: { redirect: router.currentRoute.path },
          })
        }
        break

      case 403:
        Vue.toasted.error('403: Forbidden', { icon: 'fingerprint' })
        // router.back()
        break

      case 404:
        Vue.toasted.error('404: Not Found', { icon: 'fingerprint' })
        router.back()
        break

      case 405:
        Vue.toasted.error('405: Method Not Allowed', { icon: 'fingerprint' })
        router.back()
        break

      case 500:  // You can’t get 500 errors at all, because CORs won’t come
        Vue.toasted.error('500: Oops... INTERNAL SERVER ERROR', { icon: 'fingerprint' })
        router.back()
        break
    }
  } else if (error.request) {
    console.log(error.request)
    Vue.toasted.error('The request has not been sent to Flask API，because OPTIONS get error', { icon: 'fingerprint' })
  } else {
    console.log('Error: ', error.message)
  }
  console.log(error.config)

  return Promise.reject(error)
})

export default axios