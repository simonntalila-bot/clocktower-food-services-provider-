<script setup>
import { ref, watch } from 'vue';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const props = defineProps({ food: Object });
const emit = defineEmits(['add-to-cart', 'open-detail']);
const lang = useLangStore();
const menu = useMenuStore();

const justAdded = ref(false);
const imgFailed = ref(false);

watch(() => props.food.id, () => { imgFailed.value = false; });

function handleAdd() {
  emit('add-to-cart', props.food.id, 1);
  justAdded.value = true;
  setTimeout(() => { justAdded.value = false; }, 1100);
}

function handleCardClick(e) {
  if (e.target.closest('button')) return;
  emit('open-detail', props.food.id);
}
</script>

<template>
  <article
    class="food-card"
    :class="{ added: justAdded }"
    @click="handleCardClick"
  >
    <div class="fc-thumb">
      <template v-if="food.img && !imgFailed">
        <img :src="food.img" :alt="lang.$foodName(food)" loading="lazy" @error="imgFailed = true" />
      </template>
      <template v-else>
        <span class="fc-emoji">{{ food.icon }}</span>
      </template>
    </div>
    <div class="fc-info">
      <div class="fc-top">
        <h3>{{ lang.$foodName(food) }}</h3>
      </div>
      <div class="food-price">TSh {{ food.price.toLocaleString('en') }}</div>
    </div>
    <div class="food-actions">
      <button class="add-btn" :class="{ success: justAdded }" type="button" @click.stop="handleAdd">
        <svg v-if="!justAdded" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="9" cy="21" r="1.6" /><circle cx="19" cy="21" r="1.6" />
          <path d="M2.5 3h2l2.4 12.2a1.8 1.8 0 0 0 1.8 1.4h9.6a1.8 1.8 0 0 0 1.8-1.4L21.5 7H6" />
        </svg>
        <span v-else>✓</span> {{ lang.$t('food.addBtn') }}
      </button>
    </div>
  </article>
</template>
