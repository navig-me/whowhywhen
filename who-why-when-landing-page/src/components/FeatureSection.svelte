<script>
	import { onMount, onDestroy } from 'svelte';

	let features = [
		{
			title: "Track Bots and AI Scrapers",
			description: "Know which bots and AI scrapers are accessing your data and how to block them.",
			icon: "fas fa-robot",
			img: "/bot.png"
		},
		{
			title: "Performance Monitoring",
			description: "Ensure they are meeting your performance SLAs.",
			icon: "fas fa-tachometer-alt",
			img: "/monitoring.png"
		},
		{
			title: "Real-time Analytics",
			description: "Optimize your services by knowing how your APIs are being used.",
			icon: "fas fa-chart-line",
			img: "/analytics.png"
		},
		{
			title: "Understand Your Users",
			description: "Gain insights into your users' behavior and preferences.",
			icon: "fas fa-user-friends",
			img: "/users.png"
		}
	];

	let selectedFeature = features[0];

	// Auto-scroll timer
	let interval;
	let currentIndex = 0;

	const startAutoScroll = () => {
		interval = setInterval(() => {
			currentIndex = (currentIndex + 1) % features.length;
			selectedFeature = features[currentIndex];
		}, 4000); 
	};

	const stopAutoScroll = () => {
		clearInterval(interval);
	};

	onMount(() => {
		startAutoScroll();
	});

	onDestroy(() => {
		stopAutoScroll();
	});
</script>

<section class="feature-section">
	<div class="container">
		<h2>Powerful Features</h2>
		<p>Built by developers, for developers.</p>
		<div class="features">
			<div class="feature-list">
				{#each features as feature}
					<div 
						class="feature-item {feature === selectedFeature ? 'active' : ''}" 
						on:click={() => { selectedFeature = feature; currentIndex = features.indexOf(feature); stopAutoScroll(); startAutoScroll(); }}
					>
						<i class="{feature.icon}"></i>
						<h3>{feature.title}</h3>
					</div>
				{/each}
			</div>
			<div class="feature-detail">
				<img src="{selectedFeature.img}" alt="{selectedFeature.title}" class="feature-img"/>
				<h3>{selectedFeature.title}</h3>
				<p>{selectedFeature.description}</p>
			</div>
		</div>
	</div>
</section>

<style>
	.feature-section {
		padding: 60px 20px;
		background-color: #f9f9f9; /* Light gray background for separation */
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
	}

	p {
		font-size: 1.2rem;
		margin-bottom: 40px;
	}

	.features {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 40px;
		flex-wrap: wrap;
	}

	.feature-list {
		display: flex;
		flex-direction: column;
		gap: 20px;
		width: 200px;
	}

	.feature-item {
		background: #fff; /* White background for feature items */
		padding: 20px;
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		cursor: pointer;
		transition: transform 0.3s, box-shadow 0.3s;
		text-align: center;
	}

	.feature-item.active,
	.feature-item:hover {
		background: #663399;
		color: #fff;
		transform: translateY(-5px);
		box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2);
	}

	.feature-item i {
		font-size: 1.4rem;
		margin-bottom: 10px;
	}

	.feature-item h3 {
		font-size: 1.2rem;
		margin: 0;
	}

	.feature-detail {
		flex: 1;
		text-align: center; /* Center-align the text */
		padding: 20px; /* Padding around the detail section */
		background: #fff; /* White background for detail section */
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	}

	.feature-detail img.feature-img {
		display: block; /* Make the image a block element */
		margin: 0 auto; /* Center the image */
		width: 600px; /* Fixed width */
		height: 400px; /* Fixed height */
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		margin-bottom: 20px;
		object-fit: cover; /* Ensure the image fits the container */
	}

	.feature-detail h3 {
		font-size: 1.8rem;
		margin-bottom: 15px;
		color: #333;
	}

	.feature-detail p {
		font-size: 1rem;
		color: #555;
		margin: 0 20px; /* Add margin for better text spacing */
	}

	@media (max-width: 768px) {
		.features {
			flex-direction: column;
			align-items: center;
		}

		.feature-item {
			width: 150px;
			padding: 15px;
		}

		.feature-item i {
			font-size: 1.5rem;
		}

		.feature-item h3 {
			font-size: 1rem;
		}

		.feature-detail {
			text-align: center;
		}

		.feature-detail img.feature-img {
			max-width: 100%;
			height: 200px;
			margin-bottom: 20px;
		}

		.feature-detail h3 {
			font-size: 1.5rem;
			margin-bottom: 10px;
		}

		.feature-detail p {
			font-size: 0.9rem;
			margin: 0 10px; /* Adjust margin for smaller screens */
		}
	}

	@media (max-width: 480px) {
		.feature-item {
			width: 120px;
			padding: 10px;
		}

		.feature-item i {
			font-size: 1.2rem;
		}

		.feature-item h3 {
			font-size: 0.8rem;
		}

		.feature-detail img.feature-img {
			max-width: 100%;
			height: 150px;
		}

		.feature-detail h3 {
			font-size: 1.2rem;
		}

		.feature-detail p {
			font-size: 0.8rem;
			margin: 0 5px; /* Adjust margin for smaller screens */
		}
	}
</style>
