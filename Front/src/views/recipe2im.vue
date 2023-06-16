<template>
    <div id="frame-box">

        <div id="form-drawer">
            <el-drawer v-model="drawer" title="菜谱" :direction="ltr" :before-close="handleClose" size="33%">
                <el-form :model="recipeForm" label-width="120px">
                    <el-form-item label="菜谱名称">
                        <el-input v-model="recipeForm.title" placeholder="请输入菜品名称" clearable></el-input>
                    </el-form-item>

                    <el-form-item label="配料描述">
                        <el-input v-model="recipeForm.ingredients" type="textarea" :autosize="{ minRows: 3, maxRows: 8 }"
                            placeholder="请给出制作该菜品所需的配料表"></el-input>
                        <el-button class="btn_clear" type="danger" circle @click="clearIngredients()"><el-icon>
                                <Delete />
                            </el-icon></el-button>
                    </el-form-item>
                    <el-form-item label="制作步骤">
                        <el-input v-model="recipeForm.instructions" type="textarea" :autosize="{ minRows: 5, maxRows: 10 }"
                            placeholder="请描述菜品的制作步骤"></el-input>
                        <el-button class="btn_clear" type="danger" circle @click="clearInstructions()"><el-icon>
                                <Delete />
                            </el-icon></el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button id="submit-button" type="primary" color="#626aef" @click="uploadRecipe()">
                            <el-icon>
                                <Search />
                            </el-icon>
                            搜索
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-drawer>
        </div>
        <div class="input-recipe">
            <el-button class="btn_recipe" type="primary" @click="drawer = true" color="#79dcf1">输入菜谱<el-icon>
                    <EditPen />
                </el-icon></el-button>
        </div>
        <el-divider>
            <el-icon>
                <ArrowDownBold />
            </el-icon>
        </el-divider>
        <el-row align="middle" justify="center">
            <div id="image-carousel">
                <el-col :span="24">
                    <el-carousel :interval="4000" type="card" height="450px">
                        <el-carousel-item v-for="(imageUrl, index) in  imageUrls " :key="index">
                            <el-image style="width: auto; height: 400px" id="img-recipe"
                                :src="'data:image/jpeg;base64,' + imageUrl" :fit="cover" />
                        </el-carousel-item>
                    </el-carousel>
                </el-col>
            </div>
        </el-row>
    </div>
</template>
  
<script>
import axios from "axios";
import storage from "@/utils/storage";

export default {
    name: "recipe2im",
    data() {
        return {
            uploadUrl: "/api/recipe",
            recipeForm: {
                title: "",
                ingredients: "",
                instructions: ""
            },
            imageUrls: [],
            drawer: false
        };
    },
    created() {
        this.recipeForm.title=" ";
        this.recipeForm.ingredients=" ";
        this.recipeForm.instructions=" ";
    },
    methods: {
        handleSuccess(response) {
            console.log("上传成功", response);
            //获取响应体图片的url序列
            this.imageUrls = response
            for (var i = 0; i < this.imageUrls.length; i++) {

                console.log(this.imageUrls[i]);
            }
            this.drawer = false;
        },
        handleError(error) {
            console.log("上传失败", error);
        },

        async uploadRecipe() {
            // 执行上传菜谱表单操作
            let formData = new FormData();
            for (let key in this.recipeForm) {
                formData.append(key, this.recipeForm[key]);
                console.log(formData.get(key));
            }

            console.log("正在上传菜谱")

            try {
                const response = await axios.post(this.uploadUrl, formData);

                this.handleSuccess(response.data);
            } catch (error) {
                this.handleError(error);
            }
        },
        clearIngredients() {
            this.recipeForm.ingredients = '';
        },
        clearInstructions() {
            this.recipeForm.instructions = '';
        },
        handleClose(done) {
            this.$confirm("确定要退出菜谱信息填写吗？").then(() => { this.drawer = false; done() }).catch(() => { });
        }

    }
}

</script>
<style lang="less" scoped>
.el-row {
    margin-top: 30px;
    height: 300px;
}

#submit-button {
    text-align: center;
    width: 150px;
    height: 50px;
    margin-top: 10px;
}

#image-carousel {
    width: 80%;
}

#img-recipe {
    height: auto;
    width: 100%
}

.input-recipe {
    text-align: center;
    height: 150px;
    padding-top: 50px;
}

.btn_recipe {
    color: #ffffff;
    font-size: 250%;
    font-family: YouYuan;
    font-weight: 700;
    height: 75px;
    width: 300px;
}

.btn_clear {
    margin-top: 5px;
}
</style>
