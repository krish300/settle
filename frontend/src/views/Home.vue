<template>
  <v-app>
    <nav>
      <v-navigation-drawer v-model="drawer" app clipped="clipped">
        <v-list dense>
          <!-- <v-list-item v-for="link in links" :key="link.text" router  :to="link.route"> -->
          <v-list-item
            v-for="link in links"
            :key="link.text"
            @click.stop="viewName = link.compName"
          >
            <v-list-item-action>
              <v-icon>{{ link.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>{{ link.text }}</v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </nav>
    <v-app-bar clipped-left app color="primary" dark extension-height="100%">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title class="font-italic font-weight-bold">
        {{ settlementName }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>

      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn color="primary" v-on="on">
            {{ currentUserName }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <!-- <v-btn icon @click="extendedCalander=!extendedCalander"> -->
      <!-- <span inline-block justify="end" align="center"> -->
      <v-dialog ref="dialog" v-model="modal" :return-value.sync="date" persistent width="25%">
        <template v-slot:activator="{ on }">
          <v-text-field
            v-model="date"
            prepend-inner-icon="event"
            hide-details="auto"
            readonly
            dense
            v-on="on"
            class="datePickerTxtField"
          ></v-text-field>
        </template>
        <v-date-picker v-model="date" type="date" scrollable>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="modal = false">Cancel</v-btn>
          <v-btn text color="primary" @click="$refs.dialog.save(date)">OK</v-btn>
        </v-date-picker>
      </v-dialog>
      <!-- </span> -->
      <!-- <template v-slot:extension v-if="extendedCalander">
          <v-date-picker full-width class="mb-4" />
      </template> -->
    </v-app-bar>
    <!-- Sizes your content based upon application components -->
    <v-content style="padding-top:0px;">
      <!-- Provides the application the proper gutter -->
      <v-container fluid dense>
        <!-- <EntriesGrid /> -->
        <component :is="viewName" />
        <!-- If using vue-router -->
        <!-- <router-view /> -->
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import EntriesGrid from "./EntriesGrid";
import SaleSummary from "./SaleSummary";
import { mapState, mapGetters } from "vuex";

export default {
  name: "Home",

  components: {
    EntriesGrid,
    SaleSummary
  },

  data: () => ({
    drawer: false,
    clipped: true,
    viewName: "EntriesGrid",
    date: new Date().toISOString().substr(0, 10),
    modal: false,
    //extendedCalander: false,
    links: [
      {
        icon: "home",
        text: "CashOut Entries",
        route: "/",
        compName: "EntriesGrid"
      },
      {
        icon: "folder",
        text: "Sale Summary",
        route: "/salesummary",
        compName: "SaleSummary"
      }
    ]
  }),

  computed: {
    ...mapState(["currentUserInfo", "settlementName"]),
    ...mapGetters(["currentUserName"])
  }
};
</script>

<style lang="scss">
.datePickerTxtField {
  max-width: 130px !important;
}
</style>
