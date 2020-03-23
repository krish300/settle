import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    //FIXME(kt): remove hardcode
    settlementDate: "15-03-2020",
    //FIXME(kt): remove hardcode
    settlementId: "340d7515-4e3a-4d5e-a11e-0219bed065d0",
    totalCashExpense: 0,
    currentUserInfo: {}
  },
  mutations: {
    setCurrentUserInfo(state, d) {
      state.currentUserInfo = d;
    },
    updatetotalCashExpense(state, exp) {
      state.totalCashExpense = exp;
    }
  },
  getters: {
    currentUserName(state) {
      if (state.currentUserInfo.username == undefined) {
        return "NA";
      }
      return state.currentUserInfo.username;
    }
  },
  actions: {},
  modules: {}
});
