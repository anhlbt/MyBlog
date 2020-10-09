<template>
<div id="app">
  <h1 class="title-text">Vue-Scroll-Loader</h1>
  <div class="images-container">
    <div class="images-item" v-for="(image,index) of images" :key="index">
      <div class="images-card">
        <img class="images-card__image" :src="image.urls.small" @load="masks.push(index)">
        <div class="images-card__mask" :style="{'background-color':image.color}" v-if="!masks.includes(index)"></div>
      </div>
    </div>
  </div>

  <scroll-loader :loader-method="getImageList" :loader-disable="disable">
  </scroll-loader>
</div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import ScrollLoader from 'vue-scroll-loader'
Vue.use(ScrollLoader)

export default {
  name: 'TestScroll',
  data () {
    return {
      disable: false,
      page: 1,
      pageSize: 30,
      images: [],
      masks: []
    }
  },
  methods: {
    getImageList () {
      axios.get('https://api.unsplash.com/photos', {
        params: {
          page: this.page++,
          per_page: this.pageSize,
          client_id: 'e874834b096dcd107c232fe4b0bb521158b62e486580c988b0a75cb0b77a2abe'
        }
      }).then(res => {
        res.data && (this.images = [...this.images, ...res.data])
      }).catch(error => {
        console.log(error)
      })
    }
  },
  watch: {
    page (value) {
      this.disable = value > 10
    }
  }
}
</script>

<style lang="css" scoped>
.images-item{
  animation-duration: 1s;
  animation-fill-mode: both;
  animation-name: fadeInUp;
}


.title-text {
  padding: 30px 0;
  text-align: center;
  color: #666666;
}

.images-container {
  width: 100vw;
  max-width: 1200px;
  padding-bottom: 30px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
}

.images-item {
  width: 33.333%;
  padding: 1%;
}

.images-card {
  width: 100%;
  height: 0;
  padding-bottom: 70%;
  position: relative;
}

.images-card__image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  vertical-align: middle;
}
.images-card__mask{
  position: absolute;
  z-index: 9;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: .8;
}
.copyright-container__link {
  display: flex;
  padding: 30px 0;
  justify-content: center;
  align-items: center;
  color: #666666;
  text-decoration: none;
}
.copyright-container__icon{
  width: 20px;
  margin-left: 10px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10%) scale(0.9);
  }

  to {
    opacity: 1;
    transform: translateY(0%) scale(1.0);
  }
}
</style>
