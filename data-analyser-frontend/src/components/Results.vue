<template>
  <div>
    <b class="pl-5"
      >*This simple page is just made for giving a sample on what this platform
      is developed for.</b
    >
    <p class="pl-5">
      *These results are specific to the example file named users.csv file that
      can be found in the github repository under the backend application
      folder, you can use the analyzer tool to analyze other files after
      uploading it
    </p>
    <p class="pl-5">
      *These results are generated using the analyzer tool functionalities, here
      we are just displaying
    </p>
    <p class="pl-5">
      *The interpretation of result is mostly the same for all the cell's
      parameters
    </p>
    <v-row class="pl-8 pr-8">
      <v-col cols="4">
        <v-card class="pa-2" outlined>
          <v-select
            class="mt-3"
            :items="params_list"
            v-model="target_parameter"
            chips
            label="Select Target parameter"
            outlined
          >
            <template v-slot:selection="{ item, index }">
              <v-chip v-if="index === 0">
                <span>{{ item }}</span>
              </v-chip>
            </template>
          </v-select>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="pl-8 pr-8">
      <v-col cols="8">
        <v-alert border="top" color="red lighten-2" dark>
          In my next lines, by saying <b>users_in_cells</b> I mean the average
          users in the cells that are not side effect.
          <br />
          and by saying <b>users_in_side_effects</b> I mean the average users in
          the side effect cells.
        </v-alert>
        <p>
          The first operation that comes to mind is calculating the correlation
          for the presented data, and this is to see if there is any dependence
          between the different cells parameter x and the average number of
          users in the network. What I noticed is that the correlation between
          the parameter x and <b>users_in_cells</b> is relatively weak which
          means (for the moment only) that the parameter x does not have strong
          effect on the <b>users_in_cells</b>. Ofcourse, this might or might not
          be true, since there can be more reasons for having such correlation.
          <br />
          But by considering more the correlation matrix (shown bellow), we can
          notice that hour has an important impact on the <b>users_in_cells</b>,
          which led me to take it into consideration in my study along side with
          the parameter_x.
        </p>
        <v-expansion-panels flat multiple>
          <v-expansion-panel>
            <v-expansion-panel-header color="green"
              >Correlation Matrix</v-expansion-panel-header
            >
            <v-expansion-panel-content v-if="result_is_ready">
              <correlation-matrix
                calculate_on_mount="true"
                :matrix="matrix_to_correlate"
                :matrix_headers="merged_headers"
                :all_headers="merged_headers"
              ></correlation-matrix>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <p>
          To visulize more the dependence between hour and
          <b>users_in_cells</b>, the bellow scatter plot demonstrates how the
          points constructed by hours in the x axis and <b>users_in_cells</b> in
          y axis are forming a coordinated set where it is easy to draw a line
          that fit most of the points. This reflects how a change in the hour
          can change the average number of users too.
        </p>
        <v-expansion-panels flat multiple>
          <v-expansion-panel>
            <v-expansion-panel-header color="green"
              >Regression</v-expansion-panel-header
            >
            <v-expansion-panel-content v-if="result_is_ready">
              <regression
                calculate_on_mount="true"
                :selected_headers="['Hour']"
                :second_columns="[no_side_cells_column_name]"
                :matrix="merged_matrix"
                :matrix_headers="merged_headers"
                :all_headers="merged_headers"
              >
              </regression>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <p>
          However, our main objective is to see how can a specific parameter_x
          affect the users number. Thus, by grouping the data presented in
          <b>users.csv</b> by column and parameter_x, I got the below plot that
          shows clearly the increase of <b>users_in_cells</b> by time. Where the
          <b>users_in_cells</b> is at its lowest between 0 and 9 and gets to its
          highest between 10 and 23. <br />
          <b
            >But, the interesting thing is users_in_cells is remarquably bigger
            when the parameter_x is bigger.</b
          >
        </p>
        <v-expansion-panels flat multiple>
          <v-expansion-panel>
            <v-expansion-panel-header color="green"
              >Chart</v-expansion-panel-header
            >
            <v-expansion-panel-content v-if="result_is_ready">
              <grouping-bar-chart
                calculate_on_mount="true"
                :selected_headers="['Hour']"
                :second_columns="[target_parameter]"
                :values_columns="[no_side_cells_column_name]"
                :matrix="merged_matrix"
                :matrix_headers="merged_headers"
                :all_headers="merged_headers"
              >
              </grouping-bar-chart>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ResultsServices from "../services/Services";

