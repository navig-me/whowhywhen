  <script>
    import { currentView } from '../stores/viewStore';
    import { isLoggedIn } from '../stores/userStore';

    let loggedIn;
    isLoggedIn.subscribe(value => {
      loggedIn = value;
    });

    function changeView(view) {
      currentView.set(view);
    }

    function logout() {
      isLoggedIn.set(false);
      changeView('home');
    }
  </script>

  <header class="header">
    <div class="container">
      <h1 on:click={() => changeView('home')}>WhoWhyWhen</h1>
      <nav>
        {#if loggedIn}
          <a class="btn-primary" href="https://github.com/navig-me/whowhywhen-docs" target="_blank" rel="noopener noreferrer">Docs</a>
          <a class="btn-secondary" on:click={() => changeView('dashboard')}>Dashboard</a>
          <a class="btn-primary" on:click={() => changeView('projects')}>Projects</a>
          <a class="btn-secondary" on:click={logout}>Logout</a>
        {:else}
          <a class="btn-primary" href="https://github.com/navig-me/whowhywhen-docs" target="_blank" rel="noopener noreferrer">Docs</a>
          <a class="btn-secondary" on:click={() => changeView('login')}>Login</a>
          <a class="btn-primary" on:click={() => changeView('register')}>Register</a>
        {/if}
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
      cursor: pointer;
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
      cursor: pointer;
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
