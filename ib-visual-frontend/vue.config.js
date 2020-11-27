module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  configureWebpack: {
    devtool: 'source-map'
  },
  devServer: {
        open: true,
        host: 'localhost',
        port: 8080,
        https: false,
        proxy: {
            '/api': {
                target: 'http://localhost:5000/api/',
                ws: true,
                changOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            },
            '/extra': {
              target: 'http://localhost:5001/',
              ws: true,
              changOrigin: true,
              pathRewrite: {
                  '^/extra': ''
              }
          },
        }
    }

}