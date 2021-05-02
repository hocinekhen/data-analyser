<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/file.png')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Upload your CSV file</h1>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col class="" cols="6">
        <v-row justify="center">
          <v-file-input
            show-size
            label="File input"
            v-model="currentFile"
            @change="selectFile"
            accept=".csv"
            outlined
            dense
          ></v-file-input>
        </v-row>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-btn color="success" dark @click="upload">
        Upload
        <v-icon right dark>mdi-cloud-upload</v-icon>
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
import Services from "../services/Services";
export default {
  name: "FileUploader",

  data: () => ({
    currentFile: undefined,
    progress: 0,
    message: "",

    fileInfos: [],
  }),
  methods: {
    selectFile(file) {
      this.progress = 0;
      this.currentFile = file;
    },
    
    upload() {
      if (!this.currentFile) {
        this.message = "Please select a file!";
        this.$notification.warning(this.message);
        return;
      }

      this.message = "";

      Services.upload(this.currentFile, (event) => {
        this.progress = Math.round((100 * event.loaded) / event.total);
      })
        .then((response) => {
          this.message = response.data.message;

          this.$notification.success(
            "Your file has been uploaded successfully!"
          );
          this.currentFile = undefined;
          localStorage.setItem("file_name", response.data.data);
        })
        .catch((error) => {
          this.progress = 0;
          this.message = "Could not upload the file!";
          let error_message = error.response.data.message;
          this.$notification.warning(error_message);
          this.currentFile = undefined;
        });
    },
  },
  mounted() {},
};
</script>
