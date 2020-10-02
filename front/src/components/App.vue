<template>
  <div>
    <room-register-form/>
    <sensor-register-form/>
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
