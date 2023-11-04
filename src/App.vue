<script setup>
import { ref } from 'vue';
import axios from 'axios';

const showApp = ref(true);
let showSuccess = ref(false);
let showWarning = ref(false);
const downloadOption = ref('single');
const singleFileInput = ref('');
const bulkFileInput = ref('');
const formatOption = ref('epub'); // 初始化为txt，您可以根据需要设置其他默认值

let urls = [];

const startDownload = async () => {
  showSuccess.value = false;
  showWarning.value = false;

  if (downloadOption.value === 'single') {
    console.log('Downloading single file:', singleFileInput.value);
    // 检查单文件下载的URL
    if (isValidURL(singleFileInput.value) && singleFileInput.value.includes('/page/')) {
      console.log('Downloading single file:', singleFileInput.value);
      showSuccess.value = true; // 显示成功提示框
      await sendPostRequest([singleFileInput.value], formatOption.value);
    } else {
      showWarning.value = true; // 显示警告提示框
    }
  } else if (downloadOption.value === 'bulk') {
    urls = bulkFileInput.value.split('\n');
    console.log('Downloading multiple files:', urls);
    const isValidBulk = urls.every(url => isValidURL(url) && url.includes('/page/'));
    if (isValidBulk) {
      console.log('Downloading multiple files:', urls);
      showSuccess.value = true; // 显示成功提示框
      await sendPostRequest(urls, formatOption.value);
    } else {
      showWarning.value = true; // 显示警告提示框
    }
  }
};

function isValidURL(url) {
  // 使用正则表达式检查URL是否有效
  const urlPattern = /^https?:\/\/.+/;
  return urlPattern.test(url);
}

async function sendPostRequest(urls, format) {
  try {
    const response = await axios.post('/api/down/', { urls, format });
    console.log('POST request successful:', response.data);
  } catch (error) {
    console.error('POST request failed:', error);
  }
}
</script>

<template>
  <div class="container d-flex justify-content-center align-items-center centered-div" v-if="showApp">
    <div class="text-center">
      <h1 class="display-4">番茄小说下载器</h1>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="downloadType" id="singleDownload" value="single" v-model="downloadOption">
        <label class="form-check-label" for="singleDownload">单文件下载</label>
      </div>

      <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="downloadType" id="bulkDownload" value="bulk" v-model="downloadOption">
        <label class="form-check-label" for="bulkDownload">批量下载</label>
      </div>

      <div class="mt-3">
        <label for="formatOption">文件格式：</label>
        <select class="form-control" id="formatOption" v-model="formatOption">
          <option value="txt">TXT(普通文档)</option>
          <option value="epub">EPUB(电子书)</option>
        </select>
      </div>

      <div v-if="downloadOption === 'single'" class="mt-3 url-box">
        <label for="urlInput">URL：</label>
        <input type="text" class="form-control" id="urlInput" v-model="singleFileInput" placeholder="输入URL">
      </div>

      <div v-if="downloadOption === 'bulk'" class="mt-3 url-box">
        <label for="bulkUrlInput">URL（每行一个）：</label>
        <textarea class="form-control" id="bulkUrlInput" rows="5" v-model="bulkFileInput" placeholder="输入多个URL，每行一个"></textarea>
      </div>

      <button class="btn btn-primary mt-3" @click="startDownload">提交</button>
      <br /><br />
      <div class="alert alert-success" v-show="showSuccess">
        <strong>成功!</strong> 加入下载列表！
      </div>
      <div class="alert alert-warning" v-show="showWarning">
        <strong>警告!</strong> 请输入正确的目录链接！
      </div>
    </div>
    <button class="btn btn-primary mt-3"><a href="/history" style="text-decoration:none;color:inherit;">下载任务</a></button>
  </div>
</template>

<style scoped>
.centered-div {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 10%;
  width: 60%; /* 默认情况下，在电脑网页上使用居中60%的区域 */
}

.url-box {
  width: 100%;
}

/* Media query for screens smaller than 768px (mobile screens) */
@media (max-width: 767px) {
  .centered-div {
    width: 100%; /* 在手机网页上使用居中100%的区域 */
  }
}
</style>
