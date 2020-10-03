import Vue from 'vue/dist/vue.esm.js';
import VueRouter from 'vue-router'

import App from './components/App.vue';
import MasterPage from './components/master.vue';
import VRaspPage from './components/vrasp.vue';

import store from './store';


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
    store,
    template: '<App/>',
});
