<template>
<div>
  <input v-model="password" placeholder="Room ID">
  <button v-on:click="send">
    send
  </button>
  RoomID: {{ this.roomId }}
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            roomId: '',
            password: '',
        }
    },
    
    methods: {
        send: function(event) {
            const requestBody = {
                'password': this.password,
            }

            axios
                .post('/sensor', requestBody)
                .then(response => {
                    if (response.status=200) {
                        this.clearInputs();
                        this.setRoomId(response.data.id);
                    }
                });
        },

        clearInputs: function() {
            this.password = '';
        },

        setRoomId: function(roomId) {
            this.roomId = roomId;
        }
    }
}
</script>
