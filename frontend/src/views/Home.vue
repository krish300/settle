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
        Settlement For Date: 14-Mar-2020
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- <v-btn icon @click="extendedCalander=!extendedCalander"> -->
      <span inline-block align="right">
        <v-dialog ref="dialog" v-model="modal" :return-value.sync="date" persistent width="25%">
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="date"
              prepend-icon="event"
              readonly
              v-on="on"
              inline-block
            ></v-text-field>
          </template>
          <v-date-picker v-model="date" type="date" scrollable>
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="modal = false">Cancel</v-btn>
            <v-btn text color="primary" @click="$refs.dialog.save(date)">OK</v-btn>
          </v-date-picker>
        </v-dialog>
      </span>
      <!-- <template v-slot:extension v-if="extendedCalander">
          <v-date-picker full-width class="mb-4" />
      </template> -->
    </v-app-bar>
    <!-- Sizes your content based upon application components -->
    <v-content>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- <EntriesGrid /> -->
        <component :is="viewName" />
        <!-- If using vue-router -->
        <!-- <router-view /> -->
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import EntriesGrid from "@/components/EntriesGrid";
import SaleSummary from "@/components/SaleSummary";

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
    date: new Date().toISOString().substr(0, 7),
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
  })
};
</script>
