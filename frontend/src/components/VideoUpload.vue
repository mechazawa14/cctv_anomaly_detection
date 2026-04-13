<template>
  <div class="upload-section card">
    <div
      class="drop-zone"
      :class="{ 'drag-over': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave="isDragging = false"
      @drop.prevent="handleDrop"
      @click="fileInput?.click()"
    >
      <div class="drop-icon">&#9654;</div>
      <p class="drop-text">Drop a video file here or click to browse</p>
      <p class="drop-hint">Supports MP4, AVI, MOV, MKV</p>
      <input
        ref="fileInput"
        type="file"
        accept="video/*"
        hidden
        @change="handleFileSelect"
      />
    </div>

    <div v-if="videoUrl" class="preview">
      <video :src="videoUrl" controls class="preview-video"></video>
      <div class="preview-actions">
        <span class="file-name">{{ fileName }}</span>
        <button class="btn btn-primary" :disabled="loading" @click="analyze">
          {{ loading ? 'Analyzing...' : 'Analyze Video' }}
        </button>
        <button class="btn btn-danger" @click="clearFile">Clear</button>
      </div>
    </div>

    <div v-if="loading" class="loader">
      <div class="spinner"></div>
      <p>Extracting frames and running inference...</p>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['result'])

const fileInput = ref(null)
const videoFile = ref(null)
const videoUrl = ref(null)
const fileName = ref('')
const loading = ref(false)
const error = ref(null)
const isDragging = ref(false)

function setFile(file) {
  if (!file || !file.type.startsWith('video/')) {
    error.value = 'Please select a valid video file.'
    return
  }
  videoFile.value = file
  videoUrl.value = URL.createObjectURL(file)
  fileName.value = file.name
  error.value = null
}

function handleFileSelect(e) {
  setFile(e.target.files[0])
}

function handleDrop(e) {
  isDragging.value = false
  setFile(e.dataTransfer.files[0])
}

function clearFile() {
  if (videoUrl.value) URL.revokeObjectURL(videoUrl.value)
  videoFile.value = null
  videoUrl.value = null
  fileName.value = ''
  error.value = null
}

async function analyze() {
  if (!videoFile.value) return
  loading.value = true
  error.value = null

  const formData = new FormData()
  formData.append('video', videoFile.value)

  try {
    const res = await axios.post('/api/predict/video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    })
    emit('result', res.data)
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to analyze video. Is the backend running?'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.drop-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: var(--accent);
  background: rgba(108, 99, 255, 0.05);
}

.drop-icon {
  font-size: 40px;
  color: var(--accent);
  margin-bottom: 12px;
}

.drop-text {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.drop-hint {
  font-size: 13px;
  color: var(--text-secondary);
}

.preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-video {
  width: 100%;
  max-height: 360px;
  border-radius: 8px;
  background: #000;
}

.preview-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-name {
  flex: 1;
  font-size: 13px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.loader {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 14px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-msg {
  color: var(--danger);
  font-size: 14px;
  padding: 8px 12px;
  background: rgba(231, 76, 60, 0.1);
  border-radius: 8px;
}
</style>
