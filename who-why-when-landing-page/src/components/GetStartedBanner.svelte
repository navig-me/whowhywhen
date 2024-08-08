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
		padding: 100px 20px;
		background: linear-gradient(135deg, #663399, #ff4000);
		color: #fff;
		text-align: center;
		border-radius: 15px;
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
		position: relative;
		overflow: hidden;
	}

	.container {
		position: relative;
		z-index: 1;
	}

	h2 {
		font-size: 2.5rem;
		margin-bottom: 20px;
		letter-spacing: 1px;
		text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
	}

	p {
		font-size: 1.2rem;
		margin-bottom: 30px;
		letter-spacing: 0.5px;
		text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
	}

	.btn-primary {
		background-color: #fff;
		color: #663399;
		padding: 15px 30px;
		border: none;
		border-radius: 30px;
		font-size: 1.2rem;
		cursor: pointer;
		transition: background-color 0.3s ease, transform 0.3s ease;
		box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
	}

	.btn-primary:hover {
		background-color: #f2f2f2;
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
			font-size: 2rem;
		}

		p {
			font-size: 1rem;
		}

		.btn-primary {
			padding: 12px 25px;
			font-size: 1rem;
		}

		.developers-row {
			height: 80px;
		}
	}

	@media (max-width: 480px) {
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
			height: 60px;
		}
	}
</style>
