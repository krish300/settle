<template>
  <v-container>
    <template>
      <div>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <!-- <th class="text-left">Name</th>
                <th class="text-left">SoftwareSale</th>
                <th class="text-left">Name</th>
                <th class="text-left">ManagerSale</th> -->
              </tr>
            </thead>
            <tbody>
              <!-- for category name  -->
              <tr v-for="ctgry in processedTableLayoutData" :key="ctgry.nm">
                {{
                  ctgry.nm
                }}
                <!--each to hold payment apps and respective info of each category -->
                <v-simple-table dense>
                  <template v-slot:default>
                    <tbody>
                      <!-- each td to hold software sale info each app-->
                      <td>
                        <tr v-for="payApp in ctgry.Sft" :key="'Sft' + payApp.name">
                          <td>{{ payApp.display_name }}</td>
                          <td>
                            <v-text-field single-line :value="payApp.value"></v-text-field>
                          </td>
                        </tr>
                      </td>

                      <!-- each td to hold Manager sale info each app-->
                      <td>
                        <tr v-for="payApp in ctgry.Mgr" :key="'Mgr' + payApp.name">
                          <td>{{ payApp.display_name }}</td>
                          <td>
                            <v-text-field single-line :value="payApp.value"></v-text-field>
                          </td>
                        </tr>
                      </td>
                    </tbody>
                  </template>
                </v-simple-table>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
    </template>
  </v-container>
</template>
<script>
import { mapState, Store } from "vuex";
import axios from "axios";
export default {
  name: "PaymentAppsLayout",
  methods: {
    makeTableLayoutData() {
      let returnObj = {};
      this.layoutInfo.forEach(payMode => {
        var ctgry = payMode.category_nm;
        if (ctgry == null) {
          ctgry = "Genric";
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
