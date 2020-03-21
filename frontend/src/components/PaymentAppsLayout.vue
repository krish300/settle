<template>
  <div class="PaymentAppsLayout">
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <v-row>
            <v-col>
              <v-card color="primary"> </v-card>
            </v-col>
          </v-row>
          <!--each tr to hold payment apps and respective info of each category -->
          <tr v-for="ctgryData in processedTableLayoutData" :key="ctgryData.nm">
            <v-simple-table dense>
              <template v-slot:default>
                <!-- <th dense>{{ ctgryData.nm }}</th> -->
                <tbody>
                  <v-container>
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
      //FIXME(kt): remove hardcode
      settlemenId: "340d7515-4e3a-4d5e-a11e-0219bed065d0",
      softwareSaleData: {},
      managerSaleData: {}
    };
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/payment-mode/`)
      .then(response => {
        this.layoutInfo = response.data;
        axios
          .get(`${process.env.VUE_APP_SERVER_URL}/api/sale-summary/?settlement=${this.settlemenId}`)
          .then(response => {
            this.softwareSaleData = JSON.parse(response.data[0].software_data.replace(/'/g, '"'));
            this.managerSaleData = JSON.parse(response.data[0].manager_data.replace(/'/g, '"'));
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
    ...mapState(["currentUserInfo"])
  }
};
</script>

<style lang="scss">
.PaymentAppsLayout .v-text-field input {
  padding-top: 0px;
  padding-bottom: 0px;
  //background-color: none;
}

.PaymentAppsLayout .v-text-field {
  border-style: none !important;
}
.PaymentAppsLayout .v-input__slot {
  border-style: none !important;
}

.PaymentAppsLayout .v-input__control {
  border-style: none !important;
}

.PaymentAppsLayout .v-text-field__slot {
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
</style>
