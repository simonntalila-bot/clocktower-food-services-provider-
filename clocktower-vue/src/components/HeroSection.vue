<script setup>
import { useLangStore } from '../stores/lang';
const lang = useLangStore();
const emit = defineEmits(['scroll-to-menu', 'open-cart']);
</script>

<template>
  <section class="hero" id="home">
    <div class="hero-bg">
      <img src="https://simonntalila-bot.github.io/clocktower-food-services-provider-/1.jpg" alt="ClockTower Food Service Provider Restaurant" loading="eager">
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-glow"></div>
    <div class="hero-content">
      <span class="badge">{{ lang.$t('hero.badge') }}</span>
      <h1 v-html="lang.$t('hero.title')"></h1>
      <p class="lede">{{ lang.$t('hero.lede') }}</p>
      <div class="hero-btns">
        <button class="btn btn-primary" type="button" @click="emit('scroll-to-menu')">{{ lang.$t('hero.explore') }}</button>
        <button class="btn btn-ghost" type="button" @click="emit('open-cart')">{{ lang.$t('hero.viewcart') }}</button>
      </div>
      <div class="hero-feats">
        <span>🌿 <span>{{ lang.$t('feat.fresh') }}</span></span>
        <span>⚡ <span>{{ lang.$t('feat.fast') }}</span></span>
        <span>✓ <span>{{ lang.$t('feat.hyg') }}</span></span>
        <span>♥ <span>{{ lang.$t('feat.love') }}</span></span>
      </div>
    </div>
  </section>
</template>
