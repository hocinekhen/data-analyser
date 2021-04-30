<template>
  <v-container>
    <v-card style="margin-top: 40px">
      <v-select
        :items="all_headers"
        v-model="selected_headers"
        chips
        label="X axis"
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
        label="Y axis"
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
        </template>
      </v-select>
      <v-select
        :items="all_headers"
        v-model="values_columns"
        chips
        label="Values column"
        multiple
        outlined
        @change="values_column_select_change($event)"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip v-if="index === 0">
            <span>{{ item }}</span>
          </v-chip>
          <span v-if="index === 1" class="grey--text caption">
            (+{{ second_columns.length - 1 }} others)
          </span>
        </template>
      </v-select>
      <v-btn class="ma-2" @click="get_series()"> Calculate </v-btn>
    </v-card>
    <v-row v-if="regression_x && regression_y" class="mt-4" justify="center">
      <h1>{{ "y = " + regression_x + "* x + " + regression_y }}</h1>
    </v-row>
    <v-chart
      v-if="show_chart"
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
import { BarChart, LineChart, PieChart, ScatterChart } from "echarts/charts";
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
  BarChart,
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
  name: "GroupingBarChart",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  data() {
    return {
      show_chart: true,

      labelOption: null,
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
    values_columns: { type: Array },
  },
  watch: {
    matrix_headers: function (newVal, oldVal) {
      this.selected_headers = [];
      this.first_column = "";
      this.second_columns = [];
      this.second_column = "";

      console.log("kdjfdkfj");
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
    values_column_select_change(columns) {
      console.log(columns);
      if (this.values_columns.length > 1) {
        let lastcolumn = this.values_columns[this.values_columns.length - 1];
        this.values_columns = [];
        this.values_columns.push(lastcolumn);
      }
    },
    get_series() {
      Services.get_series(
        this.$notification,
        this.selected_headers[0],
        this.second_columns[0],
        this.values_columns[0],
        true,
        { matrix: this.matrix, columns: this.matrix_headers }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) this.$notification.error(response.message);
          else {
            //this.matrix_headers = response._Matrix__columns
            //this.matrix = response._Matrix__matrix
            this.updateData(response);
            this.$notification.success(" Info are ready!");
          }
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
    updateData(data) {
      this.show_chart = false;
      this.option.series = [];
      this.option = this.drawBarChart(data.axis_x, data.axis_y, data.groups);
      this.show_chart = true;
    },
    drawBarChart(axis_x, series, groups) {
      series.forEach((element) => {
        element.type = "line";
        element.label = this.labelOption;
        element.emphasis = {
          focus: "series",
        };
      });
      var posList = [
        "left",
        "right",
        "top",
        "bottom",
        "inside",
        "insideTop",
        "insideLeft",
        "insideRight",
        "insideBottom",
        "insideTopLeft",
        "insideTopRight",
        "insideBottomLeft",
        "insideBottomRight",
      ];
      let app = {};
      app.configParameters = {
        rotate: {
          min: -90,
          max: 90,
        },
        align: {
          options: {
            left: "left",
            center: "center",
            right: "right",
          },
        },
        verticalAlign: {
          options: {
            top: "top",
            middle: "middle",
            bottom: "bottom",
          },
        },
        position: {
          options: posList.reduce(function (map, pos) {
            map[pos] = pos;
            return map;
          }, {}),
        },
        distance: {
          min: 0,
          max: 100,
        },
      };

      app.config = {
        rotate: 90,
        align: "left",
        verticalAlign: "middle",
        position: "insideBottom",
        distance: 15,
      };

      this.labelOption = {
        position: app.config.position,
        distance: app.config.distance,
        align: app.config.align,
        verticalAlign: app.config.verticalAlign,
        rotate: app.config.rotate,
        formatter: "{c}  {name|{a}}",
        fontSize: 16,
        rich: {
          name: {},
        },
      };

      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        legend: {
          data: groups,
        },
        toolbox: {
          show: true,
          orient: "vertical",
          left: "right",
          top: "center",
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar", "stack", "tiled"] },
            restore: { show: true },
            saveAsImage: { show: true },
          },
        },
        xAxis: [
          {
            type: "category",
            axisTick: { show: false },
            data: axis_x,
          },
        ],
        yAxis: [
          {
            type: "value",
          },
        ],
        series: series,
      };
      return option;
    },
  },
  mounted() {
    if (this.calculate_on_mount) {
      this.get_series();
    }
  },
};
</script>

<style scoped>
.chart {
  height: 400px;
  width: 70%;
}
</style>