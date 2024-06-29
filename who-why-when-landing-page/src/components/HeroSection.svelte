<section class="hero-section">
    <div class="overlay">
      <div class="container">
        <h2>Discover the Power of Your APIs</h2>
        <p>Unlock detailed insights on how your APIs are being used. Improve performance and grow your business.</p>
        <a href="/register" class="btn-primary">Get Started</a>
      </div>
    </div>
  </section>
  
  <style>
    .hero-section {
      position: relative;
      background: url('/www-bg.webp') no-repeat center center/cover;
      color: #fff;
      padding: 150px 0;
      text-align: center;
      overflow: hidden;
    }
  
    .overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.6); /* Overlay to darken the background image */
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%; /* Ensures overlay covers the entire section */
    }
  
    .container {
      position: relative;
      z-index: 1;
      max-width: 800px;
    }
  
    .hero-section h1 {
      margin: 0 0 20px;
      font-size: 3.5rem;
      font-weight: bold;
      animation: fadeInDown 1s ease-in-out;
    }
  
    .hero-section p {
      margin: 0 0 30px;
      font-size: 1.5rem;
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
  </style>
  