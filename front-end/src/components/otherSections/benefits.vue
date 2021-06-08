<template>
    <div id="benefits">
        <div class="text-center title">
             <h2>Our Benefits</h2>
            <p>Lorem ipsum dolor sit amet consectetur adipiscing elit. Etiam in dui velit Fusce accumsan.</p>
        </div>
        <b-container>
            <b-row class="my-5">
                <b-col cols="12" md="4">
                    <div id="single-benefit">
                        <i class="fa fa-superpowers"></i>
                        <div class="benefits-text">
                            <b>Lorem ipsum</b>
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit.</p>
                        </div>
                        <span>01</span>
                    </div>
                </b-col>
                <b-col cols="12" md="4">
                    <div id="single-benefit">
                        <i class="fa fa-superpowers"></i>
                        <div class="benefits-text">
                            <b>Lorem ipsum</b>
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit.</p>
                        </div>
                        <span>02</span>
                    </div>
                </b-col>
                <b-col cols="12" md="4">
                    <div id="single-benefit">
                        <i class="fa fa-superpowers"></i>
                        <div class="benefits-text">
                            <b>Lorem ipsum</b>
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit.</p>
                        </div>
                        <span>03</span>
                    </div>
                </b-col>
            </b-row>

            <b-row class="my-5">
                <b-col cols="12" md="4">
                    <div id="single-benefit">
                        <i class="fa fa-superpowers"></i>
                        <div class="benefits-text">
                            <b>Lorem ipsum</b>
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit.</p>
                        </div>
                        <span>04</span>
                    </div>
                </b-col>
                <b-col cols="12" md="4">
                    <div id="single-benefit">
                        <i class="fa fa-superpowers"></i>
                        <div class="benefits-text">
                            <b>Lorem ipsum</b>
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit.</p>
                        </div>
                        <span>05</span>
                    </div>
                </b-col>
                <b-col cols="12" md="4">
                    <div id="single-benefit">
                        <i class="fa fa-superpowers"></i>
                        <div class="benefits-text">
                            <b>Lorem ipsum</b>
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit.</p>
                        </div>
                        <span>06</span>
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
    #benefits {
        background: url('./../../assets/images/benefits-bg2.jpg');
        background-size: cover;
        padding: 150px;

        .title {
            color: #fff;
        }
        #single-benefit {
            padding: 30px 50px 30px 95px;
            border-radius: 10px;
            position: relative;
            background-color: #fff;
            cursor: pointer;
            transition: all .3s ease-in-out;
            -webkit-transition: all .3s ease-in-out;
            -moz-transition: all .3s ease-in-out;

            &:hover {
                box-shadow: 0 8px 22px 0 rgba(0,0,0, .3);
                -webkit-box-shadow: 0 8px 22px 0 rgba(0,0,0, .3);
                -moz-box-shadow: 0 8px 22px 0 rgba(0,0,0, .3);
            }


             &:hover i {
                background: #274160;
                color: #fff;
            }

            &:hover span {
                opacity: 0.2;
                font-size: 110px;
            }

            i {
                position: absolute;
                left: 0px;
                top: 50%;
                font-size: 30px;
                color: #274160;
                width: 70px;
                height: 70px;
                border-radius: 0 100% 100% 0;
                text-align: center;
                padding-top: 18px;
                margin-top: -36px;
                background-color: #ffffff;
                border: 1px solid #eee;
                border-left: none;
                -webkit-transition: all 0.4s ease-in-out;
                -moz-transition: all 0.4s ease-in-out;
                -ms-transition: all 0.4s ease-in-out;
                -o-transition: all 0.4s ease-in-out;
                transition: all 0.4s ease-in-out;
            }

            span {
                position: absolute;
                right: 5px;
                top: 8px;
                font-size: 90px;
                font-weight: 500;
                color: #999;
                opacity: 0.07;
                line-height: 1;
            }
        }
    }

    @media(max-width: 768px) {
        #benefits {
            padding: 30px 0!important;
            #single-benefit {
                margin: 20px 0;
            }
        }
    }
</style>