import CorrelationMatrix from "./CorrelationMatrix.vue";
import Regression from "./Regression.vue";
import GroupingBarChart from "./GroupingBarChart.vue";
export default {
  name: "Results",

  components: {
    "correlation-matrix": CorrelationMatrix,
    regression: Regression,
    "grouping-bar-chart": GroupingBarChart,
  },

  data: () => ({
    panel: [],
    sidebarMenu: false,
    result_is_ready: false,
    params_list: [],
    target_parameter: "L1547777_x",
    side_effect_columns: [],
    no_side_cells: [],
    no_side_cells_column_name: "users_in_cells",
    side_effects_column_name: "users_in_side_effects",
    matrix_headers: [],
    matrix: [],
    grouped_matrix: [],
    merged_matrix: [],
    merged_headers: [],
    matrix_to_correlate: [],
    merged_column_name: "",
  }),
  watch: {
    matrix_headers: function (newVal, oldVal) {
      this.params_list = newVal.filter((x) => x.endsWith("_x"));
      this.select_cells_columns(newVal);
      console.log(newVal, oldVal);
    },
    no_side_cells: function (newVal, oldVal) {
      console.log("noooss");
      console.log(this.matrix);
      this.merge_columns(
        this.matrix,
        this.matrix_headers,
        newVal,
        this.no_side_cells_column_name
      );
      console.log(newVal, oldVal);
    },
    side_effect_columns: function (newVal, oldVal) {
      this.merge_columns(
        this.merged_matrix,
        this.merged_headers,
        newVal,
        this.side_effects_column_name
      );
      console.log(newVal, oldVal);
    },
    target_parameter: function (newVal, oldVal) {
      this.get_matrix();
      console.log(newVal, oldVal);
    },
  },
  methods: {
    merge_columns(matrix, columns, columns_to_merge, new_column_name) {
      ResultsServices.merge_columns(
        this.$notification,
        columns_to_merge,
        new_column_name,
        true,
        { matrix: matrix, columns: columns }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          this.merged_matrix = response._Matrix__matrix;

          this.merged_headers = response._Matrix__columns;
          if (new_column_name == this.no_side_cells_column_name) {
            this.select_side_effect_columns(this.merged_headers);
            return;
          }
          this.matrix_to_correlate = [...this.merged_matrix];
          this.group_columns(this.merged_matrix, this.merged_headers, [
            "Hour",
            this.target_parameter,
          ]);
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },

    group_columns(matrix, columns, columns_to_group) {
      console.log(this.selected_group_headers);
      ResultsServices.group_columns(
        this.$notification,
        columns_to_group,
        true,
        { matrix: matrix, columns: columns }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          this.grouped_matrix = response._Matrix__matrix;
          this.result_is_ready = true;
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },

    get_matrix() {
      this.result_is_ready = false;
      ResultsServices.getMatrix(this.$notification, "users.csv")
        .then((resp) => {
          let response = resp.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          this.matrix = response.data._Matrix__matrix;

          this.matrix_headers = response.data._Matrix__columns;
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },

    select_side_effect_columns(columns) {
      ResultsServices.get_side_effect_columns(this.$notification, columns)
        .then((resp) => {
          let response = resp.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          this.side_effect_columns = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    
    select_cells_columns(columns) {
      ResultsServices.get_cells_columns(this.$notification, columns)
        .then((resp) => {
          let response = resp.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          this.no_side_cells = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  mounted() {
    this.get_matrix();
  },
};
</script>
