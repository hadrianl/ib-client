import Vue from 'vue'
import Highcharts from 'highcharts'
import HighchartsMore from 'highcharts/highcharts-more'
import exportingInit from 'highcharts/modules/exporting'
import offlineExportingInit from 'highcharts/modules/offline-exporting'
import HighchartsVue from 'highcharts-vue'

exportingInit(Highcharts)
offlineExportingInit(Highcharts)
HighchartsMore(Highcharts)
Vue.use(HighchartsVue)