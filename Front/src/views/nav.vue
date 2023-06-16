<template>
  <div id="frame-box">
    <div id="left-menu">
      <ul id="left-menu-ul">
        <li v-for="e in list" v-bind:key="e" :class="{ selected: menu_selected === e }" @click="menu_select(e)">
          <a>{{ e }}</a>
        </li>
      </ul>
      <img :src="image" />
    </div>
    <div id="right-main">
    </div>
  </div>
</template>

<script>
import storage from "@/utils/storage";
export default {
  name: "navs",
  data() {
    return {
      list: ["常用", "娱乐", "学习", "设计", "开发"],
      menu_selected: "",
      image: ''
    }
  },
  created() {
    // 将引擎列表设置为本地存储
    if (storage.get("image")) {
      this.image = storage.get("engines");
      console.log(this.image);
    }
    else {
      console.log("load image error");
    }
    this.menu_selected = this.list[0]
  },
  methods: {
    menu_select(val) {
      this.menu_selected = val
    },
  },

}
</script>

<style scoped></style>