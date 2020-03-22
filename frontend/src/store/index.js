import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    settlementDate: "",
    settlementId: "",
    totalCashExpense: 0,
    currentUserInfo: {}
  },
  mutations: {
    setCurentUserInfo(state, d) {
      state.currentUserInfo = d;
    },
    updatetotalCashExpense(state, exp) {
      state.totalCashExpense = exp;
    }
  },
  actions: {},
  modules: {}
});
