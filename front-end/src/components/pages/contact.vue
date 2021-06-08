<template>
    <div>
        <b-container id="contact-page">
            <b-row class="align-items-center">
                <b-col cols="12" md="8" class="contact-form my-5">
                    <h3>Contact us fast and simple.</h3>
                    <b-form @submit="onSubmit">

                        <b-form-input
                        id="input-1"
                        type="text"
                        required
                        placeholder="Name"
                        v-model="name"
                        :state="name.length >= 2"
                        ></b-form-input>

                        <b-form-input
                        id="input-2"
                        type="number"
                        required
                        placeholder="Phone"
                        v-model="phone"
                        :state="phone.length >= 8"
                        ></b-form-input>

                        <b-form-input
                        id="input-3"
                        type="email"
                        required
                        placeholder="Email"
                        v-model="email"
                        :state="email.length >= 5"
                        ></b-form-input>

                        <b-form-textarea
                            id="input-4"
                            v-model="message"
                            :state="message.length >= 20"
                            placeholder="Your details..."
                            rows="4"
                        ></b-form-textarea>
                        
                        <b-button type="submit" class="btn-style2">Send Message</b-button>

                    </b-form>
                </b-col>
                <b-col cols="12" md="4">
                    <div class="minicard">
                        <i class="fa fa-phone"></i>
                        <a href="tel:071212121"><b>0712 121 212</b></a>
                    </div>
                     <div class="minicard">
                        <i class="fa fa-envelope"></i>
                        <a href="mailto:office@realestate.com"><b>office@realestate.com</b></a>
                    </div>
                     <div class="minicard">
                        <i class="fa fa-window-close"></i>
                        <a><b>09:00 - 17:00 <sup>Mon - Fri</sup></b></a>
                    </div>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                name: '',
                phone: '',
                email: '',
                message: ''
            }
        },

        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                alert(JSON.stringify(this.form))
            }
        }
    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
@import "./../../assets/scss/main";
    #contact-page {
        .contact-form {
            input, textarea {
                margin: 30px 0;
            }

            .btn-style2 {
                margin: 20px 0;
                display: block;
                width: 100%;
                box-shadow: 0 5px 22px 0 rgba(0,0,0, .3);
            }
        }

        .minicard {
            background: $color1-light;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 35px 10px;
            padding: 15px;
            border-radius: 20px;
            box-shadow: 0 3px 6px rgba(0,0,0, .3);

            i {
                padding: 10px 15px;
                background: rgba(255,255,255, .3);
                border-radius: 50%;
                font-size: 30px;
            }

            a {
                font-size: 22px;
                color: #000;
                &:hover {
                    text-decoration: none;
                }
            }
        }
    }
</style>