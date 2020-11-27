import Vue from 'vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import HighchartsMore from 'highcharts/highcharts-more'
import exportingInit from 'highcharts/modules/exporting'
// import drilldownInit from 'highcharts/modules/drilldown'
import treemapInit from 'highcharts/modules/treemap'
import offlineExportingInit from 'highcharts/modules/offline-exporting'
import HighchartsVue from 'highcharts-vue'

Highcharts.setOptions({
    global: {
        timezoneOffset: -8 * 60,
    }
})
stockInit(Highcharts)
exportingInit(Highcharts)
// drilldownInit(Highcharts)
treemapInit(Highcharts)
offlineExportingInit(Highcharts)
HighchartsMore(Highcharts)
Vue.use(HighchartsVue)