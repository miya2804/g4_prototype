<template>
<div>
    <input v-model="interval"></input>ms
    <button v-on:click="setInterval">Set!</button>
</div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            interval: 0,
        };
    },

    mounted: function() {
        this.interval = this.$store.state.updateVRaspsInterval;
    },

    methods: {
        setInterval: function() {
            this.$store.commit('setUpdateVRaspsInterval',
                               this.interval);
        },
    },
}
</script>
