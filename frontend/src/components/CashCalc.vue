<template>
  <v-card>
    <v-card-title>
      <span class="headline">Cash Count</span>
    </v-card-title>
    <v-card-text>
      <v-container name="cash-calc">
        <v-simple-table fixed-header height="300px" dense>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Denomination</th>
                <th class="text-left">Count</th>
                <th class="text-left">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in denominations" :key="index">
                <td>{{ item[0] }} X</td>
                <td>
                  <v-text-field
                    type="number"
                    hide-details
                    dense
                    single-line
                    v-model="item[1]"
                  ></v-text-field>
                </td>
                <td>{{ item[0] * item[1] }}</td>
              </tr>
              <tr>
                <td></td>
                <td>Total:</td>
                <td>{{ totalCash }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="blue darken-1" text @click="updateCash('close')">Close</v-btn>
      <v-btn color="blue darken-1" text @click="updateCash('save')">Save</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  name: "CashCalc",
  methods: {
    updateCash(action) {
      let cash = null;
      if (action === "save") {
        cash = this.totalCash;
      }
      this.$emit("cash-update", cash);
    }
  },
  data() {
    return {
      denominations: [
        [2000, 0],
        [500, 0],
        [200, 0],
        [100, 0],
        [50, 0],
        [20, 0],
        [10, 0],
        [5, 0],
        [2, 0],
        [1, 0]
      ]
    };
  },
  computed: {
    totalCash() {
      let tot = 0;
      this.denominations.forEach(d => {
        tot += d[0] * d[1];
      });
      return tot;
    }
  }
};
</script>
