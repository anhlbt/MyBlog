<template>
    <div id="add-property-cta" class="my-5 py-5">
        <b-container>
            <b-row>
                <b-col cols="12" md="6">
                    <h2>Submit your property for free!</h2>
                </b-col>
                <b-col class="text-center" cols="12" md="6">
                    <router-link class="btn-style3" to="addProperty" tag="b-button">Add Property</router-link>
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
    #add-property-cta {
        -webkit-background: $gradient1;
        background: $gradient1;

        h2 {
            color: #fff;
            font-weight: 100;
        }
    }
</style>