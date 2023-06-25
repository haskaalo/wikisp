const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: {
        main: './src/index.tsx',
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'static/js/[name].[hash].js',
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
                test: /\.(png|jpg|gif)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            outputPath: "static/img",
                        }
                    }
                ]
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
            filename: "static/css/styles.[hash].css",
            chunkFilename: "static/css/[id].[chunkhash].css",
        }),
    ]
};