<template>
  <div class="media g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-20">
    <router-link v-bind:to="{ path: `/user/${property.author.id}` }" v-bind:title="property.author.name || property.author.username">
      <span v-if="property.is_new" class="d-inline-block g-pos-rel">
        <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
        <img class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="property.author.avatar" v-bind:alt="property.author.name || property.author.username">
      </span>
      <img v-else class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="property.author.avatar" v-bind:alt="property.author.name || property.author.username">
    </router-link>
    
    <div class="media-body">
      <div class="g-mb-15">
        <h5 class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${property.author.id}` }" class="g-text-underline--none--hover">{{ property.author.name || property.author.username }}</router-link> <span class="h6">Posted an article<router-link v-bind:to="{ name: 'PropertyDetail', params: { id: property.id } }" class="g-text-underline--none--hover">《<span v-html="property.title"></span>》</router-link></span></h5>
        <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(property.created_at).format('YYYY/MM/DD HH:mm:ss') }}</span>
      </div>

      <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
      v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
      <vue-markdown
        :source="property.summary"
        class="markdown-body g-mb-15"
        v-highlight>
      </vue-markdown>

      <div class="d-flex justify-content-start">
        <ul class="list-inline mb-0">
          <li class="list-inline-item g-mr-20">
            <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
              <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ property.views }}
            </a>
          </li>
          <li class="list-inline-item g-mr-20">
            <router-link v-bind:to="{ path: `/property/${property.id}#like-property` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-heart g-pos-rel g-top-1 g-mr-3"></i> {{ property.likers_count }}
            </router-link>
          </li>
          <li class="list-inline-item g-mr-20">
            <router-link v-bind:to="{ path: `/property/${property.id}#comment-list-wrap` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-3"></i> {{ property.comments_count }}
            </router-link>
          </li>
        </ul>
        <ul class="list-inline mb-0 ml-auto">
          <li class="list-inline-item g-mr-5">
            <router-link v-bind:to="{ name: 'PropertyDetail', params: { id: property.id } }" class="btn btn-xs u-btn-outline-primary">Read the full text</router-link>
          </li>
          <li v-if="property.author.id == sharedState.user_id || sharedState.user_perms.includes('admin')" class="list-inline-item g-mr-5">
            <button v-on:click="$emit('edit-property')" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editPostModal">edit</button>
          </li>
          <li v-if="property.author.id == sharedState.user_id || sharedState.user_perms.includes('admin')" class="list-inline-item">
            <button v-on:click="$emit('delete-property')" class="btn btn-xs u-btn-outline-red">delete</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'

export default {
  props: ['property'],
  components: {
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state
    }
  },

  /*
  computed: {
    leftBrdColor: function () {
      const colors = ['primary', 'blue', 'red', 'purple', 'orange', 'yellow', 'aqua', 'cyan', 'teal', 'brown', 'pink', 'black']
      let index = Math.floor((Math.random() * colors.length))
      return 'g-brd-' + colors[index] + '-left'
    }
  }
  */
}
</script>