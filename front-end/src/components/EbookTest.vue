<template>
  <div>    
    <div class="naturallanguageform">
      <div class="nlfinner">
        <p class="line">
          <audio  style="width:100%;" :src="audio_file" ref="audiofile" controls preload="auto" autobuffer></audio>
          <a href="javascript:void(0)" title="repeat" id="b_repeat" v-on:click="repx()"><br></a>
        </p>
        <p class="line subs" ref="subtitles"></p>
      </div>
    </div>
    
  </div>  
</template>



<script>
// import './app.js' 
var syncData = null;
var audioPlayer = null;
var subtitles = null;
var audio = null;
var rep = true;



export default {
  name: 'EbookTest',
  components: { 
  },
  props:{
    json_ebook:{
      type:Array,

    }, 
    audio_file:{
      type: String,

    },

  },
  
  data () {
    return {
      
    }
  },
  created(){
    syncData = this.json_ebook;
  },

  mounted() {
      
      this.repx();
      syncData = this.json_ebook;
      audio = this.audio_file;
      audioPlayer = this.$refs.audiofile;
      audioPlayer.src = this.audio_file;
      audioPlayer.load()
      subtitles = this.$refs.subtitles;

//------------- subtitle version--------------------
      // audioPlayer.addEventListener("timeupdate", function(e){
      //     syncData.forEach(async function(d, i){
      //         var el;
      //         if( (audioPlayer.currentTime*1) >= d.begin && (audioPlayer.currentTime*1) < d.end ) {
                  
      //             while(subtitles.hasChildNodes())
      //                 subtitles.removeChild(subtitles.firstChild)
                      

      //             el = document.createElement('span');
      //             el.innerText = syncData[i].lines[0];
      //             subtitles.appendChild(el);
      //             el = document.createElement('p');
      //             el.innerText = syncData[i].lines[0];
      //             subtitles.appendChild(el);
      //             await sleep(d.end-d.begin-0.150);
      //             if (d.re > 0 && (audioPlayer.currentTime*1) > d.end-0.200) {
      //                 d.re -= 0.001;
      //                 audioPlayer.currentTime = d.begin/1;
      //             }
      //         }
      //     });
      // });
//---------------------- hilight version---------------------------
      this.createSubtitle();

      audioPlayer.addEventListener('timeupdate', this.onTimeUpdateListener) //@timeupdate="onTimeUpdateListener"

      audioPlayer.addEventListener("seeked", function() {
        syncData.forEach(function(element, index, array){
          if(audioPlayer.currentTime >= element.begin && audioPlayer.currentTime <= element.end )
          {
            if(index>5 && subtitles.children.length > 5){subtitles.children[index-3].scrollIntoView()}
            // else{audioPlayer.scrollIntoView()}
            
          }
        });
      });

      // audioPlayer.addEventListener("timeupdate", function(e){
      //     syncData.forEach(function(element, index, array){
      //         if( audioPlayer.currentTime >= element.begin && audioPlayer.currentTime <= element.end ){
      //           subtitles.children[index].style.background = 'green';//initial
      //           // setTimeout(subtitles.children[index>5?index-5:index].scrollIntoView(), 5000);
      //           // subtitles.children[index].setAttribute("class", "span");
      //           // subtitles.children[index].style.fontWeight = 'bold';
      //           // setTimeout(function(){subtitles.children[index].style.fontWeight = "initial"; }, (audioPlayer.currentTime -element.begin )*1000);
      //           // setTimeout(function(){ subtitles.children[index].style.background = 'black'; }, (audioPlayer.currentTime -element.begin)*1000);

      //         }
      //         else
      //         {
      //           // subtitles.children[index].style.fontWeight = 'normal';
      //           subtitles.children[index].style.background = 'black';
      //         }                  
      //     });
      // });  

      $('.tx_trg').click(function() {
        // alert("hello there" + $(this).attr('id').split("_").pop());
        var i = $(this).attr('id').split("_").pop(); // get id of string
        audioPlayer.currentTime = syncData[i].begin;
        $(this).addClass($(this).attr('pers'));
        audioPlayer.play();
      });   


      audioPlayer.addEventListener('ended',function() {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        },
        false);

  },// ended mounted

  methods: {
    onTimeSeekedListener(event){
      for (var index = 0; index < syncData.length; index++)
      {
        var element = syncData[index]
        if( audioPlayer.currentTime >= element.begin && audioPlayer.currentTime <= element.end )
          {
            if(index>5){subtitles.children[index-3].scrollIntoView()}
            else{audioPlayer.scrollIntoView()}
            
          }
      }
            
    },

    onTimeUpdateListener(event)
    {
      // syncData.forEach(function(element, index, array)
      for (var index = 0; index < syncData.length; index++)
      {
          var element = syncData[index]
          if(audioPlayer.currentTime >= element.begin && audioPlayer.currentTime <= element.end )
          {
            subtitles.children[index].style.background = 'green';//initial
          }
          else
          {
            // subtitles.children[index].style.fontWeight = 'normal';
            subtitles.children[index].style.background = 'black';
          }              
      };
      
    },

    createSubtitle()
    {
        var element;
        for (var i = 0; i < syncData.length; i++) {
            element = document.createElement('a');
            element.className="tx_trg";
            element.setAttribute("id", "c_" + i);
            element.innerText = syncData[i].lines[0] + " ";
            subtitles.appendChild(element);
        }
    },

    repx() {
      rep=!rep;
      initr(rep?1:0);
      var repeater = document.querySelector("#b_repeat");
      // console.log(repeater)
      repeater.removeChild(repeater.firstChild);
      var xmlns = "http://www.w3.org/2000/svg";
      var img = document.createElementNS(xmlns, "svg");
      s(img,"width",48);
      s(img,"height",48);
      s(img,"fill-rule","evenodd");
      s(img,"clip-rule","evenodd");
      var path = document.createElementNS(xmlns, "path");
      s(path,"transform","scale(2,2)");
      s(path,"fill","#FFF");
      s(path,"d",rep?"M6 18h12c3.311 0 6-2.689 6-6s-2.689-6-6-6h-12.039c-3.293.021-5.961 2.701-5.961 6 0 3.311 2.688 6 6 6zm12-10c-2.208 0-4 1.792-4 4s1.792 4 4 4 4-1.792 4-4-1.792-4-4-4z":"M18 18h-12c-3.311 0-6-2.689-6-6s2.689-6 6-6h12.039c3.293.021 5.961 2.701 5.961 6 0 3.311-2.688 6-6 6zm0-10h-12c-2.208 0-4 1.792-4 4s1.792 4 4 4h12c2.208 0 4-1.792 4-4 0-2.199-1.778-3.986-3.974-4h-.026zm-12 1c1.656 0 3 1.344 3 3s-1.344 3-3 3-3-1.344-3-3 1.344-3 3-3z");
      img.appendChild(path);
      repeater.appendChild(img);

    },
    


  }
}

