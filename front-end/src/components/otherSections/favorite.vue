<template>
    <div>
        <span class="to-favorite" v-b-tooltip.hover title="Add to favorite" @click="addToFav">
            <img width="20" v-if="like" src="@/assets/images/icons/heart-active.png" alt="">
            <img width="20" v-if="!like" src="@/assets/images/icons/heart.png" alt="">
        </span>
    </div>
</template>

<script>
import store2 from '../../store/index.js';

    export default {
        props: {
                title: String,
                image: String,
                id: Number,
        },

        data() {
            return {
                 
                like : false,
                favItems: [],
                item: {
                    propertyId: this.id,
                    propertyTitle: this.title,
                    propertyImage: this.image,
                }
            }
        },
        computed: { count: () => store2.state.count ,

            likeColor: function () {
            if (this.like) {
                console.log("@/assets/images/icons/heart-active.png")
                return "@/assets/images/icons/heart-active.png"
                } 
            else {
                console.log("@/assets/images/icons/heart.png")
                return "@/assets/images/icons/heart.png"
                }
            },
        },

        methods: {
            addToFav() {
                this.like = !this.like
                console.log(this.like)
                console.log(store2.state.favorite)
                // if (this.like && !store2.state.favorite.some(item => item.propertyId === this.item.propertyId))
                if(this.like)
                {
                    store2.commit('addToFav', this.item)
                }
                else
                {
                    store2.commit('removeToFav', this.item)
                }
                
                
                // console.log(store2.state.favorite)
            },
            add: () => store2.commit('add'),
            add2: () => store2.commit('add', 2),
            addThreeAsync: () => store2.dispatch('addThreeAsync'),
            subtract: (payload) => store2.commit('subtract', +payload)            
        }
    }
</script>

	

<style lang="scss" scoped>
    .to-favorite {
        position: absolute;
        top:5px;
        right: 5px;
        cursor: pointer;
    }
</style>