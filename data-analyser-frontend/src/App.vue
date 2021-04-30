<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon
        @click.stop="sidebarMenu = !sidebarMenu"
      ></v-app-bar-nav-icon>

      <div class="d-flex align-center">
        <v-img
          alt="analyser Logo"
          class="shrink mr-2"
          contain
          src="./assets/analyser.png"
          transition="scale-transition"
          width="0"
        />

        <v-img
          alt="analyser"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="40"
          src="./assets/analyser.png"
          width="40"
        />
      </div>

      <v-spacer></v-spacer>
      <v-btn
        v-if="$route.path != '/upload'"
        @click="$router.push('/upload')"
        color="green"
        dark
      >
        <v-icon>mdi-cloud-upload</v-icon>
        Upload File
      </v-btn>
      <v-btn v-if="false" href="https://google.com/" target="_blank" text>
        <span class="mr-2">Website</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer
      v-model="sidebarMenu"
      app
      floating
      :permanent="sidebarMenu"
      color="#ecf0f1"
    >
      <v-list dense>
        <v-list-item>
          <v-list-item-action>
            <v-icon @click.stop="sidebarMenu = !sidebarMenu"
              >mdi-chevron-left</v-icon
            >
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              <h3 class="font-weight-thin"></h3>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-list dense>
        <v-list-item
          v-for="route in routes"
          :key="route.route"
          router
          :to="route.route"
        >
          <v-list-item-icon>
            <v-icon>{{ route.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ route.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <router-view class="pt-16 mt-6" />
  </v-app>
</template>

<script>
export default {
  name: "App",

  components: {},

  data: () => ({
    sidebarMenu: false,
    matrix: [],
    routes: [
      { icon: "mdi-home-analytics", title: "Welcome", route: "/" },
      { icon: "mdi-chart-scatter-plot", title: "Analyzer", route: "/analyzer" },
      { icon: "mdi-matrix", title: "Results", route: "/results" },
    ],
  }),
  methods: {},
  mounted() {
    if (!localStorage.getItem("file_name"))
      this.$notification.warning(
        "No csv file Uploaded yet! Please Upload one!"
      );
  },
};
</script>
