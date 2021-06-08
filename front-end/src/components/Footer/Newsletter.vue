<template>
    <div id ="newsletter">
        <b-container>
            <b-row>
                <b-col class="text-center">
                     <div class="newsletter-img">
                        <img width="60" src="@/assets/images/letter.png" alt="">
                    </div>
                <h3>Sign up and get fresh properties!</h3>
                <div class="newsletter-form">
                    <input type="email" placeholder="Enter your email">
                    <button><i class="fa fa-arrow-right"></i></button>
                </div>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    export default {
        
    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
    #newsletter {
        padding: 35px 0;
        border-bottom: 2px dotted #fff;
        .newsletter-img {
            background: $color1-light;
            border-radius: 50%;
            padding: 25px;
            margin: auto;
            width: 130px;
            border-bottom: 2px dotted #fff;
            border-bottom: 2px dotted #fff;
        }

         h3 {
                color:#fff;
                margin-top: 20px;
            }

        .newsletter-form {
            margin: auto;
            width: 30%;
            height: 50px;
            border-radius: 40px;
            position: relative;
            margin-top: 40px;
            background-color: #f1f1f199;

            input {
                height: 50px;
                border-radius: 40px;
                border: 0;
                background: none;
                padding: 0 30px;
                outline: none;
                font-size: 15px;
            }

            button {
                background-color: $color1!important;
                border: 0;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                position: absolute;
                outline: none;
                cursor: pointer;
                color: #fff;
                transition: .3s linear;
                transition: all .3s ease-in-out;
                -moz-transition: all .3s ease-in-out;
                -webkit-transition: all .3s ease-in-out;

                &:hover i {
                    font-size: 25px;
                }
            }
        }
    }
</style>