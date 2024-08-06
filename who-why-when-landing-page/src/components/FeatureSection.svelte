<script>
	let features = [
		{
			title: "Track Bots and AI Scrapers",
			description: "Identify and manage bots and AI scrapers to protect your data effortlessly.",
			icon: "fas fa-robot",
			color: "linear-gradient(135deg, #663399, #ff4000)"
		},
		{
			title: "Performance Monitoring",
			description: "Monitor your API performance to ensure they meet your service level agreements.",
			icon: "fas fa-tachometer-alt",
			color: "linear-gradient(135deg, #ff4000, #ffa600)"
		},
		{
			title: "Real-time API Analytics",
			description: "Gain instant insights into your API usage and optimize your services.",
			icon: "fas fa-chart-line",
			color: "linear-gradient(135deg, #ffa600, #bc5090)"
		},
		{
			title: "Anomaly Alerts",
			description: "Receive immediate notifications when your APIs exhibit unusual behavior.",
			icon: "fas fa-exclamation-triangle",
			color: "linear-gradient(135deg, #bc5090, #003f5c)"
		},
		{
			title: "Understand Your Users",
			description: "Discover valuable insights about user behavior and preferences.",
			icon: "fas fa-user-friends",
			color: "linear-gradient(135deg, #003f5c, #58508d)"
		}
	];
</script>

<section class="feature-section">
	<div class="container">
		<h2>Powerful Features</h2>
		<p>Built by developers, for developers.</p>
		<div class="features-row">
			{#each features as feature}
				<div class="feature-item">
					<div class="feature-header" style="background: {feature.color}">
						<i class="{feature.icon}"></i>
					</div>
					<h3>{feature.title}</h3>
					<p>{feature.description}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<style>
	.feature-section {
		padding: 60px 20px;
		color: #333;
		text-align: center;
		/* background-color: #f3f3f3; */
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
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

	.features-row {
		display: flex;
		justify-content: space-between;
		gap: 20px;
		flex-wrap: wrap;
	}

	.feature-item {
		background: #fff;
		padding: 20px;
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		text-align: center;
		flex: 1;
		min-width: 160px;
	}

	.feature-header {
		width: 60px;
		height: 60px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0 auto 20px;
	}

	.feature-item i {
		font-size: 2rem;
		color: #fff;
	}

	.feature-item h3 {
		font-size: 1.5rem;
		margin: 0;
		color: #333;
	}

	.feature-item p {
		font-size: 1rem;
		color: #555;
		margin: 10px 0 20px;
	}

	@media (max-width: 768px) {
		.features-row {
			flex-direction: column;
		}
	}

	@media (max-width: 480px) {
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
</style>
