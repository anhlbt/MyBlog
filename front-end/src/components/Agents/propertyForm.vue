<template>
    <div class="agent-form" id="request-tour">
        <b-row class="property-agent">
            <b-col cols="12" md="4">
                <div class="profile-card-img"><img :src="infoAuthor.avatar" alt=""></div>
            </b-col>
            <b-col cols="12" md="8">
                <div class="agent-name">{{infoAuthor.name || infoAuthor.username}}</div>    
                    <div class="agent-social">
                    <a href="#" class="agent-social-icon facebook"><div class="fa fa-facebook"></div></a>
                    <a href="#" class="agent-social-icon instagram"><div class="fa fa-instagram"></div></a>
                    <a href="#" class="agent-social-icon twitter"><div class="fa fa-twitter"></div></a>
                    <a href="#" class="agent-social-icon linkedin"><div class="fa fa-linkedin"></div></a>
                </div>
            </b-col>
        </b-row>
        <b-row class="contact-agent-form">
            <h5>Request an tour of property</h5>
            <b-form @submit="onSubmit">
                <b-form-group id="input-group-1">
                    <b-form-input id="input-1" required placeholder="Complete name"
                    ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2">
                    <b-form-input id="input-2" required placeholder="Your phone number"
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    id="input-group-3">
                    <b-form-input id="input-3" type="email" required placeholder="Your email"
                    ></b-form-input>
                </b-form-group>
                
                <label>Choose tour date and time</label>
                <date-pick
                    v-model="date"
                    :pickTime="true"
                    :format="'YYYY-MM-DD HH:mm'"
                    ></date-pick>

                <b-form-group label="How agent can contact you?" id="input-group-5">
                    <b-form-checkbox-group id="checkboxes-5">
                    <b-form-checkbox value="call">Can call me</b-form-checkbox>
                    <b-form-checkbox value="that">Can write me an email</b-form-checkbox>
                    </b-form-checkbox-group>
                </b-form-group>

                <b-button type="submit" block class="btn-outline-style1">Submit</b-button>
            </b-form>
        </b-row>        
    </div>
</template>

<script>
import DatePick from 'vue-date-pick';
    export default {
        components: {
                DatePick,
            },
        props: {
            infoAuthor:{
                type: Object,
                value: null
            }
        },
        data() {
            return {
                date: '2019-01-01 14:30',
            }
        },

        methods: {
                onSubmit(evt) {
            evt.preventDefault()
            alert(JSON.stringify(this.form))
            },
        }
    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
    .agent-form {
        background: $color1-light;
        padding: 20px;
        margin: 0 30px;
        z-index: 2!important;
        box-shadow: -1px 2px 10px 0 rgba(0, 0, 0, 0.2);
        -webkit-box-shadow: -1px 2px 10px 0 rgba(0, 0, 0, 0.2);
        -moz-box-shadow: -1px 2px 10px 0 rgba(0, 0, 0, 0.2);
        position: sticky;
        top: 0;

        .property-agent {
            border-bottom: 1px dotted #fff;
            padding: 20px;
            .profile-card-img {
                margin-right: 1px dotted #fff;
                img {
                    border-radius: 50%;
                    width: 100px;
                }
            }

            .agent-name {
                font-size: 25px;
                font-weight: bold;
            }

            .agent-social {
                    display: flex;
                    justify-content: center;
                    align-content: center;

            .agent-social-icon {
                display: inline-flex;
                width: 40px;
                height: 40px;
                margin: 5px;
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
                    transform: rotateY(180deg);
                    -moz-transform: rotateY(180deg);
                    -webkit-transform: rotateY(180deg);
                }
            }

            .facebook {
                background: linear-gradient(45deg, #3b5998, #0078d7);
            }

            .twitter {
                background: linear-gradient(45deg, #1da1f2, #0e71c8);

            }

            .instagram {
                background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
            }

            .linkedin {
                background: linear-gradient(45deg, #324e63, #414447);
            }
        }
    }

    .contact-agent-form {
        padding: 20px;

        form{
            width: 100%;
        }
    }
}
</style>