<script>
	import { Router, Route } from 'svelte-routing';
	import Home from './routes/Home.svelte';
	import LoginComponent from './routes/LoginComponent.svelte';
	import RegisterComponent from './routes/RegisterComponent.svelte';
	import Header from './components/Header.svelte';
	import Footer from './components/Footer.svelte';
	import Dashboard from './routes/Dashboard.svelte';
	import Bots from './routes/Bots.svelte';
	import Projects from './routes/Projects.svelte';
	import Integrate from './routes/Integrate.svelte';
	import Alerts from './routes/Alerts.svelte';
	import UserSettings from './routes/UserSettings.svelte';
	import GDPRModal from './components/GDPRModal.svelte';
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
	<Route path="/bots" component={Bots} />
	<Route path="/projects" component={Projects} />
	<Route path="/integrate" component={Integrate} />
	<Route path="/user-settings" component={UserSettings} />
	<Route path="/alerts" component={Alerts} />
	<GDPRModal />
  </Router>
  