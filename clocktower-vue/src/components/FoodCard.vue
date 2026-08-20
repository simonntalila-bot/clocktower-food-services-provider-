<script setup>
import { ref } from 'vue';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const props = defineProps({ food: Object });
const emit = defineEmits(['add-to-cart', 'open-detail']);
const lang = useLangStore();
const menu = useMenuStore();

const qty = ref(1);
const justAdded = ref(false);

function handleAdd() {
  emit('add-to-cart', props.food.id, qty.value);
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
      <template v-if="food.img">
        <img :src="food.img" :alt="lang.$foodName(food)" loading="lazy" />
      </template>
      <template v-else>
        <span class="fc-emoji">{{ food.icon }}</span>
      </template>
    </div>
    <div class="fc-top">
      <span class="fc-dot"></span>
      <h3>{{ lang.$foodName(food) }}</h3>
    </div>
    <div class="food-price">TSh {{ food.price.toLocaleString('en') }}</div>
    <div class="food-actions">
      <div class="qty">
        <button type="button" @click.stop="qty > 1 ? qty-- : null">−</button>
        <span class="qv">{{ qty }}</span>
        <button type="button" @click.stop="qty++">+</button>
      </div>
      <button class="add-btn" :class="{ success: justAdded }" type="button" @click.stop="handleAdd">
        {{ justAdded ? '✓ ' + lang.$t('food.addBtn') : lang.$t('food.addBtn') }}
      </button>
    </div>
  </article>
</template>
