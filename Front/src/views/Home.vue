<template>
  <div id="logo"><img alt="简洁导航" src="../assets/img/simple-so.svg"></div>

  <div id="site-main">
    <div id="container">
      <div id="upload">
        <!--<input id="search-keyword" ref="search_input" v-model="keyword" :name=engines[search_engine][1]
                   :placeholder=engines[search_engine][2]
                   autocomplete=off autofocus class="float-left" type=search
                   @blur="blur()" @focus="focus()" @input="get_hot_keyword()" @keydown.down="down()"
                   @keydown.prevent.up="up()">
            <input id="search-form-submit" class="float-right" type="submit" value="搜索">-->
        <el-upload id="upload-image" ref="upload" :action="uploadUrl" :before-upload="beforeUpload"
          :on-success="handleSuccess" :on-error="handleError" :on-change="handleChange" :limit="1" name="image">
          <el-button id="upload-button" type="primary" color="#8B40FC">点击上传菜品图片
          </el-button>
        </el-upload>

      </div>
    </div>
  </div>
</template>

<script>

import storage from "@/utils/storage";



export default {
  name: "Home",
  data() {
    return {
      uploadUrl: "/api/image",
      uploadheaders: {
        Authorization: "Bearer token_goes_here", 'Content-Type': 'multipart/form-data'
      },
      file: null,
    };
  },

  methods: {
    beforeUpload(file) {
      // 校验图片大小、格式等信息
      const isJPG = file.type === 'image/jpeg';
      const isLT2M = file.size / 1024 / 1024 < 2;
      if (!isJPG) {
        this.$message.error('只能上传 JPG 格式的图片');
        return false;
      }
      if(!isLT2M){
        this.$message.error('上传图片大小不能超过2M');
        return false;
      }
      this.file = file;
      //this.fileUrl = URL.createObjectURL(file.raw);
      return isJPG; // 阻止自动上传
    },
    handleSuccess(response) {
      console.log("上传成功", response);
      //存储POST请求的响应体，即检索的菜谱结果
      storage.set('recipes', response);

      //上传成功后，转入下一个界面
      this.$router.push('/recipe');
    },
    handleError(error) {
      console.log("上传失败", error);
    },


    handleChange(file) {
      let url = URL.createObjectURL(file.raw);
      storage.set('imageUrl', url);
      console.log(url, "handlechange的输出");
    },


  }
}
  ;
</script>
<style lang="less">
@import "../style/search";
</style>
