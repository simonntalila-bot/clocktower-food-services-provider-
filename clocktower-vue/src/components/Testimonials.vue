<script setup>
import { useLangStore } from '../stores/lang';
import { TESTIMONIALS } from '../foods';

const lang = useLangStore();

function starHtml(r) {
  const full = Math.round(r);
  let out = '';
  for (let i = 1; i <= 5; i++) out += (i <= full) ? '\u2605' : '\u2606';
  return out + '<span class="rt">' + Number(r).toFixed(1) + '</span>';
}
</script>

<template>
  <div class="testi-grid">
    <div class="testi-card" v-for="tst in TESTIMONIALS" :key="tst.name">
      <div class="t-head">
        <span class="t-avatar"><img :src="tst.avatar" :alt="tst.name" loading="lazy"></span>
        <span>
          <span class="t-name">{{ tst.name }}</span>
          <span class="t-role">{{ lang.lang === 'sw' ? tst.roleSw : tst.role }}</span>
        </span>
      </div>
      <div class="stars" v-html="starHtml(tst.rating)"></div>
      <p>{{ lang.lang === 'sw' ? tst.textSw : tst.text }}</p>
    </div>
  </div>
</template>
