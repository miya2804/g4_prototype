<template>
<div>
  <vrasp-generate-button/>
  <vrasp-set-interval-button/>
  <rasp-list/>
  <p><router-link to="/">Top</router-link></p>
</div>
</template>

<script>
import RaspList from './rasp_list.vue';
import VRaspGenerateButton from './vrasp_generate_button.vue';
import VRaspSetUpdateIntervalButton from './set_vrasp_update_interval_button.vue';

export default {
    components: {
        RaspList,
        'vrasp-generate-button': VRaspGenerateButton,
        'vrasp-set-interval-button': VRaspSetUpdateIntervalButton,
    },
}
</script>
