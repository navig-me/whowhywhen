<script>
	import { currentView } from '../stores/viewStore';
  
	function changeView(view) {
	  currentView.set(view);
	}
</script>

<section class="pricing-section">
	<div class="container">
		<h2>Choose Your Plan</h2>
		<p>Flexible and affordable pricing plans to suit your needs.</p>
		<div class="plans">
			<div class="plan">
				<h3>FREE</h3>
				<p><i class="fas fa-check"></i> 20,000 monthly free calls</p>
				<p><i class="fas fa-check"></i> Basic Analytics</p>
				<p class="price">$0/month</p>
				<button class="btn-primary" on:click={() => changeView('register')}>Get Started</button>
			</div>
			<div class="plan best-value">
				<h3>STARTER</h3>
				<p><i class="fas fa-check"></i> 250,000 monthly calls</p>
				<p><i class="fas fa-check"></i> Advanced Analytics</p>
				<p class="price">$9/month</p>
				<button class="btn-primary" on:click={() => changeView('register')}>Get Started</button>
			</div>
			<div class="plan">
				<h3>PRO</h3>
				<p><i class="fas fa-check"></i> 5,000,000 monthly calls</p>
				<p><i class="fas fa-check"></i> Advanced Analytics</p>
				<p><i class="fas fa-check"></i> Enhanced IP and Device Information</p>
				<p class="price">$39/month</p>
				<button class="btn-primary" on:click={() => changeView('register')}>Get Started</button>
			</div>
		</div>
	</div>
</section>

<style>
.pricing-section {
	padding: 100px 20px;
	background: #f9f9f9;
	text-align: center;
	color: #333;
}

.pricing-section h2 {
	font-size: 2.5rem;
	margin-bottom: 10px;
	color: #663399;
}

.pricing-section p {
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
	width: 22%;
	background: #fff;
	padding: 30px;
	border-radius: 10px;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	transition: transform 0.3s, box-shadow 0.3s;
}

.plan.best-value {
	border: 2px solid #ff4000;
}

.plan:hover {
	transform: translateY(-10px);
	box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2);
}

.plan h3 {
	margin-bottom: 20px;
	font-size: 1.8rem;
	color: #663399;
}

.plan p {
	margin-bottom: 15px;
	font-size: 1rem;
	color: #555;
}

.plan .price {
	margin: 20px 0;
	font-size: 2rem;
	color: #333;
	font-weight: bold;
}

.btn-primary {
	background-color: #ff4000;
	color: #fff;
	padding: 10px 20px;
	border: none;
	border-radius: 30px;
	text-transform: uppercase;
	font-size: 1rem;
	font-weight: bold;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
	transition: background-color 0.3s, transform 0.3s;
	cursor: pointer;
	margin-top: 20px;
}

.btn-primary:hover {
	background-color: #e63900;
	transform: scale(1.05);
}
</style>
