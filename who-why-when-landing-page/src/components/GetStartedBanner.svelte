<script>
	import { navigate } from 'svelte-routing';

	function changeView(view) {
		navigate(view);
	}
</script>

<section class="banner-section">
	<div class="container">
		<h2>Get Started Now!</h2>
		<p>Integrate your site now and unlock detailed insights with our state-of-the-art analytics platform.</p>
		<button class="btn-primary" on:click={() => changeView('/register')}>Integrate Now</button>
	</div>
</section>

<style>
	.banner-section {
		padding: 60px 20px;
		background: linear-gradient(to right, #663399, #ff4000);
		color: #fff;
		text-align: center;
	}

	h2 {
		font-size: 2.5rem;
		margin-bottom: 20px;
	}

	p {
		font-size: 1.2rem;
		margin-bottom: 40px;
	}

	.btn-primary {
		background-color: #fff;
		color: #663399;
		padding: 15px 30px;
		border: none;
		border-radius: 30px;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.btn-primary:hover {
		background-color: #e6e6e6;
		transform: scale(1.05);
	}

	@media (max-width: 768px) {
		h2 {
			font-size: 2rem;
		}
	}

	@media (max-width: 480px) {
		h2 {
			font-size: 1.8rem;
		}
	}
</style>
