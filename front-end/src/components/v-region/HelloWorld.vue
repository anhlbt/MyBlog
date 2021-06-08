<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <div>
      <!-- <v-region type="select" @values="regionChange" lang="en"></v-region> -->
      <select-group :town="false" @values="regionChange"></select-group>
      <column-group :town="false" @values="regionChange"></column-group>
      
      
    </div>
  </div>
</template>

<script>
import SelectGroup from "./SelectGroup"
import ColumnGroup from "./ColumnGroup"


export default {
  name: 'HelloWorld',

  components:{
    SelectGroup,
    ColumnGroup,

  },
  props: {
    msg: String
  },
  methods: {
    //receive selected region data
    regionChange (data) {
      console.log(data)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
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
