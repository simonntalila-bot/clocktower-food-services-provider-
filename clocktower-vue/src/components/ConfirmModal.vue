<script setup>
import { useLangStore } from '../stores/lang';
const props = defineProps({ show: Boolean, orderNum: String, total: Number, customerName: String });
const emit = defineEmits(['close']);
const lang = useLangStore();
function fmt(n) { return 'TSh ' + (n || 0).toLocaleString('en'); }

function handleOverlayClick(e) {
  if (e.target === e.currentTarget) emit('close');
}
</script>

<template>
  <div class="modal" :class="{ show }" @click="handleOverlayClick">
    <div class="modal-card confirm">
      <div class="confirm-check">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none"><path d="M4 12.5l5 5L20 6.5" stroke="#34d399" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h3 v-html="lang.$t('confirm.title')"></h3>
      <p class="confirm-greet" v-if="customerName">
        {{ lang.lang === 'sw' ? 'Asante, ' + customerName + '!' : 'Thank you, ' + customerName + '!' }}
      </p>
      <p v-else class="confirm-greet">Thank you!</p>
      <p v-html="lang.$t('confirm.text')"></p>
      <div class="fast-note" v-html="lang.$t('confirm.fast')"></div>
      <div class="order-num-box">
        <div class="on-lbl" v-html="lang.$t('confirm.onum')"></div>
        <div class="on-val">{{ orderNum }}</div>
      </div>
      <div class="confirm-total"><span v-html="lang.$t('confirm.total')"></span> <span style="color:var(--accent);">{{ fmt(total) }}</span></div>
      <button class="btn btn-primary" type="button" @click="emit('close')" v-html="lang.$t('confirm.done')"></button>
    </div>
  </div>
</template>
