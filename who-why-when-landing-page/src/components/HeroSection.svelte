<script>
	import { currentView } from '../stores/viewStore';
  
	function changeView(view) {
	  currentView.set(view);
	}
</script>
  
<section class="hero-section">
	<div class="overlay">
		<div class="container">
			<h2><span class="supercharge">Supercharge</span> Your API Insights</h2>
			<p>Unlock detailed insights, optimize resources, and take control of your API performance with our lightweight and flexible analytics.</p>
			<button class="btn-primary" on:click={() => changeView('register')}>Get Started</button>
		</div>
	</div>
</section>
  
<style>
.hero-section {
	position: relative;
	background: url('/www-bg.webp') no-repeat center center/cover;
	color: #fff;
	padding: 200px 20px;
	text-align: center;
	overflow: hidden;
	background-attachment: fixed;
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	background-blend-mode: overlay;
}

.overlay {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.6); /* Darker overlay for better text visibility */
	display: flex;
	align-items: center;
	justify-content: center;
	height: 100%; /* Ensures overlay covers the entire section */
}

.container {
	position: relative;
	z-index: 1;
	max-width: 800px;
	padding: 0 20px;
	animation: fadeIn 1.5s ease-in-out;
}

.hero-section h2 {
	margin: 0 0 20px;
	font-size: 3rem;
	font-weight: bold;
	letter-spacing: 2px;
	animation: fadeInDown 1s ease-in-out;
}

.hero-section p {
	margin: 0 0 30px;
	font-size: 1.2rem;
	animation: fadeInUp 1s ease-in-out;
}

.btn-primary {
	background-color: #ff4000;
	color: #fff;
	padding: 15px 30px;
	border: none;
	border-radius: 30px;
	text-transform: uppercase;
	font-size: 1rem;
	font-weight: bold;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
	transition: background-color 0.3s, transform 0.3s;
	cursor: pointer;
}

.btn-primary:hover {
	background-color: #e63900;
	transform: scale(1.05);
}

@keyframes fadeInDown {
	0% {
		opacity: 0;
		transform: translateY(-50px);
	}
	100% {
		opacity: 1;
		transform: translateY(0);
	}
}

@keyframes fadeInUp {
	0% {
		opacity: 0;
		transform: translateY(50px);
	}
	100% {
		opacity: 1;
		transform: translateY(0);
	}
}

@keyframes fadeIn {
	0% {
		opacity: 0;
	}
	100% {
		opacity: 1;
	}
}

.supercharge {
	background: linear-gradient(90deg, #ff4000, #ff7300, #ffd700, #73ff00, #00ffd0, #0073ff, #ff00d0);
	background-size: 600%;
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	animation: gradient 5s ease infinite;
}

@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}

@media (max-width: 768px) {
	.hero-section h2 {
		font-size: 2.5rem;
	}
  
	.hero-section p {
		font-size: 1rem;
	}
  
	.btn-primary {
		padding: 10px 20px;
		font-size: 0.9rem;
	}
}

@media (max-width: 480px) {
	.hero-section h2 {
		font-size: 2rem;
	}
  
	.hero-section p {
		font-size: 0.9rem;
	}
  
	.btn-primary {
		padding: 10px 20px;
		font-size: 0.8rem;
	}
}
</style>
