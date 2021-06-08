<template>
    <div>
        <b-row id="create-account">
            <b-col class="bg">

            </b-col>
            <b-col class="account-form">
                <h2 class="text-center">Create new account</h2>
                <b-form @submit="onSubmit">
                    <b-form-input
                        id="account-name"
                        size="md"
                        placeholder="Name"
                    ></b-form-input>

                    <b-form-input
                        id="account-phone"
                        size="md"
                        placeholder="Phone"
                    ></b-form-input>

                    <b-form-input
                        id="account-email"
                        size="md"
                        placeholder="email@example.com"
                    ></b-form-input>

                    <b-form-input
                        id="account-password"
                        type="password"
                        size="md"
                        placeholder="Password"
                    ></b-form-input>

                    <b-form-checkbox class="mb-3">Remember me</b-form-checkbox>
                    <b-button variant="primary" class="btn-style2" @click="onClick">Sign In</b-button>
                </b-form>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    export default {
        
    }
</script>

<style lang="scss" scoped>
    #create-account {
        .bg{
            background-image: url('~assets/images/account.jpg');
        }

        .account-form {
            padding: 60px 30px;
             input {
            margin: 30px 0;
            }
        }
    }
</style>