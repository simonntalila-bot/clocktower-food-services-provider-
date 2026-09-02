<script setup>
import FoodCard from './FoodCard.vue';
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';

const lang = useLangStore();
const menu = useMenuStore();

const emit = defineEmits(['open-food', 'add-to-cart']);

const filters = ['all', 'breakfast', 'visinia', 'drinks', 'lunch', 'dinner'];

const filterColors = {
  all: '#087f5b',
  breakfast: '#e5484d',
  visinia: '#a78bfa',
  drinks: '#0a9a4a',
  lunch: '#ff7a45',
  dinner: '#2563eb',
};
</script>

<template>
  <section class="section" id="menu">

    <div class="toolbar">
      <div class="menu-tagline">
        <h2 class="mt-title" v-html="lang.$t('menu.restaurant')"></h2>
        <p class="mt-sub" v-html="lang.$t('menu.tagline')"></p>
      </div>
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
        <button
          v-if="menu.searchTerm"
          class="search-clear"
          type="button"
          aria-label="Clear search"
          @click="menu.searchTerm = ''"
        >×</button>
      </div>
      <div class="filters">
        <button
          v-for="cat in filters"
          :key="cat"
          class="filter-btn"
          :class="{ active: menu.currentCat === cat }"
          :style="{ '--fc': filterColors[cat] }"
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
