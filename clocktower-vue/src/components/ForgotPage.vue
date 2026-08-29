<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import LineIcon from './LineIcon.vue';

const router = useRouter();
const API_BASE = '';

const username = ref('');
const answer = ref('');
const newPassword = ref('');
const showPw = ref(false);
const error = ref('');
const success = ref('');
const loading = ref(false);

async function handleSubmit() {
  if (!username.value.trim() || !answer.value.trim() || !newPassword.value) {
    error.value = 'Jaza username, jibu na password mpya.';
    success.value = '';
    return;
  }
  if (newPassword.value.length < 6) {
    error.value = 'Password lazima iwe na herufi 6+.';
    success.value = '';
    return;
  }
  error.value = '';
  success.value = '';
  loading.value = true;
  try {
    const res = await fetch(API_BASE + '/api/forgot/', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value.trim(),
        answer: answer.value.trim(),
        new_password: newPassword.value,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data.ok) {
      success.value = data.message || 'Password mpya imewekwa! Ingia sasa.';
      setTimeout(() => router.push('/login'), 1800);
    } else {
      error.value = data.error || 'Imeshindikana. Jaribu tena.';
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
      <div class="forgot-brand">
        <span class="forgot-title">Sahau Password?</span>
        <span class="forgot-sub">Weka username yako na ujibu swali la usalama ili upate password mpya</span>
      </div>

      <form novalidate @submit.prevent="handleSubmit">
        <div class="field">
          <label for="fg-user">Username</label>
          <input id="fg-user" type="text" v-model="username" placeholder="mf. admin" autocomplete="username">
        </div>
        <div class="field">
          <label for="fg-answer">Swali la Usalama: Jina la mkewe mwanasayansi Newton?</label>
          <input id="fg-answer" type="text" v-model="answer" placeholder="Jibu" autocomplete="off">
        </div>
        <div class="field">
          <label for="fg-pass">Password Mpya</label>
          <div class="pw-wrap">
            <input id="fg-pass" :type="showPw ? 'text' : 'password'" v-model="newPassword" placeholder="••••••••" autocomplete="new-password">
            <button type="button" class="pw-toggle" :aria-label="showPw ? 'Hide password' : 'Show password'" @click="showPw = !showPw">
              <LineIcon :name="showPw ? 'eyeslash' : 'eye'" size="17" />
            </button>
          </div>
        </div>
        <div v-if="error" class="login-error">{{ error }}</div>
        <div v-if="success" class="forgot-success">{{ success }}</div>
        <button class="login-btn-submit" type="submit" :disabled="loading">
          {{ loading ? 'Inaweka...' : 'PATA PASSWORD MPYA' }}
        </button>
        <a class="forgot-link" @click="router.push('/login')">← Rudi kwenye Login</a>
      </form>
    </div>
  </div>
</template>

<style scoped>
.forgot-brand{display:flex;flex-direction:column;gap:4px;margin-bottom:20px;}
.forgot-title{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:22px;color:#fff;}
.forgot-sub{font-size:13px;color:rgba(255,255,255,0.72);}
.forgot-success{
  background:rgba(16,185,129,0.18);color:#6ee7b7;border:1px solid rgba(16,185,129,0.45);
  border-radius:10px;padding:10px 12px;font-size:13px;margin-bottom:14px;
}
</style>
