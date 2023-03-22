const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(App) {
    App.use(
        '/api',
        createProxyMiddleware({
            target: 'http://127.0.0.1:5049',
            changeOrigin: true,
        })
    );
};
