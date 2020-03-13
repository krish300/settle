<template>
  <v-toolbar>
    <span class="hidden-sm-and-up"></span>
    <v-toolbar-title>Biggies</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items class="hidden-xs-only">
      <v-btn text v-for="item in menuItems" :key="item.title" :to="item.path">{{ item.title }}</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>
<script>
export default {
  name: "NavBar",
  data: () => ({
    menuItems: [
      { title: "Home", path: "/" },
      { title: "About", path: "/about" },
      { title: "Categories", path: "/categories" }
    ]
  })
};
</script>
