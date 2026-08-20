<script setup>
import { useLangStore } from '../stores/lang';
import { useMenuStore } from '../stores/menu';
import { CATEGORY_META } from '../foods';

const lang = useLangStore();
const menu = useMenuStore();
const emit = defineEmits(['set-filter']);

const cats = ['breakfast', 'lunch', 'dinner', 'drinks'];
</script>

<template>
  <section class="section" id="services">
    <div class="section-head">
      <span class="dot"></span>
      <span>{{ lang.$t('sec.services') }}</span>
      <span class="line"></span>
    </div>
    <h2 v-html="lang.$t('services.title')"></h2>
    <p class="sub">{{ lang.$t('services.sub') }}</p>
    <div class="cats">
      <a v-for="cat in cats" :key="cat" class="cat-card" href="#menu" @click.prevent="emit('set-filter', cat)">
        <span class="cnt-badge">{{ menu.catCount(cat) }} {{ lang.$t('cats.items') }}</span>
        <div class="cat-thumb">
          <img :src="CATEGORY_META[cat].img" :alt="lang.$t('cat.' + cat)">
        </div>
        <h3>{{ lang.$t('cat.' + cat) }}</h3>
        <p>{{ CATEGORY_META[cat].tag[lang.lang] || CATEGORY_META[cat].tag.en }}</p>
        <span class="view">{{ lang.$t('cats.view') }} <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
      </a>
    </div>
  </section>
</template>
