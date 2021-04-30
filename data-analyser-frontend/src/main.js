import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueNotification from "@kugatsu/vuenotification";
import router from "./router"
Vue.config.productionTip = false


Vue.use(VueNotification, {
  timer: 3,
  position:'bottomRight',
  
});
new Vue({
  
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
