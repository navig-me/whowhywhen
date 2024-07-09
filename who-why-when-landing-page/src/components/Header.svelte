<script>
  import { onMount } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { clearToken, isLoggedIn } from '../stores/userStore';
  import { API_BASE_URL } from '../config'; // Import the base URL

  let loggedIn;
  let user = null;
  let userRequestCount = 0;
  let monthlyCreditLimit = 0;
  let monthlyCreditUsageCrossed = false;
  let upgradeLink = '';
  let menuOpen = false; // State for menu toggle

  isLoggedIn.subscribe(value => {
    loggedIn = value;
    if (loggedIn) {
      fetchUserDetails();
    }
  });

  function changeView(view) {
    currentView.set(view);
    menuOpen = false; // Close the menu when changing views
  }

  function logout() {
    isLoggedIn.set(false);
    clearToken();
    changeView('home');
  }

  async function fetchUserDetails() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/auth/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      user = data.user;
      userRequestCount = data.user_request_count;
      monthlyCreditLimit = data.user.monthly_credit_limit;
      monthlyCreditUsageCrossed = data.user.monthly_credit_usage_crossed;
      const nextPlan = getNextPlan(user.subscription_plan);
      if (nextPlan) {
        upgradeLink = await fetchUpgradeLink(nextPlan, token);
      }
    } else if (response.status === 401) {
      clearToken();
      changeView('home');
    }
  }

  function getNextPlan(currentPlan) {
    if (currentPlan === 'free') return 'starter';
    if (currentPlan === 'starter') return 'pro';
    return ''; // No next plan for PRO
  }

  async function fetchUpgradeLink(planName, token) {
    if (!planName) return '';
    const response = await fetch(`${API_BASE_URL}/auth/stripe/payment-link/${planName}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.ok) {
      return await response.json();
    }
    return '';
  }

  function getPlanColor(planName) {
    if (planName === 'free') return '#0000FF'; // FREE
    if (planName === 'starter') return '#ff4000'; // STARTER
    if (planName === 'pro') return '#663399'; // PRO
    return '#0000FF'; // Default to black if no plan found
  }

  function getPlanName(planName) {
    if (planName === 'free') return 'FREE';
    if (planName === 'starter') return 'STARTER';
    if (planName === 'pro') return 'PRO';
    return 'FREE';
  }

  function getRequestBarWidth(used, limit) {
    return (used / limit) * 100;
  }

  function getRequestBarClass(used, limit) {
    const percentage = (used / limit) * 100;
    if (percentage > 90 || monthlyCreditUsageCrossed) return 'bar-red';
    return 'bar-green';
  }
</script>

<header class="header">
  <div class="container">
    <h1 on:click={() => changeView('home')}>WhoWhyWhen</h1>
    <nav>
      <div class="menu-toggle" on:click={() => menuOpen = !menuOpen}>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
      <div class={`menu ${menuOpen ? 'open' : ''}`}>
        {#if loggedIn}
          {#if user}
            <div class="plan-section">
              <div class="user-info">
                <div class="plan-info" style="color: {getPlanColor(user.subscription_plan)}">
                  Plan: {getPlanName(user.subscription_plan)}
                </div>
                <div class="request-info">
                  <div class="request-bar-container">
                    <div class="request-bar">
                      <div class="request-bar-inner {getRequestBarClass(userRequestCount, monthlyCreditLimit)}" style="width: {getRequestBarWidth(userRequestCount, monthlyCreditLimit)}%"></div>
                    </div>
                    <span class="request-count">{userRequestCount}/{monthlyCreditLimit}</span>
                  </div>
                </div>
                {#if user.subscription_plan === 'pro'}
                  <a class="upgrade-button" href="mailto:upgrade@whowhywhen.com">Contact to Upgrade</a>
                {:else}
                  <a class="upgrade-button" href={upgradeLink} target="_blank" rel="noopener noreferrer">Upgrade to {getNextPlan(user.subscription_plan).toUpperCase()}</a>
                {/if}
              </div>
            </div>
          {/if}
          <a class="btn-primary" href="https://whowhywhen.github.io" target="_blank" rel="noopener noreferrer">Docs</a>
          <a class="btn-primary" on:click={() => changeView('dashboard')}>Dashboard</a>
          <a class="btn-primary" on:click={() => changeView('projects')}>Projects</a>
          <a class="btn-secondary" on:click={logout}>Logout</a>
        {:else}
          <a class="btn-primary" href="https://whowhywhen.github.io" target="_blank" rel="noopener noreferrer">Docs</a>
          <a class="btn-secondary" on:click={() => changeView('login')}>Login</a>
          <a class="btn-secondary" on:click={() => changeView('register')}>Register</a>
        {/if}
      </div>
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
    flex-wrap: wrap;
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
    align-items: center;
  }

  .menu-toggle {
    display: none;
    flex-direction: column;
    cursor: pointer;
  }

  .menu-toggle .bar {
    width: 25px;
    height: 3px;
    background-color: #333;
    margin: 4px 0;
    transition: all 0.3s ease;
  }

  .menu {
    display: flex;
    gap: 10px;
    align-items: center;
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

  .plan-section {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    cursor: pointer;
    transition: all 0.3s;
    width: 250px; /* Ensuring consistent width */
  }

  .plan-info {
    font-weight: bold;
    text-align: center;
    width: 100%; /* Ensure the width matches the container */
  }

  .request-info {
    width: 100%; /* Ensure the width matches the container */
    margin-top: 10px;
  }

  .request-bar-container {
    position: relative;
    width: 100%;
    margin-top: 10px;
  }

  .request-bar {
    width: 100%;
    height: 15px; /* Increase height for better visibility */
    background-color: #ddd;
    border-radius: 5px;
    overflow: hidden;
    transition: width 0.3s;
  }

  .request-bar-inner {
    height: 100%;
  }

  .bar-green {
    background-color: #28a745;
  }

  .bar-red {
    background-color: #dc3545;
  }

  .request-count {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.75rem;
    color: #fff;
    font-weight: bold;
  }

  .upgrade-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #ff4000;
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: bold;
    opacity: 0;
    transition: opacity 0.3s;
    width: 100%; /* Ensure the width matches the container */
    text-align: center;
  }

  .user-info:hover .plan-info,
  .user-info:hover .request-info {
    opacity: 0;
  }

  .user-info:hover .upgrade-button {
    opacity: 1;
  }

  @media (max-width: 768px) {
    .menu-toggle {
      display: flex;
    }

    .menu {
      display: none;
      flex-direction: column;
      width: 100%;
      text-align: center;
      background-color: #fff;
      position: absolute;
      top: 60px;
      left: 0;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      z-index: 1;
    }

    .menu.open {
      display: flex;
    }

    nav a {
      padding: 10px;
      border-bottom: 1px solid #ddd;
    }

    .plan-section {
      width: 100%;
      padding: 10px;
      border-radius: 0;
      box-shadow: none;
    }

    .user-info {
      width: 100%;
    }

    .upgrade-button {
      position: relative;
      transform: none;
      margin-top: 10px;
      opacity: 1;
    }
  }
</style>
