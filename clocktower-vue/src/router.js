import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import LoginPage from './components/LoginPage.vue';
import ForgotPage from './components/ForgotPage.vue';
import AdminActivity from './components/AdminActivity.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/forgot', component: ForgotPage },
  { path: '/admin-panel/activity', component: AdminActivity, meta: { admin: true } },
];

export default createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});
