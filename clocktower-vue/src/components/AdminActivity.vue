<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE } from '../api.js';

const logs = ref([]);
const loading = ref(false);
const error = ref('');
const authed = ref(false);
const me = ref(null);

const username = ref('');
const password = ref('');
const showPw = ref(false);
const loginLoading = ref(false);
const loginError = ref('');

async function checkMe() {
  try {
    const r = await fetch(`${API_BASE}/api/me/`, { credentials: 'include' });
    if (r.ok) {
      const d = await r.json();
      authed.value = true;
      me.value = d;
      await loadLogs();
    } else {
      authed.value = false;
    }
  } catch (e) {
    authed.value = false;
  }
}

async function doLogin() {
  loginError.value = '';
  if (!username.value.trim() || !password.value) {
    loginError.value = 'Jaza username na password.';
    return;
  }
  loginLoading.value = true;
  try {
    const r = await fetch(`${API_BASE}/api/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username: username.value.trim(), password: password.value }),
    });
    const d = await r.json();
    if (d.ok) {
      authed.value = true;
      me.value = d;
      password.value = '';
      await loadLogs();
    } else {
      loginError.value = d.error || 'Username au password si sahihi.';
    }
  } catch (e) {
    loginError.value = 'Imeshindwa kuungana na server.';
  } finally {
    loginLoading.value = false;
  }
}

async function loadLogs() {
  loading.value = true;
  error.value = '';
  try {
    const r = await fetch(`${API_BASE}/api/activity-logs/`, { credentials: 'include' });
    if (r.ok) {
      const d = await r.json();
      logs.value = d.logs || [];
    } else if (r.status === 403) {
      error.value = 'Huna ruhusa ya kuona activity logs.';
      logs.value = [];
    } else {
      const d = await r.json().catch(() => ({}));
      error.value = d.error || 'Imeshindwa kupakia logs.';
      logs.value = [];
    }
  } catch (e) {
    error.value = 'Imeshindwa kuungana na server.';
    logs.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(checkMe);
</script>

<template>
  <div class="act-page">
    <div class="act-top">
      <h1 class="act-title">Activity Logs</h1>
      <p class="act-sub">Nani alilogi-in, kitendo gani, na lini — kwenye admin.</p>
    </div>

    <div v-if="!authed" class="act-login">
      <h2>Ingia kama Admin</h2>
      <p class="hint">Weka username na password ya admin ili kuona activity logs.</p>
      <form novalidate @submit.prevent="doLogin">
        <label>Username</label>
        <input v-model="username" type="text" placeholder="mf. admin" autocomplete="username">
        <label>Password</label>
        <div class="pw-wrap">
          <input v-model="password" :type="showPw ? 'text' : 'password'" placeholder="Password" autocomplete="current-password">
          <button type="button" class="pw-eye" @click="showPw = !showPw">{{ showPw ? 'Gusa' : 'Onesha' }}</button>
        </div>
        <button class="act-btn" type="submit" :disabled="loginLoading">
          {{ loginLoading ? 'Inaingia...' : 'INGIA' }}
        </button>
        <p v-if="loginError" class="err">{{ loginError }}</p>
      </form>
    </div>

    <div v-else>
      <div class="act-me" v-if="me">
        <span class="me-name">{{ me.name || me.username }}</span>
        <span class="me-role">({{ me.role }})</span>
      </div>

      <div v-if="loading" class="act-msg">Inapakia logs...</div>
      <div v-else-if="error" class="act-err">{{ error }}</div>
      <div v-else-if="logs.length === 0" class="act-msg">Hakuna activity logs bado.</div>
      <ul v-else class="act-list">
        <li v-for="log in logs" :key="log.id" class="act-item">
          <div class="act-head">
            <span class="act-user">{{ log.user }}</span>
            <span class="act-when">{{ log.time }}</span>
          </div>
          <div class="act-action">{{ log.action }}</div>
          <div v-if="log.detail" class="act-detail">{{ log.detail }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.act-page {
  max-width: 760px;
  margin: 0 auto;
  padding: 90px 18px 60px;
  font-family: 'Space Grotesk', sans-serif;
  color: #1f2937;
}
.act-top { margin-bottom: 22px; }
.act-title { font-size: 28px; margin: 0 0 4px; color: #0A9A4A; }
.act-sub { margin: 0; color: #6b7280; font-size: 14px; }

.act-login {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}
.act-login h2 { margin: 0 0 6px; color: #111827; }
.act-login .hint { margin: 0 0 16px; color: #6b7280; font-size: 13px; }
.act-login label { display: block; font-size: 13px; color: #374151; margin: 10px 0 4px; }
.act-login input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
}
.pw-wrap { position: relative; }
.pw-wrap input { padding-right: 68px; }
.pw-eye {
  position: absolute;
  right: 6px; top: 50%;
  transform: translateY(-50%);
  border: none; background: #f3f4f6;
  padding: 6px 10px; border-radius: 6px;
  font-size: 12px; cursor: pointer; color: #374151;
}
.act-btn {
  margin-top: 16px;
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: #0A9A4A;
  color: #fff;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
}
.act-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.err { color: #dc2626; font-size: 13px; margin-top: 10px; }

.act-me { margin-bottom: 14px; font-size: 15px; }
.me-name { font-weight: 700; color: #0A9A4A; }
.me-role { color: #6b7280; }

.act-msg { color: #6b7280; padding: 30px; text-align: center; font-size: 14px; }
.act-err { color: #dc2626; padding: 20px; text-align: center; font-size: 14px; }

.act-list { list-style: none; margin: 0; padding: 0; }
.act-item {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.act-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.act-user { font-weight: 700; color: #0A9A4A; font-size: 14px; }
.act-when { color: #9ca3af; font-size: 12px; }
.act-action { font-size: 15px; color: #111827; font-weight: 600; }
.act-detail { font-size: 13px; color: #6b7280; margin-top: 3px; }
</style>
