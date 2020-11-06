import Vue from 'vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import HighchartsMore from 'highcharts/highcharts-more'
import exportingInit from 'highcharts/modules/exporting'
import drilldownInit from 'highcharts/modules/drilldown'
import treemapInit from 'highcharts/modules/treemap'
import offlineExportingInit from 'highcharts/modules/offline-exporting'
import HighchartsVue from 'highcharts-vue'

stockInit(Highcharts)
exportingInit(Highcharts)
drilldownInit(Highcharts)
treemapInit(Highcharts)
offlineExportingInit(Highcharts)
HighchartsMore(Highcharts)
Vue.use(HighchartsVue)