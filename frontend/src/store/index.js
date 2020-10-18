import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: window.sessionStorage
    })
  ],
  state: {
    settlementDate: "00-00-0000",
    settlementId: "",
    settlementName: "NA",
    totalCashExpense: 0,
    totalExpense: 0,
    currentUserInfo: {},
    appConfig: {},
    openingCash: 0,
    closingCash: 0
  },
  mutations: {
    setAppConfig(state, appConfig) {
      state.appConfig = appConfig;
    },
    setInitState(state, settlementInfo) {
      state.settlementDate = settlementInfo.date;
      state.settlementId = settlementInfo.id;
      state.settlementName = settlementInfo.name;
      state.totalCashExpense = settlementInfo.cash_expense;
      state.totalExpense = settlementInfo.expense;
      state.openingCash = settlementInfo.opening_cash;
      state.closingCash = settlementInfo.closing_cash;
    },
    setCurrentUserInfo(state, d) {
      state.currentUserInfo = d;
    },
    setTotalExpense(state, exp) {
      state.totalExpense = exp;
    },
    setTotalCashExpense(state, exp) {
      state.totalCashExpense = exp;
    },
    setSettlementDate(state, dt) {
      state.settlementDate = dt;
    },
    // setOpeningCash(state, amt) {
    //   state.openingCash = amt;
    // },
    setClosingCash(state, amt) {
      state.closingCash = amt;
    },
    resetState(state) {
      state.settlementDate = "00-00-0000";
      state.settlementId = "";
      state.settlementName = "NA";
      state.totalCashExpense = 0;
      state.totalExpense = 0;
      state.currentUserInfo = {};
      state.openingCash = 0;
      state.closingCash = 0;
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
    },
    getAppConfig(state) {
      return state.appConfig;
    }
  },
  actions: {},
  modules: {}
});
