<template>
    <section class="callout secondary">
        <h5 class="text-center">Filter by Category</h5>
        <form>
            <div class="row">
                <div class="large-6 columns">
                    <select v-model="section">
                        <option v-for="section in sections" :value="section">{{ section }}</option>
                    </select>
                </div>
                <div class="medium-6 columns">
                    <a @click="getPosts(section)" class="button expanded">Retrieve</a>
                </div>
            </div>
        </form>
    </section>
</template>
<script>
    const SECTIONS = "home, arts, automobiles, books, business, fashion, food, health, insider, magazine, movies, national, nyregion, obituaries, opinion, politics, realestate, science, sports, sundayreview, technology, theater, tmagazine, travel, upshot, world"; // From NYTimes

    export default {
        name: 'FilterForm',
        // props: ['getPosts'],
        props:{
            getPosts:Function,
        },
        data () {
            return {
                sections: SECTIONS.split(', '), // create an array of the sections
                section: 'home' // set default section to 'home'
            }
        }
    }
</script>
<style>
</style>