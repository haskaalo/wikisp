const { merge } = require('webpack-merge');
const common = require('./webpack.config.common');
const {DefinePlugin} = require('webpack');
const TerserPlugin = require("terser-webpack-plugin"); // Uglify
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const buildconfig = {
    apiUrl: process.env.APIURL || "/api",
    isDev: false,
};

module.exports = merge(common, {
    mode: 'production',
    output: {
        publicPath: `/`
    },
    optimization: {
        minimize: true,
        minimizer: [
            new TerserPlugin(),
            new CssMinimizerPlugin()
        ]
    },
    plugins: [
        new DefinePlugin({
            BUILDCONFIG: JSON.stringify(buildconfig)
        }),
    ]
});