//-------------not used-----------------
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function initr(n) {
  syncData.forEach(function(d, i){d.re=n})
}
function s(d,a,v) {
  d.setAttributeNS(null, a, v);
}
</script>

<style lang="scss">

.span {

  font-weight: bold;
  text-transform:lowercase;
	transition: font-weight .5s,  ease-in .5s;
}

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

.bodybook {
	// background: #000;
	font-family: 'Accanthis', sans-serif;
	font-size: 1.5em;
	line-height: 1.1em;
	letter-spacing: .05em;
	margin: 0
}
body {
  background: #000;
}
// header,
// div.headerclone {
// 	background: #46ABB6;
// 	padding: 20px 0
// }

h1.heading {
	line-height: 1.1em;
	text-align: center;
	font-weight: 400;
	font-size: 1.7em;
	color: #EDF7F2
}

div.naturallanguageform {
	// width: 900px;
	margin: 2% auto;
	max-width: 95%;
	min-height: 400px;
	border-radius: 5px;
	color: #FFF;
	font-size: 1.2em
}

div.nlfinner {
	width: 96%;
	padding: 2%
}

p.line {
	line-height: 1.5em;
	font-weight: 200;
  text-align: justify;
}

input.textinput {
	background: none;
	border: 0;
	border-bottom: 1px dashed #EEE;
	width: auto;
	font-size: 1em;
	color: #B5E655;
	font: inherit
}

input.textinput:focus {
	outline: none;
	border-bottom: 1px dashed #D00
}

::-webkit-input-placeholder {
	color: #B5E655;
	font-weight: 300
}

:-moz-placeholder {
	color: #B5E655;
	opacity: 1
}

::-moz-placeholder {
	color: #B5E655;
	opacity: 1
}

:-ms-input-placeholder {
	color: #B5E655
}

select.dropdown {
	font-size: 1em;
	color: #B5E655;
	border: none;
	border-bottom: 1px dashed #EFEFEF;
	-webkit-appearance: none;
	-moz-appearance: none;
	background: none;
	width: auto;
	text-indent: .01px;
	box-shadow: none;
	font: inherit
}

select.dropdown:focus {
	outline: none;
	border-bottom: 1px dashed #D00
}

button.button {
	background: #388891;
	border: none;
	padding: 10px 50px;
	font-size: 1em;
	color: #FFF;
	display: block;
	margin: 40px auto 0;
	cursor: pointer;
	font: inherit
}

.subs span {
	color: #FFF;
	// background-color: #000;
	font-style: normal;
  text-align: justify;
}

p {
	font-style: italic;
  font-family: 'Courier', Helvetica, Arial, sans-serif;
}
</style>
