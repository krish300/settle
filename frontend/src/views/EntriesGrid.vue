<template>
  <v-container>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-row class="text-center">
        <v-col cols="2">
          <v-autocomplete
            :key="selectedCategory"
            v-model="selectedCategory"
            :items="categoryOptions"
            return-object
            :rules="[v => !!v || 'Category is required']"
            label="Select Option"
            v-on:change="catgeorySelection"
            item-text="name"
          ></v-autocomplete>
        </v-col>
        <v-col cols="2">
          <v-autocomplete
            :key="entitySelected"
            v-model="entitySelected"
            :items="entityOptions"
            :rules="[v => !!v || 'Entity is required']"
            label="Select Option"
            v-on:change="entitySelection"
            return-object
            item-text="name"
          ></v-autocomplete>
        </v-col>
        <v-col cols="1">
          <v-autocomplete
            :key="modeSelected"
            v-model="modeSelected"
            :items="mode"
            :rules="[v => !!v || 'Mode  is required']"
            label="Select"
            v-on:change="modeSelection"
          ></v-autocomplete>
        </v-col>
        <v-col cols="2">
          <v-text-field
            type="number"
            v-model="price"
            :rules="[v => !!v || 'Price  is required']"
            label="Amount"
            aria-required="true"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="description"
            :rules="[v => !!v || 'Description  is required']"
            label="Description"
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

    <v-data-table :headers="headers" :items="cashOutRecords">
      <template v-slot:item="row">
        <tr>
          <td>{{ row.item.expenceCategory }}</td>
          <td>{{ row.item.entity }}</td>
          <td>{{ row.item.description }}</td>
          <td>{{ row.item.price }}</td>
          <td>
            <v-btn small fab @click="deleteItem(row.item)">
              <span class="group pa-2">
                <v-icon>delete</v-icon>
              </span>
            </v-btn>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  name: "EntriesGrid",
  components: {},
  methods: {
    catgeorySelection(data) {
      this.cashOutRecord = {};
      this.cashOutRecord.category = data;
      axios
        .get(`${process.env.VUE_APP_SERVER_URL}/api/entity/?type=${data.entity_type}`)
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
      this.cashOutRecord.entity = data.name;
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
      if (this.$refs.form.validate()) {
        this.cashOutRecord.price = this.price;
        this.cashOutRecord.description = this.description;
        this.cashOutRecords.push(this.cashOutRecord);
        this.resetModels();
      }
    },
    resetModels() {
      this.selectedCategory = null;
      this.entitySelected = "";
      this.modeSelected = "";
      this.price = "";
      this.description = "";
    },
    deleteItem(item) {
      console.log("item delete", item);
    }
  },
  data() {
    return {
      valid: true,
      selectedCategory: "",
      entitySelected: "",
      modeSelected: null,
      price: null,
      description: null,
      categoryOptions: [],
      entityOptions: [],
      showSubCategory: false,
      displayAdd: false,
      mode: ["CA", "AC", "TR"],
      headers: [
        {
          text: "Expence Category",
          value: "expenceCategory",
          align: "center",
          sortable: true
        },
        { text: "Entity", value: "entity", align: "center", sortable: false },
        {
          text: "Description",
          value: "description",
          align: "center",
          sortable: false
        },
        { text: "Amount", value: "price", align: "center", sortable: false },
        { text: "Action", vlaue: "action", align: "center", sortable: false }
      ],
      cashOutRecord: {},
      cashOutRecords: []
    };
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/entry-category/`)
      .then(response => {
        this.categoryOptions = response.data;
      })
      .catch(error => {
        console.log("error while fetching entry-category", error);
      });
  }
};
</script>