<section class="pricing-section">
    <div class="container">
      <h2>Pricing</h2>
      <div class="plans">
        <div class="plan">
          <h3>Free Plan</h3>
          <p><i class="fas fa-check"></i> 50,000 monthly free calls</p>
          <p><i class="fas fa-check"></i> Basic Analytics</p>
          <p class="price">$0/month</p>
          <a href="/register" class="btn-primary">Get Started</a>
        </div>
        <div class="plan best-value">
          <h3>Pro Plan</h3>
          <p><i class="fas fa-check"></i> 500,000 monthly calls</p>
          <p><i class="fas fa-check"></i> Advanced Analytics</p>
          <p class="price">$10/month</p>
          <a href="/register" class="btn-primary">Get Started</a>
        </div>
      </div>
    </div>
  </section>
  
  <style>
    .pricing-section {
      padding: 20px 0;
      background: #f9f9f9;
      text-align: center;
    }
  
    .plans {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 40px;
      margin-top: 40px;
    }
  
    .plan {
      width: 30%;
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
  
    .btn-primary, .btn-secondary {
      display: inline-block;
      margin-top: 20px;
      padding: 10px 20px;
      border-radius: 30px;
      text-transform: uppercase;
      font-size: 1rem;
      font-weight: bold;
      text-decoration: none;
      transition: background-color 0.3s, transform 0.3s;
    }
  
    .btn-primary {
      background-color: #ff4000;
      color: #fff;
    }
  
    .btn-primary:hover {
      background-color: #e63900;
      transform: scale(1.05);
    }
  
    .btn-secondary {
      background-color: #663399;
      color: #fff;
    }
  
    .btn-secondary:hover {
      background-color: #552288;
      transform: scale(1.05);
    }
  
    .pricing-section .icon {
      margin-right: 8px;
    }
  </style>
  