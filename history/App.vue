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
      </div>{{ item.percent }}%
      <button class="btn btn-danger mt-3" @click="Delete(item.obid, item.file_name)">删除</button>
    </div>
    <div class="alert alert-success" v-show="showDelete">
      <strong>{{ book_name }} 删除成功!</strong>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const historyList = ref([]);
let showDelete = ref(false);
let book_name = ref('');

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
      } catch (error) {
        console.error('Failed to fetch progress:', error);
      }
    }
  }, 800); // 0.8秒钟轮询一次
};

onMounted(() => {
  fetchHistory(); // 页面加载后开始获取历史数据
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
</style>
