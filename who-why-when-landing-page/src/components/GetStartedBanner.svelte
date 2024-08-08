<script>
	import { navigate } from 'svelte-routing';

	function changeView(view) {
		navigate(view);
	}
</script>

<section class="banner-section">
	<div class="container">
		<h2>Ready to Elevate Your APIs?</h2>
		<p>Seamlessly integrate our analytics platform and gain unparalleled insights today.</p>
		<button class="btn-primary" on:click={() => changeView('/register')}>Get Started</button>
	</div>
	<div class="developers-row"></div>
</section>

<style>
	.banner-section {
		padding: 120px 20px;
		background: linear-gradient(135deg, #663399, #ff4000);
		color: #fff;
		text-align: center;
		border-radius: 10px;
		box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
		position: relative;
	}

	h2 {
		font-size: 2rem;
		margin-bottom: 10px;
	}

	p {
		font-size: 1rem;
		margin-bottom: 20px;
	}

	.btn-primary {
		background-color: #fff;
		color: #663399;
		padding: 12px 25px;
		border: none;
		border-radius: 25px;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.3s ease, transform 0.3s ease;
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
	}

	.btn-primary:hover {
		background-color: #e6e6e6;
		transform: scale(1.05);
	}

	.developers-row {
		background: url('/developers.png') repeat-x;
		height: 80px;
		width: 100%;
		position: absolute;
		bottom: 0;
		left: 0;
		background-size: contain;
	}

	@media (max-width: 768px) {
		h2 {
			font-size: 1.8rem;
		}

		p {
			font-size: 0.9rem;
		}

		.btn-primary {
			padding: 10px 20px;
			font-size: 0.9rem;
		}

		.developers-row {
			height: 80px;
		}
	}

	@media (max-width: 480px) {
		h2 {
			font-size: 1.6rem;
		}

		p {
			font-size: 0.8rem;
		}

		.btn-primary {
			padding: 8px 18px;
			font-size: 0.8rem;
		}

		.developers-row {
			height: 60px;
		}
	}
</style>
