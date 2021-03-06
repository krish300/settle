<template>
  <v-app>
    <template>
      <v-container grid-list-md>
        <v-alert type="error" v-model="errAlert" dismissible>
          {{ errorMessage }}
        </v-alert>
        <v-alert type="success" v-model="sucessAlert" dismissible>
          {{ successMessage }}
        </v-alert>
        <v-alert prominent type="error" v-model="deleteAlert">
          <v-row align="center">
            <v-col class="grow"
              >This will delete Settlement, SaleSummary and Expense Entries for the selected day.
              <br />
              <b>Are you sure?</b>
            </v-col>
            <v-col class="shrink">
              <v-btn @click="deleteSettlement">Confirm Delete</v-btn>
            </v-col>
          </v-row>
        </v-alert>
        <v-row>
          <v-col :cols="7" ref="sale-summary">
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
                    <tr
                      v-for="ctgryData in deriveRefernceAttributes(processedTableLayoutData)"
                      :key="ctgryData.nm"
                    >
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
                                            <!-- make manager sale readonly by default -->
                                            <v-text-field
                                              type="number"
                                              min="0"
                                              hide-details
                                              dense
                                              single-line
                                              :readonly="softwareSaleReadonly"
                                              :ref="displayedOrderRefs.Sft[payApp.name].ref"
                                              @keydown.enter="
                                                changeFocusToNextCell(
                                                  displayedOrderRefs.Sft[payApp.name].nextRef
                                                )
                                              "
                                              v-model.number="softwareSaleData[payApp.name]"
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
                                            <!-- readonly for cash value of Cashier -->
                                            <v-text-field
                                              type="number"
                                              min="0"
                                              hide-details
                                              dense
                                              single-line
                                              :readonly="payApp.name === 'Cash'"
                                              :ref="displayedOrderRefs.Mgr[payApp.name].ref"
                                              @keydown.enter="
                                                changeFocusToNextCell(
                                                  displayedOrderRefs.Mgr[payApp.name].nextRef
                                                )
                                              "
                                              v-model.number="managerSaleData[payApp.name]"
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
                                            getPayAppDiff(
                                              softwareSaleData[payAppData.name],
                                              managerSaleData[payAppData.name]
                                            )
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
                                          {{ getCategoryDiff(ctgryData.Sft, ctgryData.Mgr) }}
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
                            <v-col :cols="1"> {{ saleDiff }} </v-col>
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
          <!-- right column for opening, closing cash, buttons -->
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
                        <td>Todays Cash Expenses:</td>
                        <td>{{ totalCashExpense }}</td>
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
                        <v-btn block large @click="saveSettlementAndSale">SAVE</v-btn>
                      </tr>
                      <tr>
                        <v-btn
                          block
                          large
                          color="primary"
                          :disabled="closeButtonDisabled"
                          @click="closeSettlement"
                          >CLOSE</v-btn
                        >
                      </tr>
                      <tr>
                        <v-btn block large color="error" @click="deleteAlert = true">DELETE</v-btn>
                      </tr>
                      <tr v-show="getAppConfig['download-buttons-enabled'] == 'true'">
                        <v-icon large color="green darken-2" @click="downloadSaleSummaryImage">
                          mdi-arrow-down-box
                        </v-icon>
                        <v-icon large color="green darken-2" @click="getPosIstSaleSummary">
                          mdi-table-sync
                        </v-icon>
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
import router from "../router";
import { mapState, mapGetters } from "vuex";
import axios from "axios";
import * as htmlToImage from "html-to-image";
import * as download from "downloadjs";
export default {
  name: "SaleSummary",
  components: {
    CashCalc
  },
  methods: {
    validateData() {},
    saveSettlementAndSale(action = "") {
      // settlement
      let settlementPostData = {
        opening_cash: this.openingCash,
        closing_cash: this.closingCash,
        cash_expense: this.totalCashExpense,
        expense: this.totalExpense,
        last_modified_by: this.currentUserName,
        date: this.settlementDate,
        name: this.settlementName,
        id: this.settlementId
      };
      var settlementChangesSaved = false;
      let successMsg = "Saved Successfully!";
      if (action == "close") {
        settlementPostData.is_closed = true;
        settlementPostData.closed_by = this.currentUserName;
        successMsg = "Closed Successfully!";
      }

      // sale summary
      let salePostData = {
        date: this.settlementDate,
        software_data: this.softwareSaleData,
        manager_data: this.managerSaleData,
        // software_data: JSON.stringify(this.softwareSaleData),
        // manager_data: JSON.stringify(this.managerSaleData),
        software_sale: this.softwareSale,
        manager_sale: this.managerSale,
        software_discount: this.discount,
        last_modified_by: this.currentUserName,
        settlement: this.settlementId
      };
      let saleSummaryMethod = "POST";
      let urlAppend = "";
      if (this.saleSummaryId !== null) {
        urlAppend = this.saleSummaryId + "/";
        saleSummaryMethod = "PUT";
      }
      // save settlement data
      axios({
        method: "PUT",
        url: `${process.env.VUE_APP_SERVER_URL}/api/settlement/${this.settlementId}/`,
        data: settlementPostData,
        xsrfHeaderName: "X-CSRFToken"
      })
        .then(response => {
          // save sale summary data
          axios({
            method: saleSummaryMethod,
            url: `${process.env.VUE_APP_SERVER_URL}/api/sale-summary/${urlAppend}`,
            data: salePostData,
            xsrfHeaderName: "X-CSRFToken"
          })
            .then(response => {
              this.successMessage = successMsg;
              this.sucessAlert = true;
              if (this.saleSummaryId === null) {
                this.saleSummaryId = response.data.id;
              }
              if (action == "close") {
                this.settlementClosed = true;
              }
            })
            .catch(error => {
              this.errorMessage = "error while saving, call admin.";
              this.errAlert = true;
              console.log("error while saving sale summary data", error);
            });
        })
        .catch(error => {
          this.errorMessage = "error while saving, call admin.";
          this.errAlert = true;
          console.log("error while saving settlement data", error);
        });
    },
    closeSettlement() {
      this.saveSettlementAndSale("close");
    },
    deleteSettlement() {
      this.deleteAlert = false;
      axios({
        method: "DELETE",
        url: `${process.env.VUE_APP_SERVER_URL}/api/settlement/${this.settlementId}/`,
        xsrfHeaderName: "X-CSRFToken"
      })
        .then(response => {
          this.successMessage = "Settlement Deleted!";
          this.sucessAlert = true;
          axios
            .get(`${process.env.VUE_APP_SERVER_URL}/api/settlement/latest/`)
            .then(response => {
              this.$store.commit("setInitState", response.data);
              router.push({ path: "/" });
            })
            .catch(error => {
              console.log("error while fetching new settlement info", error);
            });
        })
        .catch(error => {
          this.errorMessage = "error while deleting the Settlement please call admin.";
          this.errAlert = true;
          console.log("error while deleting the Settlement", error);
        });
    },
    getPayAppDiff(sftPayAppVal, mgrPayAppVal) {
      return Number(sftPayAppVal || 0) - Number(mgrPayAppVal || 0);
    },
    getCategoryDiff(sftPayCtgryData, mgrPayCtgryData) {
      let sftCtgryTotal = 0;
      let mgrCtgryTotal = 0;
      let diff = 0;
      for (let i = 0; i < sftPayCtgryData.length; i++) {
        sftCtgryTotal += Number(this.softwareSaleData[sftPayCtgryData[i].name] || 0);
      }
      for (let i = 0; i < mgrPayCtgryData.length; i++) {
        mgrCtgryTotal += Number(this.managerSaleData[mgrPayCtgryData[i].name] || 0);
      }
      diff = Number(sftCtgryTotal) - Number(mgrCtgryTotal);
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
            display_name: payMode.display_name
          });
          //this.managerSaleData[payMode.name] = this.managerSaleData[payMode.name] || 0;
        }
        if (payMode.display_in === "SOFTWARE" || payMode.display_in === "BOTH") {
          returnObj[ctgry].Sft.push({
            name: payMode.name,
            display_name: payMode.display_name
          });
          //this.softwareSaleData[payMode.name] = this.softwareSaleData[payMode.name] || 0;
        }
      });
      this.processedTableLayoutData = returnObj;

      return returnObj;
    },
    onCashUpdate(d) {
      this.cashCalcDialog = false;
      if (d != null) {
        this.$store.commit("setClosingCash", d);
      }
    },
    appendToDisplayedOrderRefs(colType, appName, cellRefName, nextRefName) {
      this.displayedOrderRefs[colType][appName] = {
        ref: cellRefName,
        nextRef: nextRefName
      };
    },
    changeFocusToNextCell(nextCellRef) {
      this.$refs[nextCellRef][0].focus();
    },
    // fetching refernces of text feilds and getting the order in which they are rendered on UI
    // only need of this code is to add excel like functionality, next cell on ENTER key press
    // messy
    deriveRefernceAttributes(fullTableData) {
      let sftData = [];
      let mgrData = [];
      for (let eachCategoryData of Object.values(fullTableData)) {
        sftData = sftData.concat(eachCategoryData.Sft);
        mgrData = mgrData.concat(eachCategoryData.Mgr);
      }
      for (let [index, appInfo] of sftData.entries()) {
        let refName = "Sft-" + appInfo.name + "-ref";
        let nextRefName = "Sft-" + (sftData[index + 1] || sftData[0]).name + "-ref";
        this.appendToDisplayedOrderRefs("Sft", appInfo.name, refName, nextRefName);
      }
      for (let [index, appInfo] of mgrData.entries()) {
        let refName = "Mgr-" + appInfo.name + "-ref";
        let nextRefName = "Mgr-" + (mgrData[index + 1] || mgrData[0]).name + "-ref";
        this.appendToDisplayedOrderRefs("Mgr", appInfo.name, refName, nextRefName);
      }
      return fullTableData;
    },
    getPosIstSaleSummary() {
      axios
        .get(
          `${process.env.VUE_APP_SERVER_URL}/api/posist/get_posist_sale/?settlemment_date=${this.settlementDate}`
        )
        .then(response => {
          for (const [appNm, sale] of Object.entries(response.data)) {
            this.$set(this.softwareSaleData, appNm, sale);
          }
        })
        .catch(error => {
          console.log("error", error.response.data);
          console.error("oops, something went wrong!", error);
        });
    },
    downloadSaleSummaryImage() {
      console.log(this.getAppConfig);
      let ele = this.$refs["sale-summary"];
      let dt = this.settlementDate;
      htmlToImage
        .toPng(ele)
        .then(function(dataUrl) {
          download(dataUrl, `${dt}-SaleSummary.png`);
        })
        .catch(function(error) {
          console.error("oops, something went wrong!", error);
        });
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
      cashCalcDialog: false,
      errorMessage: "",
      errAlert: false,
      successMessage: "",
      sucessAlert: false,
      deleteAlert: false,
      settlementClosed: false,
      displayedOrderRefs: { Sft: {}, Mgr: {} },
      softwareSaleReadonly: true
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
              this.softwareSaleData = response.data[0].software_data;
              this.managerSaleData = response.data[0].manager_data;
              // this.softwareSaleData = JSON.parse(response.data[0].software_data.replace(/'/g, '"'));
              // this.managerSaleData = JSON.parse(response.data[0].manager_data.replace(/'/g, '"'));
              this.softwareSale = response.data[0].software_sale;
              this.managerSale = response.data[0].manager_sale;
              this.discount = response.data[0].software_discount;
              this.saleSummaryId = response.data[0].id;
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
  },
  computed: {
    ...mapState([
      "currentUserInfo",
      "settlementId",
      "totalCashExpense",
      "totalExpense",
      "settlementDate",
      "settlementName",
      "closingCash",
      "openingCash"
    ]),
    ...mapGetters(["currentUserName", "getAppConfig"]),
    saleDiff() {
      return this.managerSale - this.softwareSale;
    },
    closeButtonDisabled() {
      let acceptableSaleDiff = Number(this.getAppConfig["settlement-difference-allowed"]);
      if (
        (this.saleDiff == 0 || this.saleDiff >= -acceptableSaleDiff) &&
        this.softwareSale != 0 &&
        this.managerSale != 0
      ) {
        return false;
      }
      return true;
    },
    computedCashSale() {
      return this.closingCash + this.totalCashExpense - this.openingCash;
    }
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
    },
    settlementClosed: {
      immediate: true,
      handler() {
        if (this.settlementClosed) {
          axios
            .get(`${process.env.VUE_APP_SERVER_URL}/api/settlement/latest/`)
            .then(response => {
              this.$store.commit("setInitState", response.data);
              this.settlementClosed = false;
            })
            .catch(error => {
              console.log("error while fetching new settlement info", error);
            });
        }
      }
    },
    computedCashSale: {
      immediate: true,
      handler(computedCashSale) {
        this.managerSaleData.Cash = computedCashSale;
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
