<section class="feature-section">
	<!-- <div class="parallax" style="background-image: url('/background1.png');"></div> -->
	<div class="container">
	  <h2>Powerful Features</h2>
	  <p>Our platform offers a comprehensive set of tools to help you manage and optimize your APIs effectively.</p>
	  <div class="features">
		<div class="feature">
		  <div class="icon">
			<i class="fas fa-chart-line"></i>
		  </div>
		  <h3>Real-time Analytics</h3>
		  <p>Access real-time analytics and see how your APIs are being used, enabling you to make informed decisions and optimize your services.</p>
		</div>
		<div class="feature">
		  <div class="icon">
			<i class="fas fa-tachometer-alt"></i>
		  </div>
		  <h3>Performance Monitoring</h3>
		  <p>Monitor the performance of your APIs and ensure they are meeting your SLAs.</p>
		</div>
		<div class="feature">
		  <div class="icon">
			<i class="fas fa-bell"></i>
		  </div>
		  <h3>Alerts and Notifications</h3>
		  <p>Receive alerts and notifications when your APIs are under or over performance baselines.</p>
		</div>
		<div class="feature">
		  <div class="icon">
			<i class="fas fa-file-alt"></i>
		  </div>
		  <h3>Customizable Reports</h3>
		  <p>Generate detailed, customizable reports that provide insights into API usage trends, helping you optimize your services.</p>
		</div>
		<div class="feature">
		  <div class="icon">
			<i class="fas fa-cogs"></i>
		  </div>
		  <h3>Seamless Integration</h3>
		  <p>Integrate WhoWhyWhen effortlessly into your platform with our easy-to-use code snippets and comprehensive documentation.</p>
		</div>
	  </div>
	</div>
	<div class="parallax" style="background-image: url('/background1.png');"></div>
  </section>
  
  <style>
	.feature-section {
	  position: relative;
	  overflow: hidden;
	  color: #333;
	}
  
	.parallax {
	  position: relative;
	  height: 300px; /* Adjust based on the image height you want to show */
	  background-attachment: fixed;
	  background-position: center;
	  background-repeat: no-repeat;
	  background-size: cover;
	  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay */
	  background-blend-mode: overlay;
	}
  
	.overlay {
	  position: absolute;
	  top: 0;
	  left: 0;
	  right: 0;
	  bottom: 0;
	  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay */
	  background-blend-mode: overlay;
	}
  
	.container {
	  position: relative;
	  z-index: 2;
	  padding: 50px 20px;
	  text-align: center;
	  background: linear-gradient(135deg, #f9f9f9, #e0e0e0);
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
  
	.features {
	  display: flex;
	  flex-wrap: wrap;
	  justify-content: center;
	  gap: 40px;
	}
  
	.feature {
	  width: 22%;
	  background: #fff;
	  padding: 30px;
	  border-radius: 10px;
	  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	  transition: transform 0.3s, box-shadow 0.3s;
	  text-align: left;
	}
  
	.feature:hover {
	  transform: translateY(-10px);
	  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2);
	}
  
	.icon {
	  margin-bottom: 20px;
	  color: #663399; /* Icon color */
	}
  
	.icon i {
	  font-size: 3rem;
	}
  
	.feature h3 {
	  margin-bottom: 15px;
	  font-size: 1.8rem;
	  color: #663399;
	}
  
	.feature p {
	  font-size: 1rem;
	  color: #555;
	}
  
	@media (max-width: 768px) {
	  .features {
		flex-direction: column;
		align-items: center;
	  }
  
	  .feature {
		width: 80%;
		margin-bottom: 20px;
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
  
	  .feature {
		width: 90%;
		padding: 20px;
	  }
  
	  .feature h3 {
		font-size: 1.5rem;
	  }
  
	  .feature p {
		font-size: 0.9rem;
	  }
	}
  </style>
  