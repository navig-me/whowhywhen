<script>
    import { Router, Route, Link } from 'svelte-routing';
    import Login from '../routes/Login.svelte';
    import Register from '../routes/Register.svelte';
  </script>
  
  <Router>
    <Route path="/login" component={Login} />
    <Route path="/register" component={Register} />
  </Router>
  
  <header class="header">
    <div class="container">
      <h1>WhoWhyWhen</h1>
      <nav>
        <Link to="login">
          <a class="btn-primary">Login</a>
        </Link>
        <Link to="register">
          <a class="btn-secondary">Register</a>
        </Link>
      </nav>
    </div>
  </header>
  
  <style>
    .header {
      background-color: #fff;
      padding: 20px 0;
      border-bottom: 1px solid #ddd;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
  
    .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    .header h1 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: bold;
      letter-spacing: 1px;
      background: linear-gradient(135deg, #663399, #ff4000);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  
    nav {
      display: flex;
      gap: 10px;
    }
  
    nav a {
      padding: 10px 20px;
      border-radius: 5px;
      text-decoration: none;
      transition: background-color 0.3s, color 0.3s;
      display: inline-block;
    }
  
    .btn-primary {
      background-color: #fff;
      color: #663399;
      border: 1px solid #fff;
      text-decoration: none;
    }
  
    .btn-primary:hover {
      background-color: #663399;
      color: #fff;
    }
  
    .btn-secondary {
      background-color: #fff;
      color: #ff4000;
      border: 1px solid #fff;
      text-decoration: none;
    }
  
    .btn-secondary:hover {
      background-color: #ff4000;
      color: #fff;
    }
  </style>
  