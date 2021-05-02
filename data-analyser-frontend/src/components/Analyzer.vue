<template>
  <div>
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Current Matrix</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items> </v-toolbar-items>
        </v-toolbar>
        <matrix-viewer
          class="mt-6"
          :matrix="matrix"
          :matrix_headers="matrix_headers"
        ></matrix-viewer>
      </v-card>
    </v-dialog>
    <p class="pl-5">This tool is made to play more with data</p>
    <v-row class="pl-8 pr-8">
      <v-col cols="4">
        <v-card class="pa-2" outlined>
          <v-btn
            color="primary"
            dark
            outlined
            class="elevation-0"
            @click="dialog = true"
          >
            Show Matrix
          </v-btn>
          <v-btn
            color="primary"
            dark
            outlined
            class="elevation-0 ml-1"
            @click="get_matrix"
          >
            Reset Matrix
          </v-btn>
          <h5 class="mt-2">Matrix Operations</h5>
          <v-expansion-panels flat class="mt-2">
            <v-expansion-panel>
              <v-expansion-panel-header class="elevation-0"
                >Merging</v-expansion-panel-header
              >
              <v-expansion-panel-content>
                <v-chip class="ma-1" @click="select_cells_columns()">
                  <span class="grey--text caption">
                    select no side effects
                  </span>
                </v-chip>
                <v-chip class="ma-1" @click="select_side_effect_columns()">
                  <span class="grey--text caption"> select side effects </span>
                </v-chip>
                <v-chip
                  class="ma-1"
                  @click="
                    selected_merge_headers = matrix_headers.filter(
                      (x) => x[0] == 'L' && x[x.length - 1] != 'x'
                    )
                  "
                >
                  <span class="grey--text caption"> select all cells </span>
                </v-chip>
                <v-select
                  :items="matrix_headers"
                  v-model="selected_merge_headers"
                  chips
                  label="Selected Columns To merge"
                  multiple
                  outlined
                >
                  <template v-slot:selection="{ item, index }">
                    <v-chip v-if="index === 0">
                      <span>{{ item }}</span>
                    </v-chip>
                    <span v-if="index === 1" class="grey--text caption">
                      (+{{ selected_merge_headers.length - 1 }} others)
                    </span>
                    <v-chip
                      v-if="
                        index === 0 &&
                        selected_merge_headers.length != matrix_headers.length
                      "
                      @click="
                        selected_merge_headers = matrix_headers.filter(
                          (x) => x == x
                        )
                      "
                    >
                      <span class="grey--text caption"> select all </span>
                    </v-chip>
                    <v-chip
                      v-if="index === 0"
                      @click="selected_merge_headers = []"
                    >
                      <span class="grey--text caption"> unselect all </span>
                    </v-chip>
                  </template>
                </v-select>
                <v-text-field
                  label="new column name"
                  v-model="merged_column_name"
                  placeholder="Placeholder"
                ></v-text-field>
                <v-btn color="green" dark @click="merge_columns()">
                  Merge Columns
                </v-btn>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
              <v-expansion-panel-header class="elevation-0"
                >Grouping</v-expansion-panel-header
              >
              <v-expansion-panel-content>
                <v-select
                  :items="matrix_headers"
                  v-model="selected_group_headers"
                  chips
                  label="Selected Columns To group"
                  multiple
                  outlined
                >
                  <template v-slot:selection="{ item, index }">
                    <v-chip v-if="index === 0">
                      <span>{{ item }}</span>
                    </v-chip>
                    <span v-if="index === 1" class="grey--text caption">
                      (+{{ selected_group_headers.length - 1 }} others)
                    </span>
                    <v-chip
                      v-if="
                        index === 0 &&
                        selected_group_headers.length != matrix_headers.length
                      "
                      @click="
                        selected_group_headers = matrix_headers.filter(
                          (x) => x == x
                        )
                      "
                    >
                      <span class="grey--text caption"> select all </span>
                    </v-chip>
                    <v-chip
                      v-if="index === 0"
                      @click="selected_group_headers = []"
                    >
                      <span class="grey--text caption"> unselect all </span>
                    </v-chip>
                    <v-chip
                      v-if="index === 0"
                      @click="
                        selected_group_headers = matrix_headers.filter(
                          (x) => x[0] == 'L' && x[x.length - 1] != 'x'
                        )
                      "
                    >
                      <span class="grey--text caption"> cells only </span>
                    </v-chip>
                  </template>
                </v-select>
                <v-btn color="green" dark @click="group_columns()">
                  Group by Column
                </v-btn>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
              <v-expansion-panel-header class="elevation-0"
                >Filtering</v-expansion-panel-header
              >
              <v-expansion-panel-content>
                <v-select
                  :items="matrix_headers"
                  v-model="selected_filter_columns"
                  chips
                  label="Selected Column To Filter"
                  multiple
                  outlined
                >
                  <template v-slot:selection="{ item, index }">
                    <v-chip v-if="index === 0">
                      <span>{{ item }}</span>
                    </v-chip>
                  </template>
                </v-select>
                <v-row>
                  <v-col cols="12" sm="6" md="3">
                    <v-text-field
                      label="Min"
                      v-model="filter_min"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-text-field
                      label="Max"
                      v-model="filter_max"
                      placeholder="Placeholder"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-btn color="green" dark @click="filter_by_column()">
                  Filter
                </v-btn>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card>
      </v-col>
      <v-col cols="8">
        <v-expansion-panels v-model="panel" multiple>
          <v-expansion-panel>
            <v-expansion-panel-header
              >Correlation Matrix</v-expansion-panel-header
            >
            <v-expansion-panel-content>
              <correlation-matrix
                :matrix="matrix"
                :matrix_headers="matrix_headers"
                :all_headers="matrix_headers"
              ></correlation-matrix>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>Regression</v-expansion-panel-header>
            <v-expansion-panel-content>
              <regression
                :matrix="matrix"
                :matrix_headers="matrix_headers"
                :all_headers="matrix_headers"
              >
              </regression>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>Chart</v-expansion-panel-header>
            <v-expansion-panel-content>
              <grouping-bar-chart
                :matrix="matrix"
                :matrix_headers="matrix_headers"
                :all_headers="matrix_headers"
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
import Services from "../services/Services";

