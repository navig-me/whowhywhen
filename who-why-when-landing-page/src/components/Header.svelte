<script>
  import { Link } from 'svelte-routing';
  import { currentView } from '../stores/viewStore';
  import { clearToken, isLoggedIn } from '../stores/userStore';
  import { DASH_API_BASE_URL } from '../config';
  import { navigate } from 'svelte-routing';
  import { get } from 'svelte/store';

  let loggedIn;
  let user = null;
  let userRequestCount = 0;
  let monthlyCreditLimit = 0;
  let monthlyCreditUsageCrossed = false;
  let unreadAlertCount = 0;
  let upgradeLink = '';
  let menuOpen = false;

  isLoggedIn.subscribe(value => {
    loggedIn = value;
    if (loggedIn) {
      fetchUserDetails();
    }
  });

  function changeView(view) {
    navigate(view);
    menuOpen = false;
  }

  function logout() {
    isLoggedIn.set(false);
    clearToken();
    changeView('/');
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
      unreadAlertCount = data.unread_alert_count;

      const nextPlan = getNextPlan(user.subscription_plan);
      if (nextPlan) {
        upgradeLink = await fetchUpgradeLink(nextPlan, token);
      }
    } else if (response.status === 401) {
      clearToken();
      changeView('/');
    }
  }

  function getNextPlan(currentPlan) {
    if (currentPlan === 'free') return 'starter';
    if (currentPlan === 'starter') return 'pro';
    return '';
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

  function getRequestBarWidth(used, limit) {
    return (used / limit) * 100;
  }

  function getRequestBarClass(used, limit) {
    const percentage = (used / limit) * 100;
    if (percentage > 90 || monthlyCreditUsageCrossed) return 'bar-red';
    return 'bar-green';
  }

  function shouldShowRequestBar(used, limit) {
    const percentage = (used / limit) * 100;
    return percentage > 80;
  }

  function conditionalChangeView() {
    if (get(isLoggedIn)) {
      changeView('/dashboard');
    } else {
      changeView('/');
    }
  }
</script>

<header class="header">
  <div class="container">
    <h1 on:click={() => conditionalChangeView()}>WhoWhyWhen</h1>
    <nav>
      <div class="menu-toggle" on:click={() => menuOpen = !menuOpen}>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
      <div class={`menu ${menuOpen ? 'open' : ''}`}>
        {#if loggedIn}
          {#if user}
            <div class="nav-section">
              <Link class="nav-link" to="/dashboard">Dashboard</Link>
              <span class="dot">•</span>
              <Link class="nav-link" to="/bots">Bots</Link>
            </div>
            <div class="nav-section">
              <Link class="nav-link" to="/projects">Projects</Link>
              <span class="dot">•</span>
              <Link class="nav-link" to="/integrate">Setup & Integration</Link>
              <span class="dot">•</span>
              <div class="alerts-link">
                <Link class="nav-link" to="/alerts">
                  Alerts
                  {#if unreadAlertCount > 0}
                    <span class="alert-dot"></span>
                  {/if}
                </Link>
              </div>
            </div>
            <div class="nav-section">
              <Link class="nav-link" to="/user-settings">Settings</Link>
              {#if shouldShowRequestBar(userRequestCount, monthlyCreditLimit)}
                <div class="request-bar-container" on:click={() => changeView('/user-settings')}>
                  <div class="request-bar">
                    <div class="request-bar-inner {getRequestBarClass(userRequestCount, monthlyCreditLimit)}" style="width: {getRequestBarWidth(userRequestCount, monthlyCreditLimit)}%"></div>
                  </div>
                </div>
              {/if}
            </div>
            <div class="nav-section">
              <a class="nav-link logout-link" on:click={logout}>Logout</a>
            </div>
          {/if}
        {:else}
          <div class="nav-section">
            <Link class="nav-link" to="/integrate">Setup & Integration</Link>
          </div>
          <div class="nav-section">
            <Link class="nav-link" to="/login">Login</Link>
            <span class="dot">•</span>
            <Link class="nav-link" to="/register">Register</Link>
          </div>
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
    z-index: 10;
  }

  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .header h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: bold;
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

  .nav-section {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .nav-section + .nav-section {
    border-left: 1px solid #ddd;
    padding-left: 10px;
    margin-left: 10px;
  }

  .dot {
    color: #888;
    font-size: 1.5rem;
    line-height: 1;
    margin: 0 5px;
  }

  nav a {
    text-decoration: none;
    transition: color 0.3s;
    cursor: pointer;
    font-size: 1.1rem;
    position: relative;
  }

  .nav-link {
    color: #663399;
    font-weight: 500;
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

  .request-bar-container {
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .request-bar {
    width: 80px;
    height: 12px;
    background-color: #ddd;
    border-radius: 5px;
    overflow: hidden;
    margin-right: 10px;
    position: relative;
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
    font-size: 0.8rem;
    color: #333;
  }

  .alerts-link {
    position: relative;
  }

  .alert-dot {
    position: absolute;
    top: -2px;
    right: -5px;
    width: 5px;
    height: 5px;
    background-color: #ff4000;
    border-radius: 50%;
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
      z-index: 11;
    }

    .menu.open {
      display: flex;
    }

    nav a {
      padding: 10px;
      border-bottom: 1px solid #ddd;
    }

    .nav-section + .nav-section {
      border-left: none;
      padding-left: 0;
      margin-left: 0;
    }

    .request-bar-container {
      width: 100%;
      max-width: 120px;
      min-width: 100px;
      padding: 10px;
      border-radius: 0;
      box-shadow: none;
      border: 0.2px solid;
      box-sizing: border-box;
    }
  }
</style>
