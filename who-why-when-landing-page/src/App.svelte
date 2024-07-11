<script>
	import { currentView } from './stores/viewStore';
	import { onMount } from 'svelte';
	import LoginComponent from './routes/LoginComponent.svelte';
	import RegisterComponent from './routes/RegisterComponent.svelte';
	import Header from './components/Header.svelte';
	import FeatureSection from './components/FeatureSection.svelte';
	import PricingSection from './components/PricingSection.svelte';
	import SnippetSection from './components/SnippetSection.svelte';
	import Footer from './components/Footer.svelte';
	import HeroSection from './components/HeroSection.svelte';
	import Dashboard from './routes/Dashboard.svelte';
	import Projects from './routes/Projects.svelte';
	import UserSettings from './routes/UserSettings.svelte';
	import { isLoggedIn } from './stores/userStore';
  
	let view;
  
	// Subscribe to the currentView store and store the current view in localStorage
	$: view, currentView.subscribe(value => {
	  view = value;
	  localStorage.setItem('lastView', value);
	});
  
	onMount(() => {
	  const token = localStorage.getItem('token');
	  if (token) {
		isLoggedIn.set(true);
		const lastView = localStorage.getItem('lastView');
		if (lastView) {
		  currentView.set(lastView);
		} else {
		  currentView.set('dashboard');
		}
	  } else {
		isLoggedIn.set(false);
		currentView.set('home');
	  }
	});
  </script>
  
  <style>
	@import './styles/global.css';
  </style>
  
  <Header />
  
  {#if view === 'home'}
	<HeroSection />
	<FeatureSection />
	<PricingSection />
	<SnippetSection />
	<Footer />
  {:else if view === 'login'}
	<LoginComponent />
  {:else if view === 'register'}
	<RegisterComponent />
  {:else if view === 'dashboard'}
	<Dashboard />
  {:else if view === 'projects'}
	<Projects />
  {:else if view === 'user-settings'}
	<UserSettings />
  {/if}
  