import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    settlementDate: "00-00-0000",
    settlementId: "",
    settlementName: "NA",
    totalCashExpense: 0,
    totalExpense: 0,
    currentUserInfo: {}
  },
  mutations: {
    setInitState(state, settlementInfo) {
      state.settlementDate = settlementInfo.date;
      state.settlementId = settlementInfo.id;
      state.settlementName = settlementInfo.name;
      state.totalCashExpense = settlementInfo.cash_expense;
      state.totalExpense = settlementInfo.expense;
    },
    setCurrentUserInfo(state, d) {
      state.currentUserInfo = d;
    },
    setTotalExpense(state, exp) {
      state.totalExpense = exp;
    },
    setTotalCashExpense(state, exp) {
      state.totalCashExpense = exp;
    }
  },
  getters: {
    currentUserName(state) {
      if (state.currentUserInfo.username == undefined) {
        return "NA";
      }
      return state.currentUserInfo.username;
    },
    isAdmin(state) {
      if (state.currentUserInfo.is_staff == true) {
        return true;
      }
      return false;
    }
  },
  actions: {},
  modules: {}
});
