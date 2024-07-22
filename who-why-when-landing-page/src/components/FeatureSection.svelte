<script>
	let features = [
		{
			title: "Real-time Analytics",
			description: "Access real-time analytics and see how your APIs are being used, enabling you to make informed decisions and optimize your services.",
			icon: "fas fa-chart-line",
			img: "/analytics.png"
		},
		{
			title: "Performance Monitoring",
			description: "Monitor the performance of your APIs and ensure they are meeting your SLAs.",
			icon: "fas fa-tachometer-alt",
			img: "/monitoring.png"
		},
		{
			title: "Alerts and Notifications",
			description: "Receive alerts and notifications when your APIs are under or over performance baselines.",
			icon: "fas fa-bell"
		},
		{
			title: "Customizable Reports",
			description: "(Coming Soon) Generate detailed, customizable reports that provide insights into API usage trends, helping you optimize your services.",
			icon: "fas fa-file-alt",
			"img": "/reports.png"
		},
		{
			title: "Understand Your Users",
			description: "Gain insights into your users' behavior and preferences, enabling you to personalize your services and improve user experience.",
			icon: "fas fa-user-friends",
			img: "/users.png"
		}
	];

	let selectedFeature = features[0];
</script>

<section class="feature-section">
	<div class="container">
		<h2>Powerful Features</h2>
		<p>Built by developers, for developers. </p>
		<div class="content">
			<div class="feature-list">
				{#each features as feature}
					<div class="feature-item" on:mouseover={() => selectedFeature = feature}>
						<div class="icon">
							<i class="{feature.icon}"></i>
						</div>
						<h3>{feature.title}</h3>
					</div>
				{/each}
			</div>
			<div class="feature-detail">
				<div class="icon">
					<i class="{selectedFeature.icon}"></i>
				</div>
				<h3>{selectedFeature.title}</h3>
				<p>{selectedFeature.description}</p>
				{#if selectedFeature.img}
					<img src="{selectedFeature.img}" alt="{selectedFeature.title}">
				{/if}
			</div>
		</div>
	</div>
</section>

<style>
.feature-section {
	position: relative;
	overflow: hidden;
	color: #333;
	padding: 50px 20px;
}

.container {
	position: relative;
	z-index: 2;
	padding: 50px 20px;
	background: rgba(255, 255, 255, 0.8);
	border-radius: 10px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.feature-section h2 {
	font-size: 2.5rem;
	margin-bottom: 10px;
	color: #663399;
}

.feature-section p {
	font-size: 1.2rem;
	margin-bottom: 40px;
}

.content {
	display: flex;
	justify-content: space-between;
	gap: 20px;
}

.feature-list {
	display: flex;
	flex-direction: column;
	gap: 10px;
	width: 30%;
}

.feature-item {
	flex: 1;
	background: #fff;
	padding: 15px;
	border-radius: 10px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	cursor: pointer;
	transition: transform 0.3s, box-shadow 0.3s;
	text-align: left;
}

.feature-item:hover {
	transform: translateX(10px);
	box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2);
}

.feature-item .icon {
	margin-bottom: 10px;
	color: #663399;
}

.feature-item h3 {
	font-size: 1.2rem;
	color: #333;
}

.feature-detail {
	width: 68%;
	padding: 30px;
	background: #fff;
	border-radius: 10px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	transition: opacity 0.3s;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	text-align: center;
}

.feature-detail .icon {
	margin-bottom: 20px;
	color: #663399;
}

.feature-detail h3 {
	font-size: 1.8rem;
	margin-bottom: 15px;
	color: #333;
}

.feature-detail p {
	font-size: 1.2rem;
	color: #555;
	margin-bottom: 20px;
}

.feature-detail img {
	max-width: 100%;
	border-radius: 10px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
	.content {
		flex-direction: column;
	}

	.feature-list, .feature-detail {
		width: 100%;
	}

	.feature-detail {
		margin-top: 20px;
	}
}

@media (max-width: 480px) {
	.container {
		padding: 50px 10px;
	}

	.feature-section h2 {
		font-size: 2rem;
	}

	.feature-section p {
		font-size: 1rem;
		margin-bottom: 20px;
	}

	.feature-item {
		padding: 10px;
	}

	.feature-item h3 {
		font-size: 1rem;
	}

	.feature-detail {
		padding: 20px;
	}

	.feature-detail h3 {
		font-size: 1.5rem;
	}

	.feature-detail p {
		font-size: 1rem;
	}
}
</style>
