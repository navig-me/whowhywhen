<script>
	let features = [
		{
			title: "Track Bots and AI Scrapers",
			description: "Know which bots and AI scrapers are accessing your data and how to block them.",
			icon: "fas fa-robot"
		},
		{
			title: "Performance Monitoring",
			description: "Ensure they are meeting your performance SLAs.",
			icon: "fas fa-tachometer-alt"
		},
		{
			title: "Real-time API Analytics",
			description: "Optimize your services by knowing how your APIs are being used.",
			icon: "fas fa-chart-line"
		},
		{
			title: "Understand Your Users",
			description: "Gain insights into your users' behavior and preferences.",
			icon: "fas fa-user-friends"
		}
	];
</script>

<section class="feature-section">
	<div class="container">
		<h2>Powerful Features</h2>
		<p>Built by developers, for developers.</p>
		<div class="features-grid">
			{#each features as feature}
				<div class="feature-item">
					<i class="{feature.icon}"></i>
					<h3>{feature.title}</h3>
					<p>{feature.description}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<style>
	.feature-section {
		padding: 80px 20px;
		/* background-color: #f9f9f9; Light gray background for separation */
		color: #333;
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
		text-align: center;
		padding: 0 20px;
	}

	h2 {
		font-size: 2.5rem;
		color: #663399;
		margin-bottom: 20px;
		position: relative;
	}

	h2::after {
		content: '';
		display: block;
		width: 50px;
		height: 4px;
		background: #663399;
		margin: 10px auto;
	}

	p {
		font-size: 1.2rem;
		margin-bottom: 40px;
	}

	.features-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 20px;
	}

	.feature-item {
		background: #fff; /* White background for feature items */
		padding: 20px;
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		text-align: center;
	}

	.feature-item i {
		font-size: 2rem;
		margin-bottom: 10px;
		color: #663399;
	}

	.feature-item h3 {
		font-size: 1.5rem;
		margin: 0;
		color: #333;
	}

	.feature-item p {
		font-size: 1rem;
		color: #555;
		margin: 10px 0 0;
	}

	@media (max-width: 768px) {
		h2 {
			font-size: 2rem;
		}

		p {
			font-size: 1rem;
		}

		.feature-item {
			padding: 15px;
		}

		.feature-item i {
			font-size: 1.5rem;
		}

		.feature-item h3 {
			font-size: 1.2rem;
		}

		.feature-item p {
			font-size: 0.9rem;
		}
	}

	@media (max-width: 480px) {
		h2 {
			font-size: 1.8rem;
		}

		p {
			font-size: 0.9rem;
		}

		.feature-item {
			padding: 10px;
		}

		.feature-item i {
			font-size: 1.2rem;
		}

		.feature-item h3 {
			font-size: 1rem;
		}

		.feature-item p {
			font-size: 0.8rem;
		}
	}
</style>
