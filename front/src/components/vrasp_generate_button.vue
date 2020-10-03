<template>
<button v-on:click="generateVRasp()">Generate!</button>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    methods: mapActions([
        'generateVRasp',
    ]),
}
</script>
