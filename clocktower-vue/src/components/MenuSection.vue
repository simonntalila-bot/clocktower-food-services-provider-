<script setup>
import FoodCard from './FoodCard.vue';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const lang = useLangStore();
const menu = useMenuStore();

const emit = defineEmits(['open-food', 'add-to-cart']);

const filters = ['all', 'breakfast', 'lunch', 'dinner', 'drinks'];
</script>

<template>
  <section class="section" id="menu">

    <div class="toolbar">
      <div class="search-box">
        <svg class="sico" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <circle cx="11" cy="11" r="7" />
          <path d="M21 21l-4.3-4.3" />
        </svg>
        <input
          type="text"
          :value="menu.searchTerm"
          @input="menu.searchTerm = $event.target.value"
          :placeholder="lang.$t('menu.search')"
        />
      </div>
      <div class="filters">
        <button
          v-for="cat in filters"
          :key="cat"
          class="filter-btn"
          :class="{ active: menu.currentCat === cat }"
          type="button"
          @click="menu.setFilter(cat)"
        >
          {{ cat === 'all' ? lang.$t('f.all') : lang.$t('cat.' + cat) }}
        </button>
      </div>
    </div>
    <div class="food-grid">
      <FoodCard
        v-for="food in menu.filteredFoods()"
        :key="food.id"
        :food="food"
        @open-detail="emit('open-food', $event)"
        @add-to-cart="(id, qty) => emit('add-to-cart', id, qty)"
      />
    </div>
  </section>
</template>
