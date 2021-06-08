<template>
    <div>
        <div id="header1-topbar">
                <b-container>
                    <b-row>
                        <b-col cols="12" md="6" class="topbar-left">
                            <!--Currency select-->
                            <b-dropdown variant="outline-light" class="dropdown-btn mr-2" size="sm" text="Currency">
                                <b-dropdown-item-button><i class="fa fa-euro-sign"></i> Euro</b-dropdown-item-button>
                                <b-dropdown-item-button>Dollar</b-dropdown-item-button>
                            </b-dropdown>
                            <!--End currency select-->

                            <!--Language select-->
                            <b-dropdown variant="outline-light" class="dropdown-btn" size="sm" text="Language">
                                <b-dropdown-item-button>English</b-dropdown-item-button>
                                <b-dropdown-item-button>French</b-dropdown-item-button>
                                <b-dropdown-item-button>Spanish</b-dropdown-item-button>
                            </b-dropdown>
                            <!--End language select-->

                             <!--Not logged user-->
                            <b-button class="mx-4 pt-2" variant="outline-light" v-b-modal.modal-login-popup>Login</b-button>
                                <b-modal id="modal-login-popup" centered hide-footer title="Welcome back!">
                                    <b-form>
                                        <b-form-group label="Email" label-for="dropdown-form-email" >
                                        <b-form-input
                                            id="dropdown-form-email"
                                            size="md"
                                            placeholder="email@example.com"
                                        ></b-form-input>
                                        </b-form-group>

                                        <b-form-group label="Password" label-for="dropdown-form-password">
                                        <b-form-input
                                            id="dropdown-form-password"
                                            type="password"
                                            size="md"
                                            placeholder="Password"
                                        ></b-form-input>
                                        </b-form-group>

                                        <b-form-checkbox class="mb-3">Remember me</b-form-checkbox>
                                        <b-button variant="primary" class="btn-style2" @click="onClick">Sign In</b-button>
                                    </b-form>
                               
                                <a href="#" class="my-1">Forgot Password?</a>
                                <b-button class="btn-style1 my-3" block>Create new account</b-button>
                            </b-modal>
                            <!--End not logged user-->

                        </b-col>

                        <b-col cols="12" md="6">
                            <div class="social-accounts">
                                <a href="#" class="social-icon facebook"><div class="fa fa-facebook"></div></a>
                                <a href="#" class="social-icon instagram"><div class="fa fa-instagram"></div></a>
                                <a href="#" class="social-icon twitter"><div class="fa fa-twitter"></div></a>
                                <a href="#" class="social-icon linkedin"><div class="fa fa-linkedin"></div></a>
                            </div>
                        </b-col>
                    </b-row>
                </b-container>
            </div>
        </div>
</template>

<script>
    export default {
        methods: {
      onClick() {
        this.$refs.dropdown.hide(true)
      }
    }
    }
</script>

<style lang="scss" scoped>
    #header1-topbar {
        background: #000;
        align-content: center;
        .topbar-left {
            display: flex;
            align-items: center;
        }
    b-dropdown-form {
        min-width: 400px!important;
        padding: 10px!important;
    }
        #dropdown-form {
            .dropdown.show {
                top: 50px!important;
                left: -100px!important;
            }
        }
        .btn-secondary {
            background-color: transparent!important;
        }

        .social-accounts {
            display: flex;
            justify-content: flex-end;
            align-content: center;

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

    }
</style>