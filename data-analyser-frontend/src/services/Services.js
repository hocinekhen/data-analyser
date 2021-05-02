import http from "../http-common";

const FILE_NOT_FOUND_MSG = "No file found, please Upload a file first!"
class Services {

  upload(file, onUploadProgress) {
    let formData = new FormData();

    formData.append("file", file);

    return http.post("api/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      onUploadProgress
    });
  }

  getAllColumns(vueinstance) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.get("/api/columns/" + file_name);
  }

  get_side_effect_columns(vueinstance, columns) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/columns/side_effect/" + file_name,
      { columns: columns });
  }
  get_cells_columns(vueinstance, columns) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/columns/cells/" + file_name,
      { columns: columns });
  }

  getMatrix(vueinstance, file_name = "") {
    if (!file_name)
      file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.get("/api/matrix/" + file_name);
  }

  merge_columns(vueinstance, columns_to_merge, merged_column_name, is_in_body, matrix) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/columns/merge/" + file_name,
      {
        columns_to_merge: columns_to_merge,
        column_name: merged_column_name,
        is_in_body, matrix
      });
  }

  group_columns(vueinstance, column_to_group, is_in_body, matrix) {
    console.log(column_to_group)
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/columns/group/" + file_name, {
      columns_to_group: column_to_group,
      is_in_body: is_in_body,
      matrix: matrix
    });
  }
  
  filter_by_column(vueinstance, columns_to_filter,
    min, max, is_in_body, matrix) {
    console.log(columns_to_filter)
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/columns/filter/" + file_name, {
      column_to_filter: columns_to_filter[0],
      is_in_body: is_in_body,
      min: parseInt(min),
      max: parseInt(max),
      matrix: matrix
    });
  }

  get_series(vueinstance, column_x, column_y, column_values, is_in_body, matrix) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/matrix/series/" + file_name, {
      column_x: column_x,
      column_y: column_y,
      column_values: column_values,
      is_in_body: is_in_body,
      matrix: matrix
    });
  }

  calculateCorrelation(vueinstance, columns, is_in_body, matrix) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/matrix/correlation/" + file_name,
      { columns: columns, is_in_body, matrix });
  }

  calculateRegression(vueinstance, columns, is_in_body, matrix) {
    let file_name = localStorage.getItem('file_name')
    if (!file_name) {
      vueinstance.$notification.warning(FILE_NOT_FOUND_MSG)
      return
    }
    return http.post("/api/matrix/regression/" + file_name,
      { columns: columns, is_in_body, matrix });
  }

}

export default new Services();
