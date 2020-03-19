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
        <!-- <v-container grid-list-md text-xs-center>
          <v-layout row wrap>
            <v-row v-for="item in processedTableLayoutData" :key="item.nm">
              <v-flex xs12>
                {{ item.nm }}
                <v-flex xs4 v-for="payApp in item.Sft" :key="payApp.name">
                  <v-flex xs2>
                    {{ payApp.display_name }}
                  </v-flex>
                  <v-flex xs2>
                    0
                  </v-flex>
                </v-flex>
                <v-flex xs4 v-for="payApp in item.Mgr" :key="payApp.name">
                  <v-flex xs2>
                    {{ payApp.display_name }}
                  </v-flex>
                  <v-flex xs2>
                    0
                  </v-flex>
                </v-flex>
              </v-flex>
            </v-row>
          </v-layout>
        </v-container> -->
      </div>
    </template>

    {{ processedTableLayoutData }}
  </v-container>
</template>
<script>
import { mapState, Store } from "vuex";
export default {
  name: "PaymentAppsLayout",
  methods: {},
  data() {
    return {
      layoutInfo: [
        {
          id: 1,
          name: "Cash",
          display_name: "Cash",
          display_in: "BOTH",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: null
        },
        {
          id: 2,
          name: "Card",
          display_name: "Card",
          display_in: "BOTH",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: null
        },
        {
          id: 3,
          name: "PhonePe",
          display_name: "PhonePe",
          display_in: "SOFTWARE",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: 1
        },
        {
          id: 4,
          name: "Gpay",
          display_name: "G-Pay",
          display_in: "SOFTWARE",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: 1
        },
        {
          id: 5,
          name: "Paytm",
          display_name: "Paytm",
          display_in: "SOFTWARE",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: 1
        },
        {
          id: 6,
          name: "PaytmBusiness",
          display_name: "Paytm Business",
          display_in: "MANAGER",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: 1
        },
        {
          id: 7,
          name: "Dineout",
          display_name: "Dineout",
          display_in: "BOTH",
          created_at: "2020-03-18T00:17:39.204185+05:30",
          last_modified: "2020-03-18T00:17:39.204185+05:30",
          is_active: true,
          category: null
        },
        {
          id: 8,
          name: "ZomatoGold",
          display_name: "Zomato Gold",
          display_in: "BOTH",
          created_at: "2020-03-18T00:17:39.205182+05:30",
          last_modified: "2020-03-18T00:17:39.205182+05:30",
          is_active: true,
          category: null
        },
        {
          id: 9,
          name: "ZomatoOnline",
          display_name: "Zomato Online",
          display_in: "BOTH",
          created_at: "2020-03-18T00:17:39.205182+05:30",
          last_modified: "2020-03-18T00:17:39.205182+05:30",
          is_active: true,
          category: null
        },
        {
          id: 10,
          name: "SwiggyOnline",
          display_name: "Swiggy Online",
          display_in: "BOTH",
          created_at: "2020-03-18T00:17:39.205182+05:30",
          last_modified: "2020-03-18T00:17:39.205182+05:30",
          is_active: true,
          category: null
        },
        {
          id: 11,
          name: "test-app-1",
          display_name: "test app 1",
          display_in: "SOFTWARE",
          created_at: "2020-03-18T00:17:39.205182+05:30",
          last_modified: "2020-03-18T00:17:39.205182+05:30",
          is_active: true,
          category: 2
        },
        {
          id: 12,
          name: "test-app-2",
          display_name: "test app 2",
          display_in: "MANAGER",
          created_at: "2020-03-18T00:17:39.205182+05:30",
          last_modified: "2020-03-18T00:17:39.205182+05:30",
          is_active: true,
          category: 2
        },
        {
          id: 13,
          name: "test-app-3",
          display_name: "test app 3",
          display_in: "MANAGER",
          created_at: "2020-03-18T00:17:39.205182+05:30",
          last_modified: "2020-03-18T00:17:39.205182+05:30",
          is_active: true,
          category: 2
        }
      ]
    };
  },
  created() {},
  computed: {
    ...mapState(["currentUserInfo"]),
    processedTableLayoutData() {
      let returnObj = {};
      this.layoutInfo.forEach(payMode => {
        var ctgry = payMode.category;
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
