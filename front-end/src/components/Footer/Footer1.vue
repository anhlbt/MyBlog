<template>
    <div id="footer">
        <Newsletter />
        <b-container>
            <b-row>
                <b-col cols="12" md="4">
                    <img width="100" src="@/assets/images/real-estate.png" alt="">
                </b-col>
                <b-col cols="12" md="8">
                    <div id="footer-bottom">
                        <ul>
                            <li><a href="#">Studios</a></li>
                            <li><a href="#">Studios</a></li>
                            <li><a href="#">Studios</a></li>
                            <li><a href="#">Studios</a></li>
                            <li><a href="#">Studios</a></li>
                            <li><a href="#">Studios</a></li>
                        </ul>
                    </div>
                </b-col>
            </b-row>
        </b-container>

        <div id="footer-copy">
            <b-container>
                <p>Real Estate&copy; 2020. All right reserved. </p>
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
@import "./../../assets/scss/_variables";
#footer {
    background: $gradient1;
     #footer-bottom {
        ul {
            display: flex;
            justify-content: center;
            margin-top: 25px;
            li {
                flex: 1;
                list-style: none;
                a {
                    color: #fff;
                    text-transform: uppercase;
                    &:hover {
                        text-decoration: none;
                    }
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