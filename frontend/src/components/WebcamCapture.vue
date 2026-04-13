<template>
  <div class="webcam-section card">
    <div class="video-container">
      <video ref="videoEl" autoplay playsinline muted class="webcam-video"></video>
      <canvas ref="canvasEl" style="display: none"></canvas>
      <div v-if="!streamActive" class="webcam-placeholder" @click="startWebcam">
        <div class="cam-icon">&#9673;</div>
        <p>Click to start camera</p>
      </div>
      <div v-if="isDetecting" class="detecting-badge">
        <span class="pulse"></span> Detecting
      </div>
      <div v-if="isDetecting" class="frame-counter">
        {{ frameBuffer.length }}/20 frames
      </div>
    </div>

    <div class="controls">
      <button v-if="!streamActive" class="btn btn-primary" @click="startWebcam">
        Start Camera
      </button>
      <template v-else>
        <button
          v-if="!isDetecting"
          class="btn btn-primary"
          @click="startDetection"
        >
          Start Detection
        </button>
        <button
          v-else
          class="btn btn-danger"
          @click="stopDetection"
        >
          Stop Detection
        </button>
        <button class="btn" style="background: var(--bg-secondary); color: var(--text-primary)" @click="stopWebcam">
          Stop Camera
        </button>
      </template>

      <div v-if="isPredicting" class="predicting-indicator">
        <div class="spinner"></div>
        <span>Running inference...</span>
      </div>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import axios from 'axios'

const emit = defineEmits(['result'])

const videoEl = ref(null)
const canvasEl = ref(null)
const streamActive = ref(false)
const isDetecting = ref(false)
const isPredicting = ref(false)
const error = ref(null)
const frameBuffer = ref([])

let stream = null
let captureIntervalId = null
let predictIntervalId = null

async function startWebcam() {
  error.value = null
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480, facingMode: 'environment' },
    })
    videoEl.value.srcObject = stream
    streamActive.value = true
  } catch (err) {
    error.value = 'Camera access denied or not available. Please allow camera permissions.'
  }
}

function stopWebcam() {
  stopDetection()
  if (stream) {
    stream.getTracks().forEach((t) => t.stop())
    stream = null
  }
  if (videoEl.value) videoEl.value.srcObject = null
  streamActive.value = false
}

function captureFrame() {
  const video = videoEl.value
  const canvas = canvasEl.value
  if (!video || !canvas || video.readyState < 2) return

  const ctx = canvas.getContext('2d')
  canvas.width = 320
  canvas.height = 240
  ctx.drawImage(video, 0, 0, 320, 240)

  const b64 = canvas.toDataURL('image/jpeg', 0.7)
  frameBuffer.value.push(b64)
  if (frameBuffer.value.length > 20) {
    frameBuffer.value.shift()
  }
}

async function sendPrediction() {
  if (isPredicting.value || frameBuffer.value.length < 5) return

  isPredicting.value = true
  try {
    const res = await axios.post('/api/predict/frames', {
      frames: [...frameBuffer.value],
    }, { timeout: 60000 })
    emit('result', res.data)
  } catch (err) {
    console.error('Prediction failed:', err)
  } finally {
    isPredicting.value = false
  }
}

function startDetection() {
  frameBuffer.value = []
  isDetecting.value = true
  captureIntervalId = setInterval(captureFrame, 500)
  predictIntervalId = setInterval(sendPrediction, 5000)
}

function stopDetection() {
  isDetecting.value = false
  clearInterval(captureIntervalId)
  clearInterval(predictIntervalId)
  captureIntervalId = null
  predictIntervalId = null
}

onBeforeUnmount(() => {
  stopWebcam()
})
</script>

<style scoped>
.webcam-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.video-container {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background: #000;
  aspect-ratio: 4 / 3;
}

.webcam-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.webcam-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  cursor: pointer;
  transition: background 0.2s;
}

.webcam-placeholder:hover {
  background: var(--bg-card);
}

.cam-icon {
  font-size: 48px;
  color: var(--accent);
  margin-bottom: 8px;
}

.webcam-placeholder p {
  color: var(--text-secondary);
  font-size: 14px;
}

.detecting-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(231, 76, 60, 0.9);
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.pulse {
  width: 8px;
  height: 8px;
  background: #fff;
  border-radius: 50%;
  animation: pulse-anim 1.2s infinite;
}

@keyframes pulse-anim {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.frame-counter {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.controls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.predicting-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13px;
  margin-left: auto;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border);
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
