<template>
  <v-app>
    <PaymentAppsLayout />
    <!-- <template>
      <v-data-table
        item-key="name"
        class="elevation-1"
        loading
        loading-text="Loading... Please wait"
      ></v-data-table>
    </template> -->
  </v-app>
</template>

<script>
// @ is an alias to /src
//import <other-comp> from "@/components/<other-comp>.vue";
import PaymentAppsLayout from "@/components/PaymentAppsLayout.vue";
export default {
  name: "SaleSummary",
  components: {
    PaymentAppsLayout
  }
};
</script>
