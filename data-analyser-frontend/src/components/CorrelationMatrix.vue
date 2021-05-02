<template>
  <v-row class="text-center">
    <v-col cols="12">
      <h1>Correlation Matrix</h1>
      <v-row></v-row>

      <v-card style="margin-top: 40px">
        <v-select
          :items="all_headers"
          v-model="selected_headers"
          chips
          label="Selected Columns"
          multiple
          outlined
          @change="column_select_change($event)"
        >
          <template v-slot:selection="{ item, index }">
            <v-chip v-if="index === 0">
              <span>{{ item }}</span>
            </v-chip>
            <span v-if="index === 1" class="grey--text caption">
              (+{{ selected_headers.length - 1 }} others)
            </span>
            <v-chip
              v-if="
                index === 1 && selected_headers.length != all_headers.length
              "
              @click="selected_headers = all_headers.filter((x) => x == x)"
            >
              <span class="grey--text caption"> select all </span>
            </v-chip>
            <v-chip
              v-if="
                index === 1 && selected_headers.length == all_headers.length
              "
              @click="selected_headers = []"
            >
              <span class="grey--text caption"> unselect all </span>
            </v-chip>
          </template>
        </v-select>

        <v-btn class="ma-2" @click="calculateCorrelation()"> Calculate </v-btn>
      </v-card>
      <v-card style="margin-top: 20px">
        <v-data-table
          :headers="headers"
          :items="records"
          item-key="name"
          :search="search"
          :custom-filter="filterText"
          disable-pagination
          :hide-default-footer="true"
        >
          <template v-slot:top v-if="false">
            <v-text-field
              v-model="search"
              label="Search By column Name"
              class="mx-4"
            ></v-text-field>
          </template>
        </v-data-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import Services from "../services/Services";
export default {
  name: "CorrelationMatrix",
  components: {},
  data() {
    return {
      is_merge: false,
      search: "",
      correlation_headers: [],

      records: [],
    };
  },
  props: {
    matrix_headers: { type: Array },
    matrix: { type: Array },
    all_headers: { type: Array },
    selected_headers: { type: Array },
    calculate_on_mount: { type: Boolean },
  },
  watch: {
    matrix_headers: function (newVal, oldVal) {
      console.log("kdjfdkfj");
      this.selected_headers = [];
      console.log(newVal, oldVal);
    },
  },
  computed: {
    headers() {
      let newHeaders = [];
      newHeaders.push({
        text: "/",
        align: "start",
        sortable: false,
        value: "name",
      });
      this.correlation_headers.forEach((header) => {
        newHeaders.push({ text: header, value: header });
      });
      return newHeaders;
    },
  },
  methods: {
    convertMatrixToRecords(matrix, _headers) {
      this.records = [];
      for (let index = 0; index < _headers.length; index++) {
        const row = matrix[index];
        let newRecord = {};
        for (let j = 0; j < _headers.length; j++) {
          const value = row[j];
          let header = _headers[j];
          newRecord[header] = value;
        }
        newRecord["name"] = _headers[index];
        this.records.push(newRecord);
      }
    },
    
    filterText(value, search, item) {
      console.log(item);
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().toLowerCase().indexOf(search.toLowerCase()) !== -1
      );
    },

    column_select_change() {
      //this.calculateCorrelation(this.selected_headers)
    },

    calculateCorrelation() {
      Services.calculateCorrelation(
        this.$notification,
        this.selected_headers,
        true,
        { matrix: this.matrix, columns: this.matrix_headers }
      )
        .then((resp) => {
          let response = resp.data.data;
          if (response.error) {
            this.$notification.error(response.message);
            return;
          }
          if (!response._Matrix__columns.length == 0)
            this.correlation_headers = response._Matrix__columns;
          //this.matrix = response.data.data._Matrix__matrix
          this.convertMatrixToRecords(
            response._Matrix__matrix,
            response._Matrix__columns
          );

          this.$notification.success("Correlation matrix is ready!");
        })
        .catch((error) => {
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
        });
    },
  },
  mounted() {
    if (!this.calculate_on_mount) return;
    this.selected_headers = this.all_headers;
    this.calculateCorrelation();
  },
};
</script>
