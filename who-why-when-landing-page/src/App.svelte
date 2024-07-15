<script>
	import { Router, Route, Link } from 'svelte-routing';
	import Home from './routes/Home.svelte';
	import LoginComponent from './routes/LoginComponent.svelte';
	import RegisterComponent from './routes/RegisterComponent.svelte';
	import Header from './components/Header.svelte';
	import Footer from './components/Footer.svelte';
	import Dashboard from './routes/Dashboard.svelte';
	import Projects from './routes/Projects.svelte';
	import UserSettings from './routes/UserSettings.svelte';
	import UptimeMonitor from './routes/UptimeMonitor.svelte';
	import { isLoggedIn } from './stores/userStore';
	import { onMount } from 'svelte';

	let loggedIn = false;

	onMount(() => {
		const token = localStorage.getItem('token');
		if (token) {
			isLoggedIn.set(true);
			loggedIn = true;
		} else {
			isLoggedIn.set(false);
			loggedIn = false;
		}
	});
</script>

<style>
	@import './styles/global.css';
</style>

<Router>
	<Header />
	<Route path="/" component={Home} />
	<Route path="/login" component={LoginComponent} />
	<Route path="/register" component={RegisterComponent} />
	<Route path="/dashboard" component={Dashboard} />
	<Route path="/projects" component={Projects} />
	<Route path="/user-settings" component={UserSettings} />
	<Route path="/uptime-monitors" component={UptimeMonitor} />
	{#if !loggedIn}
		<Footer />
	{/if}
</Router>
