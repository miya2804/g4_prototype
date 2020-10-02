<template>
<button v-on:click="generateRasp()">Generate!</button>
</template>

<script>
import axios from 'axios';

export default {
    methods: {
        generateRasp: function() {
            axios
            .post('/api/rasp')
            .then(response => {
                console.log('generate success');
            });
        }
    },
}
</script>
