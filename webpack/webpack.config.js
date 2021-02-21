var webpack = require('webpack');
module.exports = {
    entry: {
        base: ['../static/js/src/http.js', '../static/js/stickUp.min.js', '../static/js/src/base.js'],
        index: ['../static/js/src/index.js'],
        detail: ['../static/js/editormd.js', '../static/js/src/article.js'],
        know: ['../static/js/editormd.js', '../static/js/src/know.js'],
        list: ['../static/js/src/list.js']

    },
    output: {
        path: '../static/js/dist/',
        filename: '[name].js'
    },
    //module: {
    //    loaders: [{
    //        test: /\.js$/,
    //        exclude: /node_modules/,
    //        loader: 'babel',
    //        query: {
    //            presets: ['es2015', 'stage-0', 'react']
    //        }
    //    }]
    //},
    plugins: [
        new webpack.optimize.UglifyJsPlugin({
            output: {
                comments: false
            },
            compress: {
                warnings: true
            }
        }),
    ]
}
