<script>
    import { Link } from 'svelte-routing';
  </script>
  
  <nav class="nav">
    <div class="container">
      <h1 class="logo">WhoWhyWhen</h1>
      <ul class="nav-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="login">Login</Link></li>
        <li><Link to="register">Register</Link></li>
      </ul>
    </div>
  </nav>
  
  <style>
    .nav {
      background-color: #663399;
      color: #fff;
      padding: 1rem 0;
    }
  
    .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
    }
  
    .logo {
      font-size: 1.5rem;
      font-weight: bold;
    }
  
    .nav-links {
      list-style: none;
      display: flex;
      gap: 1rem;
    }
  
    .nav-links li a {
      color: #fff;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 5px;
      transition: background-color 0.3s;
    }
  
    .nav-links li a:hover {
      background-color: #552288;
    }
  </style>
  