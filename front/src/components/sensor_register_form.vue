<template>
<div>
  <input v-model="roomId" placeholder="Room ID">
  <input v-model="password" placeholder="Password">
  <input v-model="host" placeholder="Host">
  <button v-on:click="send">
    send
  </button>
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            roomId: '',
            password: '',
            host: '',
        }
    },
    
    methods: {
        send: function(event) {
            const requestBody = {
                'room_id': this.roomId,
                'password': this.password,
                'host': this.host,
            }

            axios
                .post('/room', requestBody)
                .then(response => {
                    if (response.status=200) {
                        this.clearInputs();
                    }
                });
        },

        clearInputs: function() {
            this.roomId = '';
            this.password = '';
            this.host = '';
        },
    }
}
</script>
