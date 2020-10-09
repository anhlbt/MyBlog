<template>
  <div>
    <div>
      <audio id="audiofile" class="vue-audio-player" :src="file" controls></audio>
      <div id="subtitles"></div>
        <!-- {{
          audioSync({
              audioPlayer: 'audiofile', // the id of the audio tag
              subtitlesContainer: 'subtitles', // the id where subtitles should show
              subtitlesFile: '../assets/sample/tuned.vtt' // the path to the vtt file
          })
        }}    -->


    </div>
    
    <div>
      <h1>My personal Daily News</h1>
      <!--<img src="./assets/logo.png">-->
      <!-- <FilterForm :getPosts="getPosts" /> -->
      <!-- <NewsList :results="results" /> -->
      
    </div>
  </div>  
</template>



<script>
import axios from 'axios'
import Vue from 'vue'
import NewsList from './test/NewsList'
import FilterForm from './test/FilterForm'
import audioSync from 'audio-sync-with-text'
import VueAudio from 'vue-audio';
import convertVttToJson from 'vtt-json'
import vttToJson from "vtt-to-json"
import readTextFile from 'read-text-file'

// Vue.use(convertVttToJson)
// import ScrollLoader from './test/ScrollLoader'



const NYTBaseUrl = "https://api.nytimes.com/svc/topstories/v2/";
const ApiKey = "rO1Elou8Lw3AtxdM1wfRMGbiTC6KaAAO";


function buildUrl (url) {
    return NYTBaseUrl + url + ".json?api-key=" + ApiKey
}

 

export default {
  name: 'Test2',
  components: {
      NewsList,
      FilterForm,
      'vue-audio': VueAudio,
      // audioSync
      // ScrollLoader
  },
  data () {
    return {
        file:'../assets/audio/sample.mp3', //
        results: [],
        text:"",
        subtitlesFile: '../assets/audio/tuned.vtt'
    }
  },


  mounted() {
      const player = document.querySelector('.vue-audio-player');
      player.src = require('../assets/audio/sample.mp3');
      player.load();   
      var audioPlayer = document.querySelector('#audiofile');
      var subtitles = document.querySelector('#subtitles');
      var syncData = [];
      var rawSubTitle = "";
      // var convertVttToJson = require('vtt-json');   
      // audioPlayer.addEventListener('timeupdate', function() { alert("HOVER2") })

      
      // this.$el.querySelector('#audiofile').addEventListener('timeupdate', function() { alert("click") })
      // this.getPosts('home');
      // var x = new audioSync({
      //         audioPlayer: 'audiofile', // the id of the audio tag
      //         subtitlesContainer: 'subtitles', // the id where subtitles should show
      //         subtitlesFile: '../assets/audio/tuned.vtt' // the path to the vtt file
      //     }($(window), $(document)))
  },
  methods: {
      getPosts(section) {
          let url = buildUrl(section);
          axios.get(url).then((response) => {
              this.results = response.data.results;
          }).catch( error => { console.log(error); });
      },


    
  }
}
</script>

<style lang="scss">
#test {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
