<template>
<div>
  <room-register-form/>
  <sensor-register-form/>
  <p><router-link to="/vrasp">Virtual Rasps</router-link></p>
</div>
</template>

<script>
import RoomRegisterForm from './room_register_form.vue'
import SensorRegisterForm from './sensor_register_form.vue'

export default {
    components: {
        RoomRegisterForm,
        SensorRegisterForm,
    },
}
</script>
