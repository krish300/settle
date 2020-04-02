<template>
  <v-container>
    <v-alert type="error" v-model="addEntryError" dismissible>
      {{ alertErrorMessage }}
    </v-alert>
    <v-form ref="addEntryForm" v-model="valid" lazy-validation>
      <v-row class="text-center" dense>
        <v-col cols="2">
          <v-autocomplete
            v-model="selectedCategory"
            :items="entryCategoryOptions"
            return-object
            :rules="[v => !!v || 'Category is required']"
            label="Select Option"
            v-on:change="expCatgeorySelection"
            item-text="name"
            item-value="id"
            cache-items
          ></v-autocomplete>
        </v-col>
        <v-col cols="2">
          <v-autocomplete
            v-model="entitySelected"
            :items="entityOptions"
            :rules="[v => !!v || 'Entity is required']"
            label="Select Option"
            v-on:change="entitySelection"
            return-object
            item-text="name"
            item-value="id"
            :menu-props="menuProps"
          ></v-autocomplete>
        </v-col>
        <v-col cols="1" v-if="isAdmin">
          <v-autocomplete
            v-model="modeSelected"
            :items="mode"
            :rules="[v => !!v || 'Mode  is required']"
            label="Select"
            v-on:change="modeSelection"
            cache-items
          ></v-autocomplete>
        </v-col>
        <v-col cols="2">
          <v-text-field
            type="number"
            v-model="enteredAmount"
            :rules="[v => !!v || 'Amount  is required']"
            label="Amount"
            aria-required="true"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="enteredComment"
            :rules="[v => !!v || 'Comment  is required']"
            label="Comment"
            clearable
          ></v-text-field>
        </v-col>
        <v-col class="text-center" cols="2" sm="2">
          <div class="my-2">
            <v-btn large color="primary" v-on:click="addRow">Add</v-btn>
          </div>
        </v-col>
      </v-row>
    </v-form>

    <v-data-table :headers="headers" :items="cashOutRecords" item-key="id" dense>
      <template v-slot:item="row">
        <tr>
          <td>{{ row.item.expense_category }}</td>
          <td>{{ row.item.entity_name }}</td>
          <td>{{ row.item.amount }}</td>
          <td>{{ row.item.comment }}</td>
          <td>
            <v-icon small color="red" dense @click="deleteItem(row.item)"> delete </v-icon>
          </td>
        </tr>
      </template>
    </v-data-table>
    <v-row dense>
      <v-col class="text-center"></v-col>
      <v-col class="text-center"
        ><v-card color="teal lighten-1">Total Cash Expenses: {{ this.totalCashExpense }} </v-card>
      </v-col>
      <v-col class="text-center">Total Expenses: {{ this.totalExpense }} </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from "axios";
import { mapState, mapGetters, Store } from "vuex";
export default {
  name: "EntriesGrid",
  components: {},
  methods: {
    expCatgeorySelection(data) {
      console.log(data);
      this.cashOutRecord = {};
      this.cashOutRecord.category = data.id;
      data.expense_category = data.expense_category || "";
      axios
        .get(
          `${process.env.VUE_APP_SERVER_URL}/api/entity/?type=${data.entity_type}&category=${data.expense_category}`
        )
        .then(response => {
          if (response.data.length > 0) {
            this.entityOptions = response.data;
          }
        })
        .catch(error => {
          console.log("error while fetching entities", error);
        });
    },
    entitySelection(data) {
      this.cashOutRecord.entity = data.id;
      this.cashOutRecord.expenceCategory = data.expense_category;
    },
    modeSelection(data) {
      if (data === null || data === undefined) {
        this.cashOutRecord.mode = "CA";
        this.modeSelected = "CA";
      } else {
        this.cashOutRecord.mode = data;
        this.modeSelected = data;
      }
    },
    addRow() {
      if (this.$refs.addEntryForm.validate()) {
        this.cashOutRecord.amount = this.enteredAmount;
        this.cashOutRecord.comment = this.enteredComment;
        this.cashOutRecord.date = this.settlementDate;
        this.cashOutRecord.settlement = this.settlementId;
        this.cashOutRecord.created_by = this.currentUserName;
        axios({
          method: "POST",
          url: `${process.env.VUE_APP_SERVER_URL}/api/entry/`,
          data: this.cashOutRecord,
          xsrfHeaderName: "X-CSRFToken"
        })
          .then(response => {
            this.$refs.addEntryForm.reset();
            //this.$refs.addEntryForm.resetValidation();
            this.cashOutRecords.push(response.data);
            this.updateTotalExpenses();
          })
          .catch(error => {
            this.alertErrorMessage = "error while adding the entry please call admin.";
            this.addEntryError = true;
            console.log("error while creating an entry", error);
          });
      }
    },
    deleteItem(entry) {
      axios({
        method: "DELETE",
        url: `${process.env.VUE_APP_SERVER_URL}/api/entry/${entry.id}/`,
        xsrfHeaderName: "X-CSRFToken"
      })
        .then(response => {
          const ind = this.cashOutRecords.indexOf(entry);
          this.cashOutRecords.splice(ind, 1);
          this.updateTotalExpenses();
        })
        .catch(error => {
          this.alertErrorMessage = "error while deleting the entry please call admin.";
          this.addEntryError = true;
          console.log("error while deleting the entry", error);
        });
    },
    updateTotalExpenses() {
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/api/settlement/${this.settlementId}/`)
        .then(response => {
          this.$store.commit("setTotalExpense", response.data.expense);
          this.$store.commit("setTotalCashExpense", response.data.cash_expense);
        })
        .catch(error => {
          console.log("error while fetching settlment data", error);
        });
    }
  },
  data() {
    return {
      //settlementId: null,
      valid: true,
      selectedCategory: "",
      entitySelected: "",
      modeSelected: null,
      enteredAmount: null,
      enteredComment: null,
      entryCategoryOptions: [],
      entityOptions: [],
      showSubCategory: false,
      displayAdd: false,
      addEntryError: false,
      alertErrorMessage: "",
      mode: [
        { value: "CA", text: "CASH" },
        { value: "AC", text: "ACCOUNT" },
        { value: "TR", text: "TRESSURE" }
      ],
      headers: [
        {
          text: "Expence Category",
          value: "expenceCategory",
          align: "center",
          sortable: true
        },
        { text: "Entity", value: "entity", align: "center", sortable: false },
        { text: "Amount", value: "amount", align: "center", sortable: false },
        {
          text: "Comment",
          value: "comment",
          align: "center",
          sortable: false
        },
        { text: "Action", vlaue: "action", align: "center", sortable: false }
      ],
      menuProps: {
        closeOnClick: false,
        closeOnContentClick: false,
        disableKeys: true,
        openOnClick: false,
        maxHeight: 304,
        auto: true,
        dense: true
      },
      cashOutRecord: {},
      cashOutRecords: []
    };
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/entry-category/`)
      .then(response => {
        this.entryCategoryOptions = response.data;
      })
      .catch(error => {
        console.log("error while fetching entry-category", error);
      });
  },
  mounted() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/entry/?settlement=${this.settlementId}`)
      .then(response => {
        this.cashOutRecords = response.data;
        this.updateTotalExpenses();
      })
      .catch(error => {
        console.log("error while fetching existing entries", error);
      });
  },
  computed: {
    ...mapState([
      "totalCashExpense",
      "totalExpense",
      "settlementId",
      "currentUserName",
      "settlementDate"
    ]),
    ...mapGetters(["currentUserName", "isAdmin"])
  }
};
</script>
