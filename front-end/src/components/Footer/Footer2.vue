<template>
    <div id="footer">
        <b-container>
            <b-row>
                <b-col cols="12" md="4">
                    <img width="100" src="@/assets/images/real-estate.png" alt="">

                    <div class="social-accounts">
                        <a href="#" class="social-icon facebook"><div class="fa fa-facebook"></div></a>
                        <a href="#" class="social-icon instagram"><div class="fa fa-instagram"></div></a>
                        <a href="#" class="social-icon twitter"><div class="fa fa-twitter"></div></a>
                        <a href="#" class="social-icon linkedin"><div class="fa fa-linkedin"></div></a>
                    </div>
                </b-col>
                <b-col cols="12" md="4" class="footer-col2">
                   <ul>
                       <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                        <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                        <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                        <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                   </ul>
                </b-col>
                 <b-col cols="12" md="4" class="footer-col3">
                   <ul>
                       <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                        <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                        <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                        <li>
                           <a href="#">Bất động sản Phan Thiết</a>
                       </li>
                   </ul>
                </b-col>
            </b-row>
        </b-container>

        <div id="footer-copy">
            <b-container>
                <p>Real Estate&copy; 2020. All right reserved. Build by Anhlbt</p>
            </b-container>
        </div>
    </div>
</template>

<script>
import Newsletter from '@/components/Footer/Newsletter.vue';
    export default {
        components: {
            Newsletter,
        }
    }
</script>

<style lang="scss" scoped>
#footer {
    background: #010012e8;
    text-align: center;
    padding-top: 45px;

         .social-accounts {
            display: flex;
            align-content: center;
            justify-content: center;
            padding: 25px 0;

            .social-icon {
                display: inline-flex;
                width: 35px;
                height: 35px;
                margin: 15px;
                border-radius: 50%;
                align-items: center;
                justify-content: center;
                color: #fff;
                background: #405de6;
                position: relative;
                font-size: 18px;
                flex-shrink: 0;
                transition: all .6s;

                &:hover {
                    text-decoration: none;
                    transform: scale(1.1);
                    -moz-transform: scale(1.1);
                    -webkit-transform: scale(1.1);;
                }
            }

            .facebook {
                background: linear-gradient(45deg, #3b5998, #0078d7);
                box-shadow: 0px 4px 30px rgba(43, 98, 169, 0.5);
            }

            .twitter {
                background: linear-gradient(45deg, #1da1f2, #0e71c8);
                box-shadow: 0px 4px 30px rgba(19, 127, 212, 0.7);
            }

            .instagram {
                background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
                box-shadow: 0px 4px 30px rgba(120, 64, 190, 0.6);
            }

            .linkedin {
                background: linear-gradient(45deg, #324e63, #414447);
                box-shadow: 0px 4px 30px rgba(55, 75, 90, 0.6);
            }
        } 
        
        .footer-col2, .footer-col3 {
            ul li {
                list-style: none;
                padding: 10px 0;

                &:hover {
                    background: #010012bd;
                }

                a {
                    color: #fff;

                    &:hover {
                        text-decoration: none;
                    }
                }
            }
        }

    #footer-copy {
        background: #000;
        padding: 15px 0 5px 0;

        p, a {
            color: #fff;
        }
    }
}
</style>