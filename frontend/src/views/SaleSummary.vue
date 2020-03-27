<template>
  <v-app>
    <template>
      <v-container grid-list-md>
        <v-row>
          <v-col :cols="7">
            <div class="PaymentAppsLayout">
              <v-simple-table>
                <template v-slot:default>
                  <tbody>
                    <v-row>
                      <v-col>
                        <v-sheet
                          color="teal ligten-1"
                          class="white--text font-weight-bold"
                          :elevation="5"
                        >
                          <v-row class="salesummary-heading">
                            <v-col :cols="5"> Software </v-col>
                            <v-col :cols="5">
                              Cashier
                            </v-col>
                            <v-col :cols="1">
                              Diff
                            </v-col>
                          </v-row>
                        </v-sheet>
                      </v-col>
                    </v-row>
                    <!--each tr to hold payment apps and respective info of each category -->
                    <tr v-for="ctgryData in processedTableLayoutData" :key="ctgryData.nm">
                      <v-simple-table dense>
                        <template v-slot:default>
                          <!-- <th dense>{{ ctgryData.nm }}</th>
                          <v-container class="salesummary-heading" dense>{{ ctgryData.nm }} </v-container> -->
                          <tbody>
                            <v-container class="category-container">
                              <!-- each row is a container for each ctegory data -->
                              <v-row no-gutters>
                                <v-col :cols="10">
                                  <v-row no-gutters>
                                    <!-- each column td repesents Software sale  -->
                                    <v-col :cols="6">
                                      <td>
                                        <!-- each tr to hold software sale info each app-->
                                        <tr
                                          v-for="payApp in ctgryData.Sft"
                                          :key="'Sft' + payApp.name"
                                          class="row-sale-app"
                                        >
                                          <td class="text-left pay-app-name-td">
                                            {{ payApp.display_name }}
                                          </td>
                                          <td class="pay-app-value-td">
                                            <v-text-field
                                              type="number"
                                              hide-details
                                              dense
                                              single-line
                                              :ref="'Sft-' + payApp.name + '-Value'"
                                              v-model="softwareSaleData[payApp.name]"
                                            ></v-text-field>
                                          </td>
                                        </tr>
                                      </td>
                                    </v-col>
                                    <!-- each column td repesents Manager sale -->
                                    <v-col :cols="6">
                                      <td>
                                        <!-- each tr to hold Manager sale info each app-->
                                        <tr
                                          v-for="payApp in ctgryData.Mgr"
                                          :key="'Mgr' + payApp.name"
                                          class="row-sale-app"
                                        >
                                          <td class="text-left pay-app-name-td">
                                            {{ payApp.display_name }}
                                          </td>
                                          <td class="pay-app-value-td">
                                            <v-text-field
                                              type="number"
                                              hide-details
                                              dense
                                              single-line
                                              :ref="'Mgr-' + payApp.name + '-Value'"
                                              v-model="managerSaleData[payApp.name]"
                                            ></v-text-field>
                                          </td>
                                        </tr>
                                      </td>
                                    </v-col>
                                  </v-row>
                                </v-col>
                                <v-col :cols="1">
                                  <!-- this if/else section is to calaculate,render differnce -->
                                  <template v-if="ctgryData.nm === 'Generic'">
                                    <td>
                                      <!-- each row in this col is the diff of amount in paymaode -->
                                      <tr
                                        v-for="payAppData in ctgryData.Sft"
                                        :key="'Diff' + payAppData.name"
                                        class="row-sale-app"
                                      >
                                        <td class="pay-app-diff-td">
                                          {{
                                            softwareSaleData[payAppData.name] -
                                              managerSaleData[payAppData.name] || 0
                                          }}
                                        </td>
                                      </tr>
                                    </td>
                                  </template>
                                  <template v-else>
                                    <td>
                                      <!-- (Only one row) is the diff of total amount in paymaode category -->
                                      <tr class="row-sale-app">
                                        <td class="pay-app-diff-td">
                                          {{ getCategoryDiff(ctgryData.Sft, ctgryData.Mgr) || 0 }}
                                        </td>
                                      </tr>
                                    </td>
                                  </template>
                                </v-col>
                              </v-row>
                            </v-container>
                          </tbody>
                        </template>
                      </v-simple-table>
                    </tr>
                    <v-row>
                      <v-col>
                        <v-sheet
                          color="teal ligten-1"
                          class="white--text font-weight-bold"
                          :elevation="5"
                        >
                          <v-row class="totals-bar">
                            <v-col :cols="5"> Total: {{ softwareSale }} </v-col>
                            <v-col :cols="5"> Total: {{ managerSale }} </v-col>
                            <v-col :cols="1">
                              {{ softwareSale - managerSale }}
                            </v-col>
                          </v-row>
                        </v-sheet>
                      </v-col>
                    </v-row>
                  </tbody>
                </template>
              </v-simple-table>
            </div>
          </v-col>
          <!-- <v-col :cols="1"></v-col> -->
          <v-col :cols="4">
            <v-container class="fill-height" fluid>
              <v-row>
                <v-simple-table name="cash-details">
                  <template v-slot:default>
                    <thead>
                      <th class="text-right">
                        Cash Details
                      </th>
                      <!-- cash icon which opens cashCalcDialog -->
                      <th class="text-right">
                        <v-dialog v-model="cashCalcDialog" max-width="400px">
                          <template v-slot:activator="{ on }">
                            <v-icon v-on="on">money</v-icon>
                          </template>

                          <CashCalc @cash-update="onCashUpdate" />
                        </v-dialog>
                      </th>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Opening Cash:</td>
                        <td>{{ openingCash }}</td>
                      </tr>
                      <tr>
                        <td>Closing Cash:</td>
                        <td>{{ closingCash }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-row>
              <v-row>
                <v-simple-table name="actions" class="actions-table">
                  <template v-slot:default>
                    <thead>
                      <th class="text-center" width="190">Actions</th>
                    </thead>
                    <tbody>
                      <tr>
                        <v-btn block large>SAVE</v-btn>
                      </tr>
                      <tr>
                        <v-btn block large color="primary" :disabled="closeButtonDisabled"
                          >CLOSE</v-btn
                        >
                      </tr>
                      <tr>
                        <v-btn block large color="error">DELETE</v-btn>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </v-app>
</template>

<script>
import CashCalc from "@/components/CashCalc.vue";

import { mapState, Store } from "vuex";
import axios from "axios";
export default {
  name: "SaleSummary",
  components: {
    CashCalc
  },
  methods: {
    getCategoryDiff(sftPayCtgryData, mgrPayCtgryData) {
      let sftCtgryTotal = 0;
      let mgrCtgryTotal = 0;
      let diff = 0;
      for (let i = 0; i < sftPayCtgryData.length; i++) {
        sftCtgryTotal += this.softwareSaleData[sftPayCtgryData[i].name];
      }
      for (let i = 0; i < mgrPayCtgryData.length; i++) {
        mgrCtgryTotal += this.managerSaleData[mgrPayCtgryData[i].name];
      }
      diff = sftCtgryTotal - mgrCtgryTotal;
      return diff;
    },
    makeTableLayoutData() {
      let returnObj = {};
      this.layoutInfo.forEach(payMode => {
        var ctgry = payMode.category_nm;
        if (ctgry == null) {
          ctgry = "Generic";
        }
        returnObj[ctgry] = returnObj[ctgry] || { nm: ctgry, Mgr: [], Sft: [] };

        if (payMode.display_in === "MANAGER" || payMode.display_in === "BOTH") {
          returnObj[ctgry].Mgr.push({
            name: payMode.name,
            display_name: payMode.display_name,
            value: this.managerSaleData[payMode.name] || 0
          });
        }
        if (payMode.display_in === "SOFTWARE" || payMode.display_in === "BOTH") {
          returnObj[ctgry].Sft.push({
            name: payMode.name,
            display_name: payMode.display_name,
            value: this.softwareSaleData[payMode.name] || 0
          });
        }
      });
      this.processedTableLayoutData = returnObj;
      return returnObj;
    },
    onCashUpdate(d) {
      this.cashCalcDialog = false;
      if (d != null) {
        this.closingCash = d;
      }
    }
  },
  data() {
    return {
      saleSummaryId: null,
      layoutInfo: [],
      processedTableLayoutData: {},
      softwareSaleData: {},
      managerSaleData: {},
      softwareSale: 0,
      managerSale: 0,
      discount: 0,
      closingCash: 0,
      openingCash: 0,
      cashCalcDialog: false,
      closeButtonDisabled: false
    };
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/payment-mode/`)
      .then(response => {
        this.layoutInfo = response.data;
        axios
          .get(
            `${process.env.VUE_APP_SERVER_URL}/api/sale-summary/?settlement=${this.settlementId}`
          )
          .then(response => {
            if (response.data.length > 0) {
              this.softwareSaleData = JSON.parse(response.data[0].software_data.replace(/'/g, '"'));
              this.managerSaleData = JSON.parse(response.data[0].manager_data.replace(/'/g, '"'));
              this.softwareSale = response.data[0].software_sale;
              this.managerSale = response.data[0].manager_sale;
              this.discount = response.data[0].software_discount;
            }
            this.makeTableLayoutData();
          })
          .catch(error => {
            console.log("error while fetching sale-summary data", error);
          });
      })
      .catch(error => {
        console.log("error while fetching available payment modes", error);
      });

    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/settlement/${this.settlementId}/`)
      .then(response => {
        this.openingCash = response.data.opening_cash;
        this.closingCash = response.data.closing_cash;
      })
      .catch(error => {
        console.log("error while fetching settlment data", error);
      });
  },
  mounted() {
    setTimeout(() => {
      // executed after render + 2sec
      this.$refs["Mgr-Cash-Value"][0].readonly = true;
    }, 2000);
  },
  computed: {
    ...mapState(["currentUserInfo", "settlementId", "totalCashExpense"])
  },
  watch: {
    // whenever softwareSaleData changes(deep watch), this handler will run
    softwareSaleData: {
      deep: true,
      handler(softwareSaleData) {
        this.softwareSale = Object.values(softwareSaleData).reduce((a, b) => Number(a) + Number(b));
      }
    },
    managerSaleData: {
      deep: true,
      handler(managerSaleData) {
        this.managerSale = Object.values(managerSaleData).reduce((a, b) => Number(a) + Number(b));
      }
    }
  }
};
</script>

<style lang="scss">
.PaymentAppsLayout .v-text-field input {
  padding-top: 0px;
  padding-bottom: 0px;
}

.PaymentAppsLayout .v-input__slot:before {
  border-style: none !important;
}

.PaymentAppsLayout .pay-app-value-td {
  border-width: thin;
  border-style: solid;
  border-color: black;
  width: 100px;
}

.PaymentAppsLayout .pay-app-name-td {
  border-width: thin;
  border-style: solid;
  border-color: black;
  width: 125px;
  padding-left: 2px;
  background-color: bisque;
}

.PaymentAppsLayout .pay-app-diff-td {
  border-width: thin;
  border-style: solid;
  border-color: black;
  width: 50px;
}

.PaymentAppsLayout .row-sale-app {
  height: 28px;
}

.category-container {
  padding-top: 0px !important;
  padding-left: 0px !important;
  padding-bottom: 2px !important;
}

.v-data-table__wrapper {
  overflow-x: hidden !important;
}
</style>
