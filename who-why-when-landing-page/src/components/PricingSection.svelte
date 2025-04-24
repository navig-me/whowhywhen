<script>
	import { navigate } from 'svelte-routing';

	function changeView(view) {
		navigate(view);
	}
</script>

<section class="pricing-section">
	<div class="container">
		<h2>Open Source Analytics</h2>
		<p>Free and open source analytics for your applications. Contributions welcome!</p>
		<div class="plans">
			<div class="plan">
				<h3>FREE</h3>
				<p><i class="fas fa-check"></i> Unlimited API calls</p>
				<p><i class="fas fa-check"></i> All Analytics</p>
				<p><i class="fas fa-check"></i> In-App Alerts</p>
				<p><i class="fas fa-check"></i> Email Alerts</p>
				<p><i class="fas fa-check"></i> Self-hosted and fully customizable</p>
				<p class="price">$0</p>
				<button class="btn-primary" on:click={() => changeView('/register')}>Get Started</button>
			</div>
		</div>
	</div>
</section>

<style>
	.pricing-section {
		padding: 40px 20px;
		background: #e0e0e0;
		text-align: center;
		color: #333;
	}

	h2 {
		font-size: 2.5rem;
		margin-bottom: 10px;
		color: #663399;
	}

	p {
		font-size: 1.2rem;
		margin-bottom: 40px;
	}

	.plans {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 40px;
	}

	.plan {
		background: #fff;
		padding: 30px;
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		text-align: center;
		width: 100%;
		max-width: 300px;
	}

	.plan.best-value {
		border: 2px solid #ff4000;
	}

	h3 {
		font-size: 1.8rem;
		color: #663399;
	}

	.plan p {
		font-size: 1rem;
		color: #555;
		margin-bottom: 15px;
	}

	.price {
		font-size: 2rem;
		color: #333;
		font-weight: bold;
		margin: 20px 0;
	}

	.btn-primary {
		background-color: #ff4000;
		color: #fff;
		padding: 10px 20px;
		border: none;
		border-radius: 30px;
		font-size: 1rem;
		cursor: pointer;
		margin-top: 20px;
	}

	.btn-primary:hover {
		background-color: #e63900;
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
