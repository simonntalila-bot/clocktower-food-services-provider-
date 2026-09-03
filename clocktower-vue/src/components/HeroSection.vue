<script setup>
import { useLangStore } from '../stores/lang';
import LineIcon from './LineIcon.vue';

const lang = useLangStore();
const emit = defineEmits(['scroll-to-menu', 'open-cart']);
</script>

<template>
  <section class="hero" id="home">
    <div class="hero-bg"></div>
    <div class="hero-overlay"></div>
    <img src="/welcome.png" class="hero-welcome-img" alt="Welcome" />

    <div class="hero-content">
      <span class="badge">
        <LineIcon name="clocktower" size="14" color="#F57C00" />
        {{ lang.$t('hero.badge') }}
      </span>
      <h1>{{ lang.$t('hero.title') }}</h1>
      <p class="hero-sub">{{ lang.$t('hero.sub') }}</p>
      <div class="hero-actions">
        <button class="btn btn-primary" type="button" @click="emit('scroll-to-menu')">
          {{ lang.$t('cats.view') }} <LineIcon name="arrowright" size="14" color="#ffffff" style="vertical-align:-2px" />
        </button>
        <button class="btn btn-ghost" type="button" @click="emit('open-cart')">
          ORDER NOW <LineIcon name="cart" size="14" color="#ffffff" style="vertical-align:-2px" />
        </button>
      </div>
    </div>
  </section>
</template>