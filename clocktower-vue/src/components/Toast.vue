<script setup>
import { ref } from 'vue';

const toasts = ref([]);

function showToast(msg, icon = '✓') {
  const id = Date.now();
  toasts.value.push({ id, msg, icon });
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id);
  }, 2800);
}

defineExpose({ showToast });
</script>

<template>
  <div class="toasts">
    <div v-for="toast in toasts" :key="toast.id" class="toast show">
      <span class="tick">{{ toast.icon }}</span> {{ toast.msg }}
    </div>
  </div>
</template>
