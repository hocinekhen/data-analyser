import Vue from 'vue'

import Welcome from './components/Welcome.vue'
import VueRouter from "vue-router"
import FileUploader from './components/FileUploader.vue'
import Analyzer from './components/Analyzer.vue'
import Results from './components/Results.vue'
Vue.config.productionTip = false
Vue.use(VueRouter)

const routes = [
  
  { name: 'welcome', path: '/', component: Welcome },
  { name: 'upload', path: '/upload', component: FileUploader },
  { name: 'analyzer', path: '/analyzer', component: Analyzer },
  { name: 'results', path: '/results', component: Results },
  {
    path: '*',
    redirect: '/'
  },
]
export default new VueRouter({
    mode:'history',
  routes:routes
})
