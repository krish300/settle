import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    settlementDate: "",
    currentUserInfo: {}
  },
  mutations: {
    setCurentUserInfo(state, d) {
      state.currentUserInfo = d;
    }
  },
  actions: {},
  modules: {}
});