import CorrelationMatrix from "./CorrelationMatrix.vue";
import Regression from "./Regression.vue";
import MatrixViewer from "./MatrixViewer.vue";
import GroupingBarChart from "./GroupingBarChart.vue";
export default {
  name: "Analyzer",

  components: {
    "correlation-matrix": CorrelationMatrix,
    regression: Regression,
    "matrix-viewer": MatrixViewer,
    "grouping-bar-chart": GroupingBarChart,
  },

  data: () => ({
    panel: [],
    sidebarMenu: false,
    matrix_headers: [],
    matrix: [],
    filter_min: 0,
    filter_max: 0,
    merged_column_name: "",
    selected_merge_headers: [],
    selected_group_headers: [],
    selected_filter_columns: [],
    dialog: false,
  }),
  methods: {
    merge_columns() {
      console.log(this.selected_merge_headers);
      Services.merge_columns(
        this.$notification,
        this.selected_merge_headers,
        this.merged_column_name,
        true,
        { matrix: this.matrix, columns: this.matrix_headers }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) this.$notification.error(response.message);
          else {
            this.matrix = response._Matrix__matrix;

            this.matrix_headers = response._Matrix__columns;
            this.selected_merge_headers = [];
            this.selected_filter_columns = [];
            this.selected_group_headers = [];
            this.$notification.success("Columns Merged!");
            console.log(this.matrix);
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
    group_columns() {
      console.log(this.selected_group_headers);
      Services.group_columns(
        this.$notification,
        this.selected_group_headers,
        true,
        { matrix: this.matrix, columns: this.matrix_headers }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) this.$notification.error(response.message);
          else {
            this.matrix = response._Matrix__matrix;

            this.matrix_headers = response._Matrix__columns;
            this.$notification.success("Columns Grouped!");
            console.log(this.matrix);
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
    filter_by_column() {
      console.log(this.selected_group_headers);
      Services.filter_by_column(
        this.$notification,
        this.selected_filter_columns,
        this.filter_min,
        this.filter_max,
        true,
        { matrix: this.matrix, columns: this.matrix_headers }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) this.$notification.error(response.message);
          else {
            this.matrix = response._Matrix__matrix;

            this.matrix_headers = response._Matrix__columns;
            this.$notification.success("Column Filtered!");
            console.log(this.matrix);
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
    get_matrix() {
      Services.getMatrix(this.$notification)
        .then((resp) => {
          let response = resp.data;
          if (response.error) this.$notification.error(response.message);
          else {
            this.matrix = response.data._Matrix__matrix;

            this.matrix_headers = response.data._Matrix__columns;
            this.selected_merge_headers = [];
            this.selected_filter_columns = [];
            this.selected_group_headers = [];
            console.log(this.matrix);
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },

    select_side_effect_columns() {
      Services.get_side_effect_columns(this.$notification, this.matrix_headers)
        .then((resp) => {
          let response = resp.data;
          if (response.error) this.$notification.error(response.message);
          else {
            this.selected_merge_headers = response.data;
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
    select_cells_columns() {
      Services.get_cells_columns(this.$notification, this.matrix_headers)
        .then((resp) => {
          let response = resp.data;
          if (response.error) this.$notification.error(response.message);
          else {
            this.selected_merge_headers = response.data;
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
  },

  mounted() {
    this.get_matrix();
  },
};
</script>
