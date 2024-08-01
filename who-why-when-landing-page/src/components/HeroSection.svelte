<script>
	import { navigate } from 'svelte-routing';

	function changeView(view) {
		navigate(view);
	}
</script>

<section class="hero-section">
	<div class="container">
		<h1><span class="supercharge">Supercharge</span> Your APIs, Protect Your Data</h1>
		<p>Get real-time analytics, track bots and AI scrapers, and optimize your resources with our comprehensive API management platform.</p>
		<button class="btn-primary" on:click={() => changeView('/register')}>START FOR FREE</button>
	</div>
</section>

<style>
	.hero-section {
		background: url('/supercharge.jpg') no-repeat center center/cover;
		color: #fff;
		padding: 180px 20px;
		text-align: center;
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
	}

	.container {
		max-width: 800px;
		text-align: center;
	}

	h1 {
		font-size: 3rem;
		margin: 0 0 20px;
	}

	p {
		font-size: 1.2rem;
		margin: 0 0 30px;
	}

	.btn-primary {
		background-color: #ff4000;
		color: #fff;
		padding: 15px 30px;
		border: none;
		border-radius: 30px;
		text-transform: uppercase;
		font-size: 1rem;
		cursor: pointer;
	}

	.supercharge {
		background: linear-gradient(90deg, #ff4000, #ff7300, #ffd700, #73ff00, #00ffd0, #0073ff, #ff00d0);
		background-size: 600%;
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		animation: gradient 5s ease infinite;
	}

	@media (max-width: 768px) {
		h1 {
			font-size: 2.5rem;
		}

		p {
			font-size: 1rem;
		}

		.btn-primary {
			padding: 10px 20px;
		}
	}

	@media (max-width: 480px) {
		h1 {
			font-size: 2rem;
		}

		p {
			font-size: 0.9rem;
		}

		.btn-primary {
			padding: 10px 20px;
			font-size: 0.8rem;
		}
	}
</style>
