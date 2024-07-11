import { writable } from 'svelte/store';

const initialView = localStorage.getItem('lastView') || 'home';
export const currentView = writable(initialView);
