<script>
	import HeroSection from '../components/HeroSection.svelte';
	import FeatureSection from '../components/FeatureSection.svelte';
	import PricingSection from '../components/PricingSection.svelte';
	import Footer from '../components/Footer.svelte';
</script>

<div class="parallax-wrapper">
	<div class="parallax"></div>
	<div class="content-wrapper">
		<HeroSection />
		<FeatureSection />
	</div>
</div>
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
