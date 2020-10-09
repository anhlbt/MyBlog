<template>                
    <!-- In the News Section -->
    <section class="itn-section">
        <!-- ITN Title Box -->
        <div class="itn-title-box">
            <!-- TV section Title Flag -->
            <div class="itn-title-flag">
                <!-- TV section Title Text -->
                <h1 class="itn-title-text">In the news</h1>
                <!-- /end of TV section Title Text -->
            </div>
            <!-- /end of TV section Title Flag -->
        </div>
        <!-- /end of ITN Title Box -->

        <!-- ITN Card Wrapper -->
        <div class="itn-content-card-wrapper">
            <div class="itn-content-card" v-for="post in posts.items" v-bind:key="post.id">
                <!-- ITN Content Card Image -->
                <div class="itn-content-img-wrapper">
                    <img class="itn-content-img" v-bind:src="post.image">
                </div>
                <!-- /end of ITN Content Card Image -->

                <!-- ITN Details Wrapper -->
                <div class="itn-details-wrapper">

                    <!-- ITN Content Details category-->
                    <div class="itn-content-category">
                        <a class="itn-content-category-link">
                            <div class="itn-content-category-text">
                                {{post.topic}}
                            </div>
                        </a>
                    </div>
                    <!-- /end of ITN Content Details Category -->
                    <!-- ITN Content Wrapper -->
                    <div class="itn-content-wrapper">
                        <!-- ITN Content Headline -->
                        <div class="itn-content-headline">
                            <a class="itn-content-link">
                                <div class="itn-content-text">
                                    {{post.title}}
                                </div>
                            </a>
                        </div>
                        <!-- ITN Content Headline -->

                        <!-- ITN Content Details -->
                        <div class="itn-content-details">
                            <!-- ITN Content Details des-->
                            <div class="itn-content-des">
                                <a class="itn-content-des-link">
                                    <div class="itn-content-des-text">
                                        <!-- {{post.summary}} -->
                                    </div>
                                </a>
                            </div>
                        </div>
                        <!-- /end of ITN Content Details -->
                    </div>
                    <!-- /end of ITN Content Wrapper -->

                </div>
                <!-- /end of ITN Details Wrapper -->

            </div>
        </div>
        <!-- /end of ITN Card Wrapper -->

    </section>
    <!-- /end of In the News Section -->
</template>

<script>
export default {
    data:function() {
        return {
            posts: null,
            aa:"hello world",
            
        }
    },

    methods:{
      getPosts () {
        let page = 1
        let per_page = 10
        //get all post
        //const path = `/api/posts/?page=${page}&per_page=${per_page}`
        // get all topics except ebook
        const path = `/api/posts/?page=${page}&per_page=${per_page}`
        this.$axios.get(path)
          .then((response) => {
            // handle success
            this.posts = response.data

          })
          .catch((error) => {
            // handle error
            console.log(error.response.data)
          })
      }      

    },
  mounted() {
      this.getPosts()
    },
    
}

</script>

<style lang="scss">
@import "./../assets/scss/main";

/* Smartphones (portrait and landscape) ----------- */
@media only screen and (min-device-width: 320px) and (max-device-width: 480px) {
.itn-section {
    grid-row: 31 / 33;
    grid-column: 1 / -1;
    margin: 1em 0;
  }
  .itn-title-box {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1em;
    background-color: $white;
  }
  .itn-title-flag {
    display: flex;
    justify-content: center;
    align-items: center;
    font-style: italic;
    background: $third-color;
    color: $white;
    height: 2em;
  }
  .itn-title-text {
    text-transform: uppercase;
    padding: 0 15px;
    font-size: 1.0625rem;
    font-family: $font-bold;
    letter-spacing: 0.12em;
    padding-top: 3px;
  }
  .itn-content-card-wrapper {
    margin: 1em 0 0 0;
  }
  .itn-content-card {
    display: flex;
    flex-direction: column;
    margin-bottom: 1em;
    padding-bottom: 1em;
    border-bottom: 0.8px solid $border-bottom;
  }
  .itn-content-img-wrapper {
  }
  .itn-content-img {
    width: 100%;
  }
  .itn-details-wrapper {
    padding: 0 1em;
  }
  .itn-content-category {
  }
  .itn-content-category-link {
  }
  .itn-content-category-text {
    font-family: $font-bold;
    font-size: 0.8125rem;
    letter-spacing: 1.4px;
  }
  .itn-content-wrapper {
  }
  .itn-content-headline {
    padding: 0.3em 0;
  }
  .itn-content-headline:hover {
    text-decoration: underline;
  }
  .itn-content-link {
  }
  .itn-content-text {
    font-family: $font-bold;
    font-size: 1.75rem;
    line-height: 1.875rem;
    letter-spacing: 0.01em;
  }
  .itn-content-details {
  }
  .itn-content-des {
  }
  .itn-content-des-link {
  }
}

/* Desktops and laptops ----------- */
@media only screen and (min-width: 1224px) {
.itn-section {
    grid-row: 24 / 27;
    grid-column: 2 / 11;
    margin: 1em 0;
  }
  .itn-title-box {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1em;
    background-color: $white;
  }
  .itn-title-flag {
    display: flex;
    justify-content: center;
    align-items: center;
    font-style: italic;
    background: $third-color;
    color: $white;
    height: 2em;
    width: 30%;
  }
  .itn-title-text {
    text-transform: uppercase;
    padding: 0 15px;
    font-size: 1.0625rem;
    font-family: $font-bold;
    letter-spacing: 0.12em;
    padding-top: 3px;
  }
  .itn-content-card-wrapper {
    margin: 1em 0 0 0;
  }
  .itn-content-card {
    display: flex;
    flex-direction: row;
    margin-bottom: 1em;
    padding-bottom: 1em;
    border-bottom: 0.8px solid $border-bottom;
  }
  .itn-content-img-wrapper {
  }
  .itn-content-img {
    max-width: 196px;
    height: 130px;
  }
  .itn-details-wrapper {
    padding: 0 1em;
  }
  .itn-content-category {
  }
  .itn-content-category-link {
  }
  .itn-content-category-text {
    font-family: $font-bold;
    font-size: 0.8125rem;
    letter-spacing: 1.4px;
  }
  .itn-content-wrapper {
  }
  .itn-content-headline {
    padding: 0.3em 0;
  }
  .itn-content-headline:hover {
    text-decoration: underline;
  }
  .itn-content-link {
  }
  .itn-content-text {
    font-family: $font-bold;
    font-size: 1.25rem;//1.75
    line-height: 1.875rem;
    letter-spacing: 0.01em;
  }
  .itn-content-details {
  }
  .itn-content-des {
  }
  .itn-content-des-link {
  }
}
</style>
