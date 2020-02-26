const webpack = require('webpack');
const fs = require('fs');

const config = {
    entry:  __dirname + '/index.js',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
  node: {
  	child_process: "empty",
    fs: 'empty',
    tls: 'empty',
  },
};

module.exports = config;
