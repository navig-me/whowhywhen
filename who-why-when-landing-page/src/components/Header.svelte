<script>
  import { Link } from 'svelte-routing';
  import { currentView } from '../stores/viewStore';
  import { clearToken, isLoggedIn } from '../stores/userStore';
  import { DASH_API_BASE_URL } from '../config';
  import { navigate } from 'svelte-routing';

  let loggedIn;
  let user = null;
  let userRequestCount = 0;
  let monthlyCreditLimit = 0;
  let monthlyCreditUsageCrossed = false;
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

  function calculateDaysUntilRenewal(resetDate) {
    const reset = new Date(resetDate);
    const now = new Date();
    const timeDiff = Math.abs(reset.getTime() - now.getTime());
    const diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
    return 30 - diffDays;
  }
</script>

<header class="header">
  <div class="container">
    <h1 on:click={() => changeView('/')}>WhoWhyWhen</h1>
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
                <div class="request-info">
                  <div class="request-bar-container">
                    <div class="request-bar">
                      <div class="request-bar-inner {getRequestBarClass(userRequestCount, monthlyCreditLimit)}" style="width: {getRequestBarWidth(userRequestCount, monthlyCreditLimit)}%"></div>
                    </div>
                    <span class="request-count">{userRequestCount}/{monthlyCreditLimit}</span>
                  </div>
                  <small class="renewal-info">Renews in {calculateDaysUntilRenewal(user.monthly_credit_limit_reset)} days</small>
                </div>
                {#if user.subscription_plan !== 'pro'}
                  <a class="upgrade-button" href={upgradeLink} target="_blank" rel="noopener noreferrer">Upgrade</a>
                {:else}
                  <a class="upgrade-button" href="mailto:support@whowhywhen.com">Contact to Upgrade</a>
                {/if}
              </div>
            </div>
          {/if}
          <!-- <a class="nav-link" href="https://whowhywhen.github.io" target="_blank" rel="noopener noreferrer">Docs</a> -->
          <Link class="nav-link" to="/dashboard">Dashboard</Link>
          <Link class="nav-link" to="/projects">Projects</Link>
          <Link class="nav-link" to="/integrate">Integrate</Link>
          <Link class="nav-link" to="/user-settings">
            <i class="fa fa-user"></i>
          </Link>
          <a class="nav-link logout-link" on:click={logout}>Logout</a>
        {:else}
          <!-- <a class="nav-link" href="https://whowhywhen.github.io" target="_blank" rel="noopener noreferrer">Docs</a> -->
          <Link class="nav-link" to="/integrate">Integrate</Link>
          <Link class="nav-link" to="/login">Login</Link>
          <Link class="nav-link" to="/register">Register</Link>
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
    color: #663399 !important;
  }

  .nav-link:hover {
    color: #ff4500;
  }

  .logout-link {
    color: #ff4500 !important;
  }

  .logout-link:hover {
    color: #663399;
  }

  .plan-section {
    padding: 10px;
    border-radius: 10px;
    border: 0.1px solid;
    background-color: #f9f9f9;
    background-size: 56.57px 56.57px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    box-sizing: border-box;
  }

  .user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    cursor: pointer;
    transition: all 0.3s;
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
    height: 12px;
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
    font-size: 0.6rem;
    color: #fff;
    font-weight: bold;
  }

  .renewal-info {
    font-size: 0.7rem;
    color: #888;
    margin-top: 5px;
    text-align: center;
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
    font-size: 0.8rem;
    font-weight: bold;
    opacity: 0;
    transition: opacity 0.3s;
    width: 100%;
    text-align: center;
  }

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
      z-index: 11;
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
      border: 0.2px solid;
      box-sizing: border-box;
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
