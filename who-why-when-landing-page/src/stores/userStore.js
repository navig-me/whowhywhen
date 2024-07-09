import { writable } from 'svelte/store';

const storedToken = localStorage.getItem('token');
export const isLoggedIn = writable(!!storedToken);
export const selectedProjectIdStore = writable(null); // New store for selected project ID

export function setToken(token) {
  localStorage.setItem('token', token);
  isLoggedIn.set(true);
}

export function clearToken() {
  localStorage.removeItem('token');
  isLoggedIn.set(false);
}
