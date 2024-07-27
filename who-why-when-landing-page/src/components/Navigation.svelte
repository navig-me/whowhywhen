  <!-- Navigation.svelte -->
  <script>
    import { Link } from 'svelte-routing';
    import { isLoggedIn, clearToken, changeView } from '../stores/userStore';

    let loggedIn;
    isLoggedIn.subscribe(value => {
      loggedIn = value;
    });

    function logout() {
      isLoggedIn.set(false);
      clearToken();
      // changeView('home');
    }
  </script>

  <nav class="nav">
    <div class="container">
      <h1 class="logo">WhoWhyWhen</h1>
      <ul class="nav-links">
        <li><Link to="/">Home</Link></li>
        {#if loggedIn}
          <li><Link to="dashboard">Dashboard</Link></li>
          <li><Link to="bots">Bots</Link></li>
          <li><Link to="projects">Projects</Link></li>
          <li><Link to="integrate">Usage Guide</Link></li>
          <li><a on:click={logout}>Logout</a></li>
        {:else}
          <li><Link to="integrate">Usage Guide</Link></li>
          <li><Link to="login">Login</Link></li>
          <li><Link to="register">Register</Link></li>
        {/if}
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
