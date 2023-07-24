const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { DefinePlugin } = require('webpack');

module.exports = {
    entry: {
        main: './src/index.tsx',
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'js/[name].[fullhash].js',
        publicPath: '/static'
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.json', '.css', '.scss'],
        alias: {
            'assets': path.resolve(__dirname, 'src/assets/'),
            'variables': path.resolve(__dirname, 'src/styles/variables.scss'),
            '@home': path.resolve('./src')
        },
    },
    module: {
        rules: [
            { test: /\.ts(x?)$/, loader: "ts-loader" },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                    },
                    "css-loader", "sass-loader"
                ]
            },
            {
                test: /\.(svg)$/,
                type: 'asset/resource',
                generator: {
                    filename: 'svg/[name].[hash].[ext]'
                }
            },
            {
                test: /\.ttf/,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name].[hash].[ext]'
                }
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            chunks: ["main"],
            template: path.join(__dirname, "src/html/index.html"),
            filename: "html/index.html",
        }),
        new MiniCssExtractPlugin({
            filename: "css/styles.[fullhash].css",
            chunkFilename: "css/[id].[chunkhash].css",
        }),
        new DefinePlugin({
            BUILDCONFIG: JSON.stringify({
                isDev: false,
                apiURL: process.env.API_URL === undefined ? "/api" : process.env.API_URL,
                recaptchaSiteKey: process.env.RECAPTCHA_SITEKEY
            })
        })
    ]
};