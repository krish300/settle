<template>
  <v-app>
    <div class="login">
      <UserLogin />
    </div>
  </v-app>
</template>

<script>
// @ is an alias to /src
import UserLogin from "@/components/UserLogin.vue";
import axios from "axios";
export default {
  name: "Login",
  components: {
    UserLogin
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/settlement/latest/`)
      .then(response => {
        this.$store.commit("setInitState", response.data);
      })
      .catch(error => {
        console.log("error while fetching new settlement info", error);
      });
    axios
      .get(`${process.env.VUE_APP_SERVER_URL}/api/config/`)
      .then(response => {
        this.$store.commit("setAppConfig", response.data);
      })
      .catch(error => {
        console.log("error while fetching app config", error);
      });
  }
};
</script>
