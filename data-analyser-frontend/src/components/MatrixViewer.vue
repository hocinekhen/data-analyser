<template>
  <v-row class="text-center">
    <v-col cols="12">
      <v-row></v-row>

      <v-data-table
        :headers="headers"
        :items="records"
        item-key="name"
        :search="search"
        :custom-filter="filterText"
        disable-pagination
        :hide-default-footer="false"
      >
        <template v-slot:top v-if="false">
          <v-text-field
            v-model="search"
            label="Search By column Name"
            class="mx-4"
          ></v-text-field>
        </template>
      </v-data-table>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "MatrixViewer",
  data() {
    return {
      search: "",

      records: [],
    };
  },
  props: {
    matrix: {
      type: Array,
    },
    all_headers: {
      type: Array,
    },
    matrix_headers: {
      type: Array,
    },
  },
  watch: {
    matrix_headers: function (newVal, oldVal) {
      console.log(newVal, oldVal);
      this.convertMatrixToRecords(this.matrix);
    },
    
    matrix: function (newVal, oldVal) {
      console.log(newVal, oldVal);
      console.log(newVal);

      this.convertMatrixToRecords(newVal);
    },
  },
  computed: {
    headers() {
      let newHeaders = [];
      //uncomment this to show name of rows
      /*
        newHeaders.push({
            text: '/',
            align: 'start',
            sortable: false,
            value: 'name',
          })
          */
      this.matrix_headers.forEach((header) => {
        newHeaders.push({ text: header, value: header });
      });

      return newHeaders;
    },
  },
  methods: {
    convertMatrixToRecords(matrix) {
      this.records = [];
      for (let index = 0; index < this.matrix.length; index++) {
        const row = matrix[index];
        let newRecord = {};
        for (let j = 0; j < this.matrix_headers.length; j++) {
          const value = row[j];
          let header = this.matrix_headers[j];
          newRecord[header] = value;
        }
        //uncomment this to show name of rows
        //newRecord['name'] = this.matrix_headers[index]
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
  },
  mounted() {
    this.convertMatrixToRecords(this.matrix);
  },
};
</script>
