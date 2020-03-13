<template>
  <v-app>
    <div id="app">
      <router-view></router-view>
      
      
    </div>
  </v-app>
</template>
<script>
import HelloWorld from "./components/HelloWorld";
import router from "./router";
import Home from "../src/views/Home.vue";
import TopNavBar from "../src/views/NavigationBar.vue";
export default {
  name: "App",

  components: {
    HelloWorld,
    Home,
    TopNavBar
  },
  data() {
    return {
      isLoggedIn: false
    };
  },
  beforeCreate() {
    this.isLoggedIn = false;
    if (this.isLoggedIn) {
      router.push({ path: "home" });
    }else{
      router.push({ path: "login" });
    }
  }
};
</script>
