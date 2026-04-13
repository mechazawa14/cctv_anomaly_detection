<template>
  <div class="app">
    <header class="app-header">
      <h1 class="app-title">CCTV Anomaly Detection</h1>
      <div class="backend-status" :class="backendOnline ? 'online' : 'offline'">
        <span class="status-dot"></span>
        {{ backendOnline ? 'Backend Online' : 'Backend Offline' }}
      </div>
    </header>

    <nav class="tabs">
      <button
        class="tab"
        :class="{ active: activeTab === 'webcam' }"
        @click="activeTab = 'webcam'"
      >
        Webcam
      </button>
      <button
        class="tab"
        :class="{ active: activeTab === 'upload' }"
        @click="activeTab = 'upload'"
      >
        Upload Video
      </button>
    </nav>

    <main class="content">
      <WebcamCapture v-if="activeTab === 'webcam'" @result="onResult" />
      <VideoUpload v-if="activeTab === 'upload'" @result="onResult" />
      <ResultDisplay :result="result" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import WebcamCapture from './components/WebcamCapture.vue'
import VideoUpload from './components/VideoUpload.vue'
import ResultDisplay from './components/ResultDisplay.vue'

const activeTab = ref('upload')
const result = ref(null)
const backendOnline = ref(false)

function onResult(data) {
  result.value = data
}

async function checkHealth() {
  try {
    const res = await axios.get('/api/health', { timeout: 5000 })
    backendOnline.value = res.data?.status === 'ok'
  } catch {
    backendOnline.value = false
  }
}

onMounted(() => {
  checkHealth()
  setInterval(checkHealth, 15000)
})
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.backend-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}

.backend-status.online {
  color: var(--success);
  background: rgba(46, 204, 113, 0.1);
}

.backend-status.offline {
  color: var(--danger);
  background: rgba(231, 76, 60, 0.1);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.online .status-dot {
  background: var(--success);
}

.offline .status-dot {
  background: var(--danger);
}

.tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-secondary);
  padding: 4px;
  border-radius: 10px;
}

.tab {
  flex: 1;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  color: var(--text-secondary);
  background: transparent;
  transition: all 0.2s;
}

.tab:hover {
  color: var(--text-primary);
}

.tab.active {
  background: var(--accent);
  color: #fff;
}

.content {
  display: flex;
  flex-direction: column;
}
</style>
