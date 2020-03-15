<template>
  <v-content>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-alert type="error" dismissible v-if="showError"
            >Invalid User Details</v-alert
          >
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>User Login</v-toolbar-title>
              <v-spacer />
            </v-toolbar>
            <v-card-text>
              <v-form ref="form">
                <v-autocomplete
                  label="Select User"
                  name="login"
                  prepend-icon="person"
                  :key="userName"
                  v-model="userName"
                  :items="userNames"
                  :rules="[v => !!v || 'User Name is required']"
                  v-on:change="userNameChange"
                  @click.native="showError = false"
                ></v-autocomplete>
                <v-text-field
                  :rules="[v => !!v || 'Password is required']"
                  id="password"
                  label="Password"
                  name="password"
                  prepend-icon="lock"
                  type="password"
                  v-model="password"
                  clearable
                  @click.native="showError = false"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn color="primary" @click.native="login">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>
<script>
import router from "../router";
export default {
  name: "UserLogin",
  methods: {
    login() {
      this.invalidUser = true;
      if (this.$refs.form.validate()) {
        // validate login
        if (this.password == "1234") {
          this.invalidUser = false;
        }
        if (this.invalidUser) {
          console.log("inside for invalid user", this.invalidUser);
          // reset the form
          // display error message
          this.password = "";
          this.showError = true;
        } else {
          router.push({ path: "home" });
        }
      }
    },
    userNameChange() {},
    resetModel() {}
  },
  data() {
    return {
      valid: true,
      showError: false,
      invalidUser: false,
      userName: "",
      password: "",
      userNames: ["Krishna", "Shiva", "Sandeep"]
    };
  }
};
</script>
