<template>
<div>
  <vrasp-generate-button/>
  <rasp-list/>
  <p><router-link to="/">Top</router-link></p>
</div>
</template>

<script>
import RaspList from './rasp_list.vue';
import VRaspGenerateButton from './vrasp_generate_button.vue';

export default {
    components: {
        RaspList,
        'vrasp-generate-button': VRaspGenerateButton,
    },
}
</script>
