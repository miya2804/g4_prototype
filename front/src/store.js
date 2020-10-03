import Vue from 'vue/dist/vue.esm.js';
import Vuex from 'vuex';

import axios from 'axios';

Vue.use(Vuex);

const state = {
    updateVRaspsInterval: 1000,
    vRasps: [{"id": 1, "opened": true}],
};

const mutations = {
    setUpdateVRaspsInterval(state, updateVRaspsInterval) {
        state.updateVRaspsInterval = updateVRaspsInterval;
    },
    updateVRasps(state, vRasps) {
        state.vRasps = vRasps;
    },
};

const actions = {
    async updateVRasps({ commit }) {
        commit('updateVRasps', await getLatestVRasps());
    },

    updateVRaspsLoop({ dispatch, commit, state }) {
        dispatch('updateVRasps');

        setTimeout(function() {
            dispatch('updateVRaspsLoop')},
                   state.updateVRaspsInterval);
    },

    async generateVRasp() {
        await generateNewVRasp();
    }
};

const getters = {};

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations,
});

const getLatestVRasps = async function() {
    let response = await axios.get('/api/rasp');

    let vRasps = [];
    if (response.status == 200) {
        let vRaspsMap = response.data;
        Object.keys(vRaspsMap).forEach(key => {
            let vRasp = {
                "id": key,
                "opened": vRaspsMap[key].opened,
            };
            vRasps.push(vRasp);
        });
        return vRasps;
    } else {
        return [];
    }
}

const generateNewVRasp = async function() {
    let response = axios.post('/api/rasp');
    if (response.status == 200) {
        console.log('generate success!');
    }
}
