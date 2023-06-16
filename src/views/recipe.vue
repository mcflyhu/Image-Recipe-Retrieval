<template>
    <div id="frame-box">
        <el-row :gutter="10">
            <el-col :span="6">
                <div id="left-menu">
                    <span></span>
                    <el-image id="recipe-image" :src="imageUrl" :fit="contain" />
                </div>
            </el-col>
            <el-col :span="18">
                <div id="right-main">
                    <div id="btn_switch">
                        <button class="btn_anniu" @click="switchShow(0)" :class="{ newStyle: 0 === visualShow }">配料</button>
                        <button class="btn_anniu" @click="switchShow(1)" :class="{ newStyle: 1 === visualShow }">做法</button>
                    </div>
                    <el-carousel id="recipe-carousel" height="650px" trigger="click" :autoplay="false" direction="vertical">
                        <el-carousel-item v-for="(recipe, index) in recipes" :key="index">
                            <div class="title-header font">
                                <h1 align="center" class="recipe-name extra-bold">{{ recipe.title }}</h1>
                            </div>
                            <div v-show="0 === visualShow" id="ingredients">
                                <ul class="list-unstyled font">
                                    <li class="ingredient xs-mb1 " v-for="ingredient in recipe.ingredients"
                                        :key="ingredient">
                                        {{ ingredient }}</li>
                                </ul>
                            </div>
                            <div v-show="1 === visualShow" id="instructions">
                                <ol class="steps font">
                                    <li class="xs-mb2" v-for="instruction in recipe.instructions" :key="instruction">
                                        {{ instruction }}</li>
                                </ol>
                            </div>
                        </el-carousel-item>
                    </el-carousel>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import storage from '@/utils/storage';

export default {
    name: "recipe",
    data() {
        return {
            recipes: [],
            imageUrl: '',
            visualShow: 0
        }
    },
    methods: {

        switchShow(page) {
            this.visualShow = page;
        }
    },
    created() {
        this.imageUrl = storage.get('imageUrl'); //获取上传的图片
        this.recipes = storage.get('recipes'); //获取检索结果
        console.log(this.recipes);

    }
}
</script>
  
<style lang="less" scoped>
#left-menu {
    max-height: 100%;
    height: 650px;
    width: 100%;
    line-height: 100%;
    border-right: 2px solid #a6c8d7;
    padding-right: 5px;
}

#left-menu span {
    display: inline-block;
    vertical-align: middle;
    height: 135%;
}

#recipe-image {
    max-width: 100%;
    max-height: 100%;
    height: auto;
    width: auto;

}

#right-main {
    margin-top: 5px;
}


.el-carousel__item:nth-child(2n) {
    background-color: #cee8f3;
}

.el-carousel__item:nth-child(2n + 1) {
    background-color: #f7e7f7;
}

.btn_anniu {
    width: 50%;
    padding: 5px 0;
    font-size: 20px;
    font-weight: bold;
    border: 0 solid #fff;
    color: #000;
    outline: none;
    background: #fff;
}

.newStyle {
    border-bottom: 2px solid #f0892e;
    color: #f0892e;
    font-size: 26px;
    font-weight: bold;
}

.xs-mb1 {
    margin:0 15px 25px 30px;
    font-size: 20px;
}

ol,
table,
ul {
    font-variant-numeric: tabular-nums;
    font-feature-settings: "tnum" 1, "tnum";
}

ol {
    display: block;
    list-style-type: decimal;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    padding-inline-start: 40px;
}

.xs-mb2 {
    margin-bottom: 8px;
    font-size: 17px;
    font-weight: 500;

}

ol.steps li {
    list-style: none;
    counter-increment: step-counter;
}

ol.steps li::before {
    display: inline-block;
    content: counter(step-counter);
    color: #757575;
    font-weight: 800;
    margin-left: -2rem;
    width: 33px;
}

.font {
    font-family: "Proxima Nova";
}

.title-header {
    margin: 10px 0 15px 0;

}

.extra-bold {
    font-weight: 1000;
}
</style>