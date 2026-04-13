<template>
  <div v-if="result" class="result-display card">
    <div class="result-header">
      <div class="result-label" :class="labelClass">
        <span class="label-icon">{{ result.label === 'Anomaly' ? '!' : '' }}</span>
        {{ result.label }}
      </div>
      <span class="result-confidence">{{ (result.confidence * 100).toFixed(1) }}%</span>
    </div>

    <div class="scores">
      <div class="score-row">
        <span class="score-label">Normal</span>
        <div class="score-bar">
          <div class="score-fill normal" :style="{ width: (result.normal_score * 100) + '%' }"></div>
        </div>
        <span class="score-value">{{ (result.normal_score * 100).toFixed(1) }}%</span>
      </div>
      <div class="score-row">
        <span class="score-label">Anomaly</span>
        <div class="score-bar">
          <div class="score-fill anomaly" :style="{ width: (result.anomaly_score * 100) + '%' }"></div>
        </div>
        <span class="score-value">{{ (result.anomaly_score * 100).toFixed(1) }}%</span>
      </div>
    </div>

    <div class="result-time">{{ timestamp }}</div>
  </div>

  <div v-else class="result-placeholder card">
    <p>No results yet. Upload a video or start webcam detection.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: Object,
})

const labelClass = computed(() => ({
  'label-normal': props.result?.label === 'Normal',
  'label-anomaly': props.result?.label === 'Anomaly',
}))

const timestamp = computed(() => {
  return new Date().toLocaleTimeString()
})
</script>

<style scoped>
.result-display {
  margin-top: 20px;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.result-label {
  font-size: 28px;
  font-weight: 700;
  padding: 8px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 18px;
  font-weight: 900;
}

.label-normal {
  color: var(--success);
  background: rgba(46, 204, 113, 0.1);
}

.label-normal .label-icon {
  background: var(--success);
  color: #fff;
}

.label-anomaly {
  color: var(--danger);
  background: rgba(231, 76, 60, 0.1);
}

.label-anomaly .label-icon {
  background: var(--danger);
  color: #fff;
}

.result-confidence {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-secondary);
}

.scores {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.score-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.score-label {
  width: 70px;
  font-size: 13px;
  color: var(--text-secondary);
}

.score-bar {
  flex: 1;
  height: 10px;
  background: var(--bg-primary);
  border-radius: 5px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.score-fill.normal {
  background: var(--success);
}

.score-fill.anomaly {
  background: var(--danger);
}

.score-value {
  width: 55px;
  text-align: right;
  font-size: 13px;
  font-weight: 600;
}

.result-time {
  margin-top: 16px;
  font-size: 12px;
  color: var(--text-secondary);
  text-align: right;
}

.result-placeholder {
  margin-top: 20px;
  text-align: center;
  color: var(--text-secondary);
  padding: 40px;
}
</style>
