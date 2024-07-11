<script>
  import { onMount } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { clearToken, isLoggedIn } from '../stores/userStore';
  import { DASH_API_BASE_URL } from '../config'; // Import the base URL

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
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/users/me`, {
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
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/stripe/payment-link/${planName}`, {
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
    if (planName === 'free') return '#1E90FF'; // FREE
    if (planName === 'starter') return '#ff4500'; // STARTER
    if (planName === 'pro') return '#8A2BE2'; // PRO
    return '#1E90FF'; // Default to blue if no plan found
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
          <a class="nav-link" href="https://whowhywhen.github.io" target="_blank" rel="noopener noreferrer">Docs</a>
          <a class="nav-link" on:click={() => changeView('dashboard')}>Dashboard</a>
          <a class="nav-link" on:click={() => changeView('projects')}>Projects</a>
          <a class="nav-link logout-link" on:click={logout}>Logout</a>
        {:else}
          <a class="nav-link" href="https://whowhywhen.github.io" target="_blank" rel="noopener noreferrer">Docs</a>
          <a class="nav-link" on:click={() => changeView('login')}>Login</a>
          <a class="nav-link" on:click={() => changeView('register')}>Register</a>
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
    position: relative;
    z-index: 10; /* Increased z-index for mobile view */
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
    gap: 20px;
    align-items: center;
  }

  nav a {
    text-decoration: none;
    transition: color 0.3s;
    cursor: pointer;
    font-size: 1.1rem;
  }

  .nav-link {
    color: #663399;
  }

  .nav-link:hover {
    color: #ff4500;
  }

  .logout-link {
    color: #ff4500;
  }

  .logout-link:hover {
    color: #663399;
  }

  .plan-section {
    padding: 10px;
    border-radius: 10px;
    border: 0.1px solid;
    background-color: #f9f9f9;
    background-size: 56.57px 56.57px; /* Adjust based on the size needed */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 180px; /* Smaller and more sleek */
  }

  .user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    cursor: pointer;
    transition: all 0.3s;
  }

  .plan-info {
    font-weight: bold;
    text-align: center;
    font-size: 1rem; /* Adjusted text size */
    width: 100%;
  }

  .request-info {
    width: 100%;
    margin-top: 5px;
  }

  .request-bar-container {
    position: relative;
    width: 100%;
    margin-top: 5px;
  }

  .request-bar {
    width: 100%;
    height: 8px;
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
    font-size: 0.7rem; /* Smaller font size */
    color: #fff;
    font-weight: bold;
  }

  .upgrade-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #ff4500;
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    text-decoration: none;
    font-size: 0.7rem; /* Smaller font size */
    font-weight: bold;
    opacity: 0;
    transition: opacity 0.3s;
    width: 100%;
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
      z-index: 11; /* Increased z-index for mobile view */
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
      border: 0.2px solid; /* Ensure border is visible */
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
