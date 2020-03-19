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
  methods: {},
  data() {
    return {
      layoutInfo: []
    };
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/payment-mode/`)
      .then(response => {
        this.layoutInfo = response.data;
      })
      .catch(error => {
        console.log("error while fetching available payment modes", error);
      });
  },
  computed: {
    ...mapState(["currentUserInfo"]),
    processedTableLayoutData() {
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
            value: 0
          });
        }
        if (payMode.display_in === "SOFTWARE" || payMode.display_in === "BOTH") {
          returnObj[ctgry].Sft.push({
            name: payMode.name,
            display_name: payMode.display_name,
            value: 0
          });
        }
      });
      console.log(returnObj);
      return returnObj;
    }
  }
};
</script>
