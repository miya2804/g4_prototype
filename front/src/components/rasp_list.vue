<template>
<ul>
    <rasp-item v-for="vrasp in $store.state.vRasps"
        :key="vrasp.id"
        v-bind:id="vrasp.id"
        v-bind:opened="vrasp.opened">
    </rasp-item>
</ul>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex';
import RaspItem from './rasp_item.vue';

export default {
    components: {
        RaspItem,
    },

    mounted: function() {
        this.updateVRaspsLoop();
    },

    methods: mapActions([
        'updateVRasps',
        'updateVRaspsLoop',
    ]),
}
</script>
