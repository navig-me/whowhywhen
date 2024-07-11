<script>
    import { onMount } from 'svelte';
    import { clearToken, isLoggedIn } from '../stores/userStore';
    import { DASH_API_BASE_URL } from '../config';
  
    let user = null;
    let upgradeLink = '';
    let daysUntilRenewal = 0;
    let userRequestCount = 0;
  
    onMount(async () => {
      await fetchUserDetails();
    });
  
    async function fetchUserDetails() {
      const token = localStorage.getItem('token');
      const response = await fetch(`${DASH_API_BASE_URL}/dashauth/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        userRequestCount = data.user_request_count;
        user = data.user;
        const nextPlan = getNextPlan(user.subscription_plan);
        if (nextPlan) {
          upgradeLink = await fetchUpgradeLink(nextPlan, token);
        }
        daysUntilRenewal = calculateDaysUntilRenewal(user.monthly_credit_limit_reset);
      } else if (response.status === 401) {
        clearToken();
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
  
    function calculateDaysUntilRenewal(resetDate) {
      const reset = new Date(resetDate);
      const now = new Date();
      const timeDiff = Math.abs(reset.getTime() - now.getTime());
      const diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
      return 30 - diffDays;
    }
  </script>
  
  <section class="user-settings">
    {#if user}
      <h2>User Settings</h2>
      <div class="user-info">
        <p><strong>Name:</strong> {user.name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Plan:</strong> {user.subscription_plan.toUpperCase()}</p>
        <p><strong>Requests Used:</strong> {userRequestCount}/{user.monthly_credit_limit}</p>
        <p><strong>Plan Renews In:</strong> {daysUntilRenewal} days</p>
      </div>
      <div class="upgrade-section">
        {#if user.subscription_plan !== 'pro'}
          <a href={upgradeLink} class="upgrade-button" target="_blank" rel="noopener noreferrer">Upgrade to {getNextPlan(user.subscription_plan).toUpperCase()}</a>
        {:else}
          <a href="mailto:upgrade@whowhywhen.com" class="upgrade-button">Contact to Upgrade</a>
        {/if}
      </div>
    {/if}
  </section>
  
  <style>
    .user-settings {
      padding: 40px 20px;
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      max-width: 600px;
      margin: 40px auto;
    }
  
    .user-info {
      margin-bottom: 20px;
    }
  
    .user-info p {
      margin: 5px 0;
    }
  
    .upgrade-section {
      text-align: center;
    }
  
    .upgrade-button {
      display: inline-block;
      padding: 10px 20px;
      background-color: #ff4500;
      color: #fff;
      border-radius: 5px;
      text-decoration: none;
      font-size: 1rem;
      font-weight: bold;
      transition: background 0.3s;
    }
  
    .upgrade-button:hover {
      background-color: #ff6347;
    }
  </style>
  