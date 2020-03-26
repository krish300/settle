<template>
  <div class="PaymentAppsLayout">
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <v-row class="salesummary-heading" :elevation="5">
            <v-col :cols="7">
              <v-sheet color="teal ligten-1" class="white--text font-weight-bold" :elevation="5">
                <v-row>
                  <v-col :cols="5"> Software </v-col>
                  <v-col :cols="5">
                    Cashier
                  </v-col>
                  <v-col :cols="2">
                    Differance
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
                      <v-col :cols="6">
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
                                    hide-details
                                    dense
                                    single-line
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
                                    hide-details
                                    dense
                                    single-line
                                    v-model="managerSaleData[payApp.name]"
                                  ></v-text-field>
                                </td>
                              </tr>
                            </td>
                          </v-col>
                        </v-row>
                      </v-col>
                      <!-- this if/else section is to calaculate,render differnce -->
                      <template v-if="ctgryData.nm === 'Generic'">
                        <v-col :cols="1">
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
                                    managerSaleData[payAppData.name]
                                }}
                              </td>
                            </tr>
                          </td>
                        </v-col>
                      </template>
                      <template v-else>
                        <v-col :cols="1">
                          <td>
                            <!-- (Only one row) is the diff of total amount in paymaode category -->
                            <tr class="row-sale-app">
                              <td class="pay-app-diff-td">
                                {{ getCategoryDiff(ctgryData.Sft, ctgryData.Mgr) }}
                              </td>
                            </tr>
                          </td>
                        </v-col>
                      </template>
                    </v-row>
                  </v-container>
                </tbody>
              </template>
            </v-simple-table>
          </tr>
          <v-row class="totals-bar">
            <v-col :cols="7">
              <v-sheet color="teal ligten-1" class="white--text font-weight-bold" :elevation="5">
                <v-row>
                  <v-col :cols="5"> Total: {{ softwareSale }} </v-col>
                  <v-col :cols="5"> Total: {{ managerSale }} </v-col>
                  <v-col :cols="2">
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
</template>
<script>
import { mapState, Store } from "vuex";
import axios from "axios";
export default {
  name: "PaymentAppsLayout",
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
    }
  },
  data() {
    return {
      layoutInfo: [],
      processedTableLayoutData: {},
      softwareSaleData: {},
      managerSaleData: {},
      softwareSale: 0,
      managerSale: 0,
      discount: 0
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
            this.softwareSaleData = JSON.parse(response.data[0].software_data.replace(/'/g, '"'));
            this.managerSaleData = JSON.parse(response.data[0].manager_data.replace(/'/g, '"'));
            this.softwareSale = response.data[0].software_sale;
            this.managerSale = response.data[0].manager_sale;
            this.discount = response.data[0].software_discount;
            this.makeTableLayoutData();
          })
          .catch(error => {
            console.log("error while fetching sale-summary data", error);
          });
      })
      .catch(error => {
        console.log("error while fetching available payment modes", error);
      });
  },
  computed: {
    ...mapState(["currentUserInfo", "settlementId"])
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
  //background-color: none;
}

.PaymentAppsLayout .v-input__slot:before {
  border-style: none !important;
}

.PaymentAppsLayout .pay-app-value-td {
  border-width: thin;
  border-style: solid;
  border-color: black;
  width: 100px;
  // height: 32px;
}

.PaymentAppsLayout .pay-app-name-td {
  border-width: thin;
  border-style: solid;
  border-color: black;
  width: 125px;
  padding-left: 2px;
  background-color: bisque;
  // height: 32px;
}

.PaymentAppsLayout .pay-app-diff-td {
  border-width: thin;
  border-style: solid;
  border-color: black;
  width: 50px;
  // height: 32px;
}

.PaymentAppsLayout .row-sale-app {
  height: 28px;
}

.category-container {
  padding-top: 0px !important;
  padding-left: 0px !important;
  padding-bottom: 2px !important;
  //border-bottom: 0.3px;
  //border-bottom-style: solid;
}

.v-data-table__wrapper {
  overflow-x: hidden !important;
}

.totals-bar {
  text-decoration-color: white;
}
</style>
