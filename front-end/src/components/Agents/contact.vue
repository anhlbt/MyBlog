<template>
    <div>
        <b-form @submit="onSubmit">
            <b-form-group id="input-group-1">
                <b-form-input
                id="input-1"
                required
                placeholder="Complete name"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-2">
                <b-form-input
                id="input-2"
                required
                placeholder="Your phone number"
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-3">
                <b-form-input
                id="input-3"
                type="email"
                required
                placeholder="Your email"
                ></b-form-input>
            </b-form-group>

            <b-form-group label="How agent can contact you?" id="input-group-5">
                <b-form-checkbox-group id="checkboxes-5">
                <b-form-checkbox value="call">Can call me</b-form-checkbox>
                <b-form-checkbox value="that">Can write me an email</b-form-checkbox>
                </b-form-checkbox-group>
            </b-form-group>

            <b-button type="submit" block class="btn-outline-style1">Submit</b-button>
        </b-form>
    </div>
</template>

<script>
    export default {
        methods: {
            onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
        },
    }
}
</script>

<style lang="scss" scoped>

</style>