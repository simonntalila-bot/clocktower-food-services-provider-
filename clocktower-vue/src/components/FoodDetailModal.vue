<script setup>
import { ref, watch } from 'vue';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const props = defineProps({ show: Boolean, food: Object });
const emit = defineEmits(['close', 'add-to-cart']);
const lang = useLangStore();
const menu = useMenuStore();
const qty = ref(1);
const imgFailed = ref(false);

watch(() => props.food, () => { qty.value = 1; imgFailed.value = false; });

function starHtml(r) {
  const full = Math.round(r);
  let out = '';
  for (let i = 1; i <= 5; i++) out += (i <= full) ? '★' : '☆';
  return out + '<span class="rt">' + Number(r).toFixed(1) + '</span>';
}

function handleAdd() {
  if (props.food) {
    emit('add-to-cart', props.food.id, qty.value);
    emit('close');
  }
}
</script>

<template>
  <div class="modal" :class="{ show: show }" @click.self="emit('close')">
    <div class="modal-card" v-if="food">
      <button class="modal-close" type="button" aria-label="Close" @click="emit('close')">&times;</button>
      <div class="detail-img">
        <template v-if="food.img && !imgFailed">
          <img :src="food.img" :alt="lang.$foodName(food)" @error="imgFailed = true" />
        </template>
        <template v-else>
          <span class="fc-emoji" style="font-size:64px;line-height:1">{{ food.icon }}</span>
        </template>
      </div>
      <div class="detail-body">
        <div class="d-top">
          <h3>{{ lang.$foodName(food) }}</h3>
          <span class="cat-chip">{{ lang.$t('cat.' + food.category) }}</span>
        </div>
        <p class="detail-desc">{{ lang.$foodDesc(food) }}</p>
        <div class="stars" style="margin-bottom:12px;" v-html="starHtml(food.rating || 4.5)"></div>
        <div class="detail-price">TSh {{ food.price.toLocaleString('en') }}</div>
        <div class="detail-actions">
          <div class="qty">
            <button type="button" @click="qty > 1 ? qty-- : null">−</button>
            <span class="qv">{{ qty }}</span>
            <button type="button" @click="qty++">+</button>
          </div>
          <button class="add-btn" type="button" @click="handleAdd">{{ lang.$t('food.addBtn') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
