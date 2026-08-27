<script setup>
import { useMenuStore } from './stores/menu';
import { useRouter } from 'vue-router';
import NavBar from './components/NavBar.vue';

const router = useRouter();
const menu = useMenuStore();

function handleSetFilter(cat) {
  menu.setFilter(cat);
  router.push('/');
  setTimeout(() => {
    document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' });
  }, 100);
}
</script>

<template>
  <NavBar
    @set-filter="handleSetFilter"
  />

  <router-view />
</template>
