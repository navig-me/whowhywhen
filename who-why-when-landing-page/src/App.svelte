<script>
	import { currentView } from './stores/viewStore';
	import { onMount } from 'svelte';
	import Header from './components/Header.svelte';
	import FeatureSection from './components/FeatureSection.svelte';
	import PricingSection from './components/PricingSection.svelte';
	import SnippetSection from './components/SnippetSection.svelte';
	import Footer from './components/Footer.svelte';
	import HeroSection from './components/HeroSection.svelte';
	import Login from './routes/Login.svelte';
	import Register from './routes/Register.svelte';
	import Dashboard from './routes/Dashboard.svelte';
  
	let view;
  
	// Subscribe to the currentView store
	$: view, currentView.subscribe(value => view = value);
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
	<Login />
  {:else if view === 'register'}
	<Register />
  {:else if view === 'dashboard'}
	<Dashboard />
  {/if}
  