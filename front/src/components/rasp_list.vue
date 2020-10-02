<template>
<ul>
    <rasp-item v-for="rasp in rasps"
        :key="rasp.id"
        v-bind:id="rasp.id"
        v-bind:opened="rasp.opened">
    </rasp-item>
</ul>
</template>

<script>
import axios from 'axios';
import RaspItem from './rasp_item.vue';

export default {
    data() {
        return {
            rasps: [{"id": "10", "opened": true,},],
        };
    },
    components: {
        RaspItem,
    },
    mounted: function() {
        this.updateRasps()
    },

    methods: {
        updateRasps: function () {
            axios
            .get('/api/rasp')
            .then(response => {
                if (response.status == 200) {
                    let rasps = [];
                    let raspsMap = response.data;
                    Object.keys(raspsMap).forEach(key => {
                        let rasp = {
                            "id": key,
                            "opened": raspsMap[key].opened
                        };
                        rasps.push(rasp);
                    });
                    this.rasps = rasps;
                }
            });
            setTimeout(this.updateRasps, 3000);
        },
    },
}
</script>
