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

export default {
  name: "Login",
  components: {
    UserLogin
  }
};
</script>
