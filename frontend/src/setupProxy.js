const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(App) {
    App.use(
        '/api',
        createProxyMiddleware({
            target: 'https://f4b3-82-132-217-127.eu.ngrok.io/',
            changeOrigin: true,
        })
    );
};