/*
 * Copyright (c) 2021. ZHANGDI Studio All Rights Reserved.
 */
module.exports={
    publicPath:'/',
    lintOnSave:false,
    devServer: {
        open:true,
        // 使用代理解决跨域问题
        proxy: {
            '/api': {
                target: 'http://192.168.20.100:8030/',
                changeOrigin: true,
                pathRewrite: {
                    "^/api": ''
                }
            }
        },
    }

};
