import Vue from 'vue/dist/vue.esm.js';
import VueRouter from 'vue-router'

import App from './components/App.vue';
import MasterPage from './components/master.vue';
import VRaspPage from './components/vrasp.vue';


Vue.use(VueRouter);


const routes = [
    { path: '/', component:  MasterPage },
    { path: '/vrasp', component: VRaspPage },
];

const router = new VueRouter({
    routes,
});

new Vue({
    router,
    components: { App },
    el: '#app',
    template: '<App/>',
});
