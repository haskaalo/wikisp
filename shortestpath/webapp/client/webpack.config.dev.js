const { merge } = require('webpack-merge');
const common = require('./webpack.config.common.js');
const { DefinePlugin } = require('webpack');

module.exports = merge(common, {
    devtool: 'source-map',
    mode: 'development',
    output: {
        publicPath: "/",
    },
    module: {
        rules: [
            {enforce: 'pre', test: /\.js$/, loader: 'source-map-loader'},
        ],
    }
});