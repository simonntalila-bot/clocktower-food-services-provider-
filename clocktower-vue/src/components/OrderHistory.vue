<script setup>
import { computed } from 'vue';
import { useLangStore } from '../stores/lang';
import { useCartStore } from '../stores/cart';

const props = defineProps({ show: Boolean });
const emit = defineEmits(['close']);
const lang = useLangStore();
const cart = useCartStore();

const history = computed(() => cart.loadHistory());

function fmt(n) { return 'TSh ' + n.toLocaleString('en'); }
function formatDate(d) {
  const date = new Date(d);
  return date.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) + ' ' + date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}

function handleOverlayClick(e) {
  if (e.target === e.currentTarget) emit('close');
}
</script>

<template>
  <div class="modal" :class="{ show }" @click="handleOverlayClick">
    <div class="modal-card history">
      <button class="modal-close" type="button" aria-label="Close" @click="emit('close')">&times;</button>
      <div style="padding:22px 24px 6px;text-align:center;">
        <h3 style="margin:0;font-family:'Space Grotesk',sans-serif;font-size:20px;"><span v-html="lang.$t('history.title')"></span></h3>
        <p style="color:var(--muted);font-size:13px;margin:6px 0 0;" v-html="lang.$t('history.sub')"></p>
      </div>
      <div class="history-list">
        <template v-if="history.length === 0">
          <div class="history-empty" v-html="lang.$t('history.empty')"></div>
        </template>
        <template v-else>
          <li v-for="(o, idx) in history" :key="idx">
            <div class="h-top">
              <span class="h-num">{{ o.num }}</span>
              <span class="h-total">{{ fmt(o.total) }}</span>
            </div>
            <div class="h-items">{{ o.items.join(' \u2022 ') }}</div>
            <div class="h-date">{{ formatDate(o.date) }}{{ o.name ? ' \u2022 ' + o.name : '' }}</div>
          </li>
        </template>
      </div>
    </div>
  </div>
</template>
