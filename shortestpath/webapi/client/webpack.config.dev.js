const { merge } = require('webpack-merge');
const common = require('./webpack.config.common.js');

const {DefinePlugin} = require('webpack');

const buildconfig = {
    apiUrl: process.env.APIURL || "/api",
    isDev: true,
}

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
    },
    plugins: [
        new DefinePlugin({
            BUILDCONFIG: JSON.stringify(buildconfig),
        })
    ]
});