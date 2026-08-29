<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import LineIcon from './LineIcon.vue';
import logoImg from '../assets/logo.png';

const router = useRouter();

const API_BASE = '';

const username = ref('');
const password = ref('');
const showPw = ref(false);
const error = ref('');
const loading = ref(false);

async function handleSubmit() {
  if (!username.value.trim() || !password.value) {
    error.value = 'Weka username na password.';
    return;
  }
  error.value = '';
  loading.value = true;
  try {
    const res = await fetch(API_BASE + '/api/login/', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value.trim(), password: password.value }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data.ok) {
      localStorage.setItem('ct_user', JSON.stringify(data));
      window.location.href = API_BASE + '/admin-panel/';
    } else {
      error.value = data.error || 'Login imeshindikana. Jaribu tena.';
    }
  } catch (e) {
    error.value = 'Server haipatikani. Hakikisha backend inaendeshwa (localhost:8000).';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <button class="modal-close login-close" type="button" aria-label="Close" @click="router.push('/')">&times;</button>
      <div class="login-brand">
        <div class="login-logo-wrap">
          <img :src="logoImg" alt="Clocktower" class="login-logo" />
        </div>
        <span class="b2">food service provider</span>
      </div>
      <h3>Ingia kwenye Akaunti</h3>
      <p class="login-sub">Admin na Reception wanaweza kuingia hapa.</p>

      <form novalidate @submit.prevent="handleSubmit">
        <div class="field">
          <label for="lg-user">Username</label>
          <input id="lg-user" type="text" v-model="username" placeholder="mf. admin" autocomplete="username">
        </div>
        <div class="field">
          <label for="lg-pass">Password</label>
          <div class="pw-wrap">
            <input id="lg-pass" :type="showPw ? 'text' : 'password'" v-model="password" placeholder="••••••••" autocomplete="current-password">
            <button type="button" class="pw-toggle" :aria-label="showPw ? 'Hide password' : 'Show password'" @click="showPw = !showPw">
              <LineIcon :name="showPw ? 'eyeslash' : 'eye'" size="17" />
            </button>
          </div>
        </div>
        <div v-if="error" class="login-error">{{ error }}</div>
        <button class="login-btn-submit" type="submit" :disabled="loading">
          {{ loading ? 'Inaingia...' : 'Login' }}
        </button>
        <a class="forgot-link" @click.prevent="router.push('/forgot')" href="#/forgot">Umesahau password?</a>
        <p class="login-cred-hint">Default: <strong>admin</strong> / <strong>Clocktower@2026</strong></p>
      </form>
    </div>
  </div>
</template>
