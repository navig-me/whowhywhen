<script>
	import HeroSection from '../components/HeroSection.svelte';
	import FeatureSection from '../components/FeatureSection.svelte';
	import PricingSection from '../components/PricingSection.svelte';
	import Questions from '../components/Questions.svelte';
	import Footer from '../components/Footer.svelte';

	const questions = [
		"Why is my endpoint failing?", "Why high bot traffic?", "Why do I need to support mobile view?",
		"Who visited my app?", "Where are my visitors located?", "When does my API fail more?",
		"When do people visit the most?", "What browsers do my users use?", "Who uses my API the most?",
		"What time of day is busiest?", "Why is uptime important?", "When do I get the most errors?",
		"What is the average response time?", "Why monitor API performance?", "Who are my top users?",
		"When is my API least used?", "What devices do users prefer?", "Who experiences the most errors?",
		"Why do I need real-time analytics?", "What endpoints are most popular?", "Why track API usage?",
		"When is peak usage time?", "Who benefits from my API?", "Why is performance monitoring key?",
		"Where are the most errors occurring?", "Who needs uptime reports?", "What is causing slow responses?",
		"Why customize reports?", "When should I scale my API?", "Who relies on my API?", 
		"Where is my API used the most?", "Why track user behavior?", "What are my API's key metrics?",
		"Why set performance baselines?", "When do users experience downtime?", "What is the uptime percentage?",
		"Who triggers the most alerts?", "Why are notifications important?", "What reports are most useful?",
		"Where can I optimize performance?"
	];
</script>

<div class="parallax-wrapper">
	<div class="parallax"></div>
	<div class="content-wrapper">
		<HeroSection />
		<FeatureSection />
	</div>
</div>
<Questions {questions} />
<PricingSection />
<Footer />

<style>
	@import '../styles/global.css';

	.parallax-wrapper {
		position: relative;
		overflow: hidden;
	}

	.parallax {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: url('/supercharge.jpg') no-repeat center center/cover;
		background-attachment: fixed;
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;
		z-index: -1;
	}

	.content-wrapper {
		position: relative;
		z-index: 1;
	}

	.overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.6); /* Dark overlay */
	}

	.container {
		position: relative;
		z-index: 2;
		padding: 50px 20px;
		background: rgba(255, 255, 255, 0.8);
		border-radius: 10px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	}

	@media (max-width: 768px) {
		.container {
			padding: 20px;
		}
	}

	@media (max-width: 480px) {
		.container {
			padding: 10px;
		}
	}
</style>
