<template>
  <div class="title">
    <h1 class="display-4">下载任务</h1>
  </div>
  <div class="centered-div">
    <div v-for="item in historyList.history" :key="item.obid" class="history-item">
      <h2>{{ item.file_name }}</h2>
      <div class="progress">
        <div class="progress-bar" :style="{ width: `${item.percent}%` }">
        </div>
      </div>
      <div class="progress-div">
        {{ item.percent }}%
        <a
            v-if="item.percent === 100"
            :href="download_link + item.file_name"
            class="btn btn-primary"
        >
          下载
        </a>
        <button v-else class="btn btn-secondary" disabled>
          下载
        </button>
        <button class="btn btn-danger mt-3" @click="Delete(item.obid, item.file_name)">删除</button>
      </div>
    </div>
    <div class="alert alert-success" v-show="showDelete">
      <strong>{{ book_name }} 删除成功!</strong>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import axios from 'axios';

const historyList = ref([]);
let showDelete = ref(false);
let book_name = ref('');
let download_link = ref('');

document.title = '番茄小说下载器 | 下载任务';

const Delete = async (obid, book_name) => {
  showDelete.value = false;
  try {
    const response = await axios.get(`/api/down/del/${obid}/`);
    showDelete.value = true;
    location.reload();
  } catch (error) {
    console.error('Failed to fetch history data:', error);
  }
}

const fetchHistory = async () => {
  try {
    const response = await axios.get('/api/history/');
    historyList.value = response.data;
    console.log(response.data)
    console.log(typeof response.data)
    pollProgress(); // 开始轮询进度
  } catch (error) {
    console.error('Failed to fetch history data:', error);
  }
};

const pollProgress = () => {
  const interval = setInterval(async () => {
    for (const item of historyList.value.history) {
      if(item.percent === 100) continue;
      try {
        const response = await axios.get(`/api/history/${item.obid}/`)
        item.percent = response.data.percent;
        console.log(item.percent)
      } catch (error) {
        console.error('Failed to fetch progress:', error);
      }
    }
  }, 800); // 0.8秒钟轮询一次
};

const fetchDownloadUrl = async () => {
  try {
    const response = await axios.get('/api/get_download_url/');
    console.log(response.data)
    download_link.value = response.data["download_url"];
  } catch (error) {
    console.error('Failed to fetch history data:', error);
  }
};

// const fetchDownloadUrl = () => {
//   axios.get('/api/get_download_url')
//       .then(response => {
//         // 从JSON响应中提取URL值
//          this.downloadUrl = response.data.url;
//       })
//       .catch(error => {
//         console.error('获取下载链接失败', error);
//       });
//   return this.downloadUrl
// }

onMounted(() => {
  fetchHistory(); // 页面加载后开始获取历史数据
  fetchDownloadUrl()
  // console.log(download_link);
  // console.log(typeof  download_link);
  // console.log(download_link.PromiseResult);
});
</script>

<style scoped>
.centered-div {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 从上往下渲染 */
  margin-top: 5%;
}

.title {
  text-align: center;
  justify-content: center;
  margin-top: 10%;
  height: 20%;
}

.title h1 {
  margin: 0;
}

.history-item {
  text-align: center;
  background-color: #f0f0f0;
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
  width: 60%; /* 默认情况下，在电脑网页上使用居中60%的区域 */
}

.progress {
  height: 20px;
  text-align: left;
  background-color: #e0e0e0;
  border-radius: 5px;
  margin-top: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  line-height: 20px;
  text-align: left;
  background-color: #007bff;
  color: white;
  transition: width 0.3s ease-in-out;
}

.progress-div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
