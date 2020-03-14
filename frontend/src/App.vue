<template>
  <v-app>
    <div id="app">
      <v-toolbar app>
        <span class="hidden-sm-and-up">
          <v-toolbar-side-icon @click="sidebar = !sidebar"></v-toolbar-side-icon>
        </span>
        <v-toolbar-title>Biggies</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-xs-only">
          <v-btn flat v-for="item in menuItems" :key="item.title" :to="item.path">{{ item.title }}</v-btn>
        </v-toolbar-items>
      </v-toolbar>

      <router-view />
    </div>

    <v-content>
      <HelloWorld />
    </v-content>
  </v-app>
</template>

<script>
import HelloWorld from "./components/HelloWorld";

export default {
  name: "App",

  components: {
    HelloWorld
  },

  data: () => ({
    sidebar: false,
    menuItems: [
      { title: "Home", path: "/" },
      { title: "About", path: "/about" },
      { title: "Categories", path: "/categories" }
    ]
  })
};
</script>
