<template>
  <div id="menu" :class="{ on: is_on }" @click="menu_client()"><i></i></div>
  <!--<div :class="{closed:!is_on}" class="list">
    <ul id="setting">
      <li :class="{selected:menu_selected==='bookmark'}" @click="menu_select('bookmark')"><a>书签</a></li>
      <li :class="{selected:menu_selected==='setting'}" @click="menu_select('setting')"><a>设置</a></li>
    </ul>
    <ul id="element">
      <span v-if="menu_selected==='bookmark'">
        <Bookmarks></Bookmarks>
      </span>
      <span v-else-if="menu_selected==='setting'">
        <Setting></Setting>
      </span>
    </ul>
  </div>
-->
  <div id="content" ref="content" @click="menu_close()">
    <div id="top-menu-list">
      <ul id="top-menu-ul">
        <li :class="{ selected: this.$route.path === '/' }">
          <router-link to="/">首页</router-link>
        </li>
        <li :class="{ selected: this.$route.path === '/recipe2im' }">
          <router-link to="/recipe2im">菜谱搜图</router-link>
        </li>
      </ul>
    </div>
    <router-view></router-view>
    <!--    <Background @background="set_background"></Background>-->
    <div id="message"></div>
    <div id="foot">©2023 HU QIANYUE. All rights reserved.
      <!--      <a href="https://github.com/zzd/Simple-Search-Page" style="font-size: 12px;" target="_blank">-->
      <!--        <span class="tag_box">v{{ version }} Vue 测试版</span></a>-->

      <span class="tag_box">菜谱检索系统（beta）</span>
    </div>
  </div>
</template>
<script>
import packageJson from '../package.json'
// import storage from "@/utils/storage";
// import axios from "axios";


export default {
  name: "Home",
  data() {
    return {
      version: packageJson.version,
      is_on: false,
      menu_selected: "bookmark",
      background: "",
    }
  },
  methods: {
    menu_client() {
      this.is_on = !this.is_on
    },
    menu_close() {
      this.is_on = false
    },
    menu_select(val) {
      this.menu_selected = val
    },
    set_background(data) {
      this.background = data;
    },
  },
  watch: {
    background() {
      try {
        this.$refs.content.style.background = this.background
      } catch (error) {
        console.log(error);
      }
    }
  },
  mounted() {
    this.$refs.content.style.background = this.background
  }
};
</script>

<style lang='less'>
@import "style/main";
</style>