<template>
    <div v-swiper:mySwiper="swiperOption">
        <h4 class="mt-5 text-center">Partners</h4>
        <div class="swiper-wrapper my-5">
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
            <div class="swiper-slide">
                <img width="100" src="@/assets/images/agencies.jpg" alt="">
            </div>
        </div>
  </div>

</template>

<script>
    export default {
        data() {
            return {
                swiperOption: {
                    loop: true,
                    slidesPerView: '6',
                    centeredSlides: false,
                    spaceBetween: 25,
                    autoplay: true,
        
                    autoplay: {
                        delay: 3000,
                    },

                        controller: {
                        inverse: true,
                    },

                    breakpoints: {
                        768: {
                            slidesPerView: 4,
                            loopedSlides: 2,
                            spaceBetween: 10
                        },
                        675: {
                            slidesPerView: 3,
                            loopedSlides: 1,
                            spaceBetween: 5
                        }
                    }
                },
         
            }
        }
    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/main";
</style>