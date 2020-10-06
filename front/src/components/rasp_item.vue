<template>
<li v-if="opened">
  vrasp{{ id }}: OPENED!
  <button v-on:click="closeWindow()">Close!</button>
</li>
<li v-else>
  vrasp{{ id }}: CLOSED!
  <button v-on:click="openWindow()">Open!</button>
</li>
</template>

<script>
import axios from 'axios';

export default {
    props: ['id', 'opened'],
    methods: {
        setWindowState: function(open) {
            const requestBody = {
                'open': open,
            }
            
            axios
            .post('/api/vrasp/'+this.id, requestBody)
            .then(response => {
                console.log('success');
            });
        },
        
        closeWindow: function() {
            this.setWindowState(false);
        },

        openWindow: function() {
            this.setWindowState(true);
        },
    },
}
</script>
