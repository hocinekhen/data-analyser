<template>
  <v-container>
    <v-card style="margin-top: 40px">
      <v-select
        :items="all_headers"
        v-model="selected_headers"
        chips
        label="First Column"
        multiple
        outlined
        @change="first_column_select_change($event)"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip v-if="index === 0 || index === 1">
            <span>{{ item }}</span>
          </v-chip>
          <span v-if="index === 2" class="grey--text caption">
            (+{{ selected_headers.length - 1 }} others)
          </span>
        </template>
      </v-select>
      <v-select
        :items="all_headers"
        v-model="second_columns"
        chips
        label="Second Column"
        multiple
        outlined
        @change="second_column_select_change($event)"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip v-if="index === 0">
            <span>{{ item }}</span>
          </v-chip>
          <span v-if="index === 1" class="grey--text caption">
            (+{{ second_columns.length - 1 }} others)
          </span>
          <v-chip
            v-if="index === 1 && second_columns.length != all_headers.length"
            @click="second_columns = all_headers.filter((x) => x == x)"
          >
            <span class="grey--text caption"> select all </span>
          </v-chip>
          <v-chip
            v-if="index === 1 && second_columns.length == all_headers.length"
            @click="second_columns = []"
          >
            <span class="grey--text caption"> unselect all </span>
          </v-chip>
          <v-chip
            v-if="index === 1"
            @click="
              second_columns = all_headers.filter(
                (x) => x[0] == 'L' && x[x.length - 1] != 'x'
              )
            "
          >
            <span class="grey--text caption"> cells only </span>
          </v-chip>
        </template>
      </v-select>
      <v-btn class="ma-2" @click="calculateRegression()"> Calculate </v-btn>
    </v-card>
    <v-row v-if="regression_x && regression_y" class="mt-4" justify="center">
      <h1>{{ "y = " + regression_x + "* x + " + regression_y }}</h1>
    </v-row>
    <v-chart
      class="chart"
      :option="option"
      style="margin-top: 40px; padding-left: 20%"
    />
  </v-container>
</template>

<script>
import "echarts/lib/chart/line";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart, PieChart, ScatterChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  PolarComponent,
  GeoComponent,
  SingleAxisComponent,
  ParallelComponent,
  CalendarComponent,
  GraphicComponent,
  ToolboxComponent,
  AxisPointerComponent,
  BrushComponent,
  TimelineComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
  VisualMapComponent,
  VisualMapContinuousComponent,
  VisualMapPiecewiseComponent,
  AriaComponent,
  DatasetComponent,
  TransformComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import Services from "../services/Services";

use([
  CanvasRenderer,
  PieChart,
  ScatterChart,
  LineChart,
  LegendComponent,
  GridComponent,
  PolarComponent,
  GeoComponent,
  SingleAxisComponent,
  ParallelComponent,
  CalendarComponent,
  GraphicComponent,
  ToolboxComponent,
  TooltipComponent,
  AxisPointerComponent,
  BrushComponent,
  TitleComponent,
  TimelineComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
  VisualMapComponent,
  VisualMapContinuousComponent,
  VisualMapPiecewiseComponent,
  AriaComponent,
  DatasetComponent,
  TransformComponent,
]);

export default {
  name: "Regression",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  data() {
    return {
      first_column: "",
      second_column: "",
      regression_x: 0,
      regression_y: 0,
      option: {},
    };
  },
  props: {
    matrix_headers: { type: Array },
    matrix: { type: Array },
    all_headers: { type: Array },
    calculate_on_mount: { type: Boolean },
    selected_headers: { type: Array },
    second_columns: { type: Array },
  },
  watch: {
    matrix_headers: function (newVal, oldVal) {
      this.selected_headers = [];
      this.first_column = "";
      this.second_columns = [];
      this.second_column = "";
      console.log(newVal, oldVal);
    },
  },
  methods: {
    first_column_select_change(columns) {
      console.log(columns);
      if (this.selected_headers.length > 1) {
        let lastcolumn = this.selected_headers[
          this.selected_headers.length - 1
        ];
        this.selected_headers = [];
        this.selected_headers.push(lastcolumn);
      }
    },
    second_column_select_change(columns) {
      console.log(columns);
      if (this.second_columns.length > 1) {
        let lastcolumn = this.second_columns[this.second_columns.length - 1];
        this.second_columns = [];
        this.second_columns.push(lastcolumn);
      }
    },

    calculateRegression() {
      Services.calculateRegression(
        this.$notification,
        [this.selected_headers[0], this.second_columns[0]],
        true,
        { matrix: this.matrix, columns: this.matrix_headers }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          if (!response._Matrix__columns.length == 0) {
            this.regression_x = response.regression_coeff.a.toFixed(3);
            this.regression_y = response.regression_coeff.b.toFixed(2);
            this.updateData(response._Matrix__matrix);
            this.$notification.success("Regression Info are ready!");
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },

    drawLinePoints(x, y) {
      console.log(x, y);
      let minpoint = {
        coord: [(0 - this.regression_y) / this.regression_x, 0],
        symbol: "none",
      };
      let maxpoint = {
        coord: [0, 0 * this.regression_x + this.regression_y],
        symbol: "none",
      };
      this.option.series[0].markLine.data = [[minpoint, maxpoint]];
    },

    updateData(data) {
      this.option.series[0].data = data;
      console.log([(0 - this.regression_y) / this.regression_x, 0]);
      this.drawLinePoints(this.regression_x, this.regression_y);
    },

    getscatterOptions() {
      var dataAll = [];

      var markLineOpt = {
        responsive: true,
        animation: false,
        label: {
          formatter: "y = " + this.regression_x + " * x + " + this.regression_y,
          align: "right",
        },
        lineStyle: {
          type: "solid",
          normal: {
            color: "red",
          },
        },
        xAxis: [
          {
            gridIndex: 0,
            ticks: {
              suggestedMin: 0,
              suggestedMax: 100,
            },
          },
        ],
        yAxis: [
          {
            gridIndex: 0,
            ticks: {
              suggestedMin: 0,
              suggestedMax: 100,
            },
          },
        ],
        tooltip: {
          formatter: "y = " + this.regression_x + " * x + " + this.regression_y,
        },
        data: [
          [
            {
              coord: [0, 5],
              symbol: "none",
            },
            {
              coord: [5, 0],
              symbol: "none",
            },
          ],
        ],
      };

      let option = {
        responsive: true,
        title: {
          text: "Scaled data between -1 and 1",
          left: "center",
          top: 0,
        },
        grid: [{ left: "7%", bottom: "10%", width: "100%", height: "80%" }],

        tooltip: {
          formatter: " {a}: ({c})",
        },
        xAxis: [{ gridIndex: 0, min: 0, max: 1.2 }],
        yAxis: [{ gridIndex: 0, min: 0, max: 1.1 }],
        series: [
          {
            name: "I",
            type: "scatter",
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: dataAll[0],
            markLine: markLineOpt,
          },
        ],
      };
      return option;
    },
  },

  mounted() {
    this.option = this.getscatterOptions();
    if (!this.calculate_on_mount) return;
    this.calculateRegression();
  },
};
</script>

<style scoped>
.chart {
  height: 400px;
  width: 70%;
}
</style>