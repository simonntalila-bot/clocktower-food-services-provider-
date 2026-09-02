<script setup>
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';
import heroFood from '../assets/hero-food.png';

const lang = useLangStore();
</script>

<template>
  <section class="hero" id="home">
    <div class="hero-bg">
      <img :src="heroFood" alt="ClockTower delicious food" loading="eager" />
    </div>
    <div class="hero-overlay"></div>

    <div class="hero-content">
      <span class="badge">
        <LineIcon name="clocktower" size="14" color="#F57C00" />
        {{ lang.$t('hero.badge') }}
      </span>
      <h1>{{ lang.$t('hero.title') }}</h1>
      <p class="hero-sub">{{ lang.$t('hero.sub') }}</p>
    </div>
  </section>
</template>