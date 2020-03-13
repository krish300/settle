<template>
  <div class="home">
  <UserLogin />
  </div>
</template>

<script>
// @ is an alias to /src
import UserLogin from "@/components/UserLogin.vue";
import Login from "./Login.vue";

export default {
  name: "Home",
  components: {
    UserLogin
  }
};
</script>
