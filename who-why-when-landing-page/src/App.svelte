<script>
	import { Router, Route } from 'svelte-routing';
	import Header from './components/Header.svelte';
	import FeatureSection from './components/FeatureSection.svelte';
	import PricingSection from './components/PricingSection.svelte';
	import SnippetSection from './components/SnippetSection.svelte';
	import Footer from './components/Footer.svelte';
	import HeroSection from './components/HeroSection.svelte';
	import Login from './routes/Login.svelte';
	import Register from './routes/Register.svelte';
	import Dashboard from './routes/Dashboard.svelte';
  </script>
  
  <style>
	@import './styles/global.css';
  </style>
  
  <Router>
	<Header />
	<Route path="/">
	  <HeroSection />
	  <FeatureSection />
	  <PricingSection />
	  <SnippetSection />
	  <Footer />
	</Route>
	<Route path="/login" component={Login} />
	<Route path="/register" component={Register} />
	<Route path="/dashboard" component={Dashboard} />
  </Router>
  