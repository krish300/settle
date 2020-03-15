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
            :key="price"
            :rules="[v => !!v || 'Price  is required']"
            label="Amount"
            aria-required="true"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="description"
            :key="description"
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
      <template v-slot:items="props">
        <td class="text-xs-right">{{ props.item.expenceCategory }}</td>
        <td class="text-xs-right">{{ props.item.entity }}</td>
        <td class="text-xs-right">{{ props.item.description }}</td>
        <td class="text-xs-right">{{ props.item.price }}</td>
        <!-- <td class="text-xs-right"><v-icon small>test</v-icon></td> -->
      </template>
      <template>
        <v-icon small>mdi-delete</v-icon>
      </template>
    </v-data-table>
    <v-row class="text-center"></v-row>
  </v-container>
</template>
<script>
import axios from "axios";
export default {
  name: "EntriesGrid",
  components: {
  },
  methods: {
    catgeorySelection(data) {
      this.cashOutRecord = {};
      this.cashOutRecord.category = data;
      axios
        .get(
          `http://krish300.pythonanywhere.com/api/entity/?type=${data.entity_type}`
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
      this.price = null;
      this.description = null;
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
      .get("http://krish300.pythonanywhere.com/api/entry-category/")
      .then(response => {
        this.categoryOptions = response.data;
      })
      .catch(error => {
        console.log("error while fetching entry-category", error);
      });
  }
};
</script>