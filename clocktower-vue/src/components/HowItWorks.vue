<script setup>
import { useLangStore } from '../stores/lang';
const lang = useLangStore();
const emit = defineEmits(['scroll-to-menu']);

const steps = [
  { num: 'STEP 1', ico: '🍽️', titleKey: 'about.st1', descKey: 'about.s1' },
  { num: 'STEP 2', ico: '🛒', titleKey: 'about.st2', descKey: 'about.s2' },
  { num: 'STEP 3', ico: '✅', titleKey: 'about.st3', descKey: 'about.s3' }
];
</script>

<template>
  <section class="section" id="about">
    <div class="section-head">
      <span class="dot"></span>
      <span>{{ lang.$t('sec.about') }}</span>
      <span class="line"></span>
    </div>
    <h2 v-html="lang.$t('about.title')"></h2>
    <p class="sub">{{ lang.$t('about.sub') }}</p>
    <div class="about-grid">
      <div v-for="step in steps" :key="step.num" class="step-card">
        <span class="step-num">{{ step.num }}</span>
        <span class="step-ico">{{ step.ico }}</span>
        <h3>{{ lang.$t(step.titleKey) }}</h3>
        <p>{{ lang.$t(step.descKey) }}</p>
      </div>
    </div>
    <div class="about-cta">
      <button class="add-btn" type="button" @click="emit('scroll-to-menu')">{{ lang.$t('about.cta') }}</button>
      <p class="about-tag">{{ lang.$t('about.tag') }}</p>
    </div>
  </section>
</template>
