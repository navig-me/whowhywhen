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
	import { DASH_API_BASE_URL } from './config';
	
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

	if ('serviceWorker' in navigator && 'PushManager' in window) {
		navigator.serviceWorker.register('/service-worker.js')
		.then(swReg => {
			console.log('Service Worker is registered', swReg);
		})
		.catch(error => {
			console.error('Service Worker Error', error);
		});
	}

	async function subscribeUser() {
		const swReg = await navigator.serviceWorker.ready;
		const subscription = await swReg.pushManager.subscribe({
			userVisibleOnly: true,
			applicationServerKey: urlBase64ToUint8Array('BCaXWkZFN67uHxHaX1-o4Cwbd1k-G3o4Xo173mVuFFqwSbyKk9ywVhqn8G4LYZp7rksyx8-OafETKQA-hHaO3jY')
		});

		const response = await fetch(`${DASH_API_BASE_URL}/dashapi/subscribe-push`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${localStorage.getItem('token')}`
			},
			body: JSON.stringify(subscription)
		});

		if (!response.ok) {
			console.error('Failed to subscribe the user: ', response.statusText);
		} else {
			console.log('Successfully subscribed the user');
		}
	}

	function urlBase64ToUint8Array(base64String) {
		const padding = '='.repeat((4 - base64String.length % 4) % 4);
		const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
		const rawData = window.atob(base64);
		const outputArray = new Uint8Array(rawData.length);

		for (let i = 0; i < rawData.length; ++i) {
			outputArray[i] = rawData.charCodeAt(i);
		}
		return outputArray;
	}

	onMount(() => {
		if ('serviceWorker' in navigator && 'PushManager' in window) {
			subscribeUser();
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
	<Route path="/setup-integration" component={Integrate} />
	<Route path="/user-settings" component={UserSettings} />
	<Route path="/alerts" component={Alerts} />
	<GDPRModal />
  </Router>
  