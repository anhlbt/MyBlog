<!--
<template>
    <div class="container">
        <div class="row" v-for="(posts, index) in processedPosts" :key="index">
            <div class="col-md-4" v-for="(post, index) in posts" v-bind:post="post" v-bind:key="index">    
                <div class="card">
                    <div class="card-title">
                        {{ post.title }}
                    </div>
                    <a :href="post.url" target="_blank"><img :src="post.image_url"></a>
                    <div class="card-text">
                        <p>{{ post.abstract }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 
-->
<template>
    <div>
        <div class="row" v-for="(posts, index) in processedPosts" :key="index">
            <div class="columns large-4 medium-6 small-8" v-for="(post, index) in posts" v-bind:key="index">    
                <div class="card">
                    <div class="card-divider">
                        {{ post.title }}
                    </div>
                    <a :href="post.url" target="_blank"><img :src="post.image_url"></a>
                    <div class="card-section">
                        <p>{{ post.abstract }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'NewsList',
        // props: ['results'],
        props:{
            results:Object
        },
        computed: {
            processedPosts() {
                let posts = this.results;

                // Add image_url attribute
                posts.map(post => {
                    let imgObj = post.multimedia.find(media => media.format === "superJumbo");
                    post.image_url = imgObj ? imgObj.url : "http://placehold.it/300x200?text=N/A";
                });

                // Put Array into Chunks
                let i, j, chunkedArray = [], chunk = 3;
                for (i=0, j=0; i < posts.length; i += chunk, j++) {
                    chunkedArray[j] = posts.slice(i,i+chunk);
                }
                return chunkedArray;
            }
        }
    }
</script>

<style lang="scss">
</style>