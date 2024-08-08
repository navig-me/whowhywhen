<script>
  import { onMount } from 'svelte';
  import { clearToken, isLoggedIn } from '../stores/userStore';
  import { DASH_API_BASE_URL } from '../config';
  import ChangePasswordPopup from './ChangePasswordPopup.svelte';
  import QRCode from 'qrcode';

  let user = null;
  let upgradeLink = '';
  let customerPortalLink = '';
  let daysUntilRenewal = 0;
  let userRequestCount = 0;
  let showChangePasswordPopup = false;
  let showEnable2FAPopup = false;
  let totpUri = '';
  let qrCodeUrl = '';
  let current2FAToken = '';
  let showPricing = false; // State to show/hide pricing section

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
      customerPortalLink = await fetchCustomerPortalLink(token);
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

  async function fetchCustomerPortalLink(token) {
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/stripe/customer-portal`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      return data || '';
    }
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
      const data = await response.json();
      return data || '';
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

  function openChangePasswordPopup() {
    showChangePasswordPopup = true;
  }

  function closeChangePasswordPopup() {
    showChangePasswordPopup = false;
  }

  async function enable2FA() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/get-2fa-qr-code`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      totpUri = data.totp_uri;
      qrCodeUrl = await QRCode.toDataURL(totpUri);
      showEnable2FAPopup = true;
    } else {
      alert('Failed to enable 2FA');
    }
  }

  async function verifyAndEnable2FA() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/enable-2fa`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ token: current2FAToken })
    });

    if (response.ok) {
      await fetchUserDetails();
      showEnable2FAPopup = false;
      alert('2FA enabled successfully');
    } else {
      alert('Failed to verify 2FA token');
    }
  }

  async function disable2FA() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/disable-2fa`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      await fetchUserDetails();
      alert('2FA disabled successfully');
    } else {
      alert('Failed to disable 2FA');
    }
  }

  function closeEnable2FAPopup() {
    showEnable2FAPopup = false;
  }

  function togglePricing() {
    showPricing = !showPricing;
  }
</script>

<section class="user-settings">
  {#if user}
    <h2>User Settings</h2>
    <div class="user-card">
      <div class="user-info">
        <div class="user-details">
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
        <a href="javascript:void(0);" class="btn-link" on:click={openChangePasswordPopup}>Change Password</a>
      </div>
      <hr>
      <div class="plan-info">
        <h3>Subscription Plan</h3>
        <div class={`subscription-card ${user.subscription_plan}`}>
          <h4>{user.subscription_plan.toUpperCase()} Plan</h4>
          <p>Requests Used: {userRequestCount}/{user.monthly_credit_limit}</p>
          <p>Renews In: {daysUntilRenewal} days</p>
        </div>
        {#if user.subscription_plan !== 'pro'}
          <a href={upgradeLink} class="btn-link" target="_blank" rel="noopener noreferrer">Upgrade to {getNextPlan(user.subscription_plan).toUpperCase()}</a>
        {/if}
        {#if user.subscription_plan !== 'free'}
          <a href={customerPortalLink} class="btn-link manage-subscription" target="_blank" rel="noopener noreferrer">Manage Subscription</a>
        {/if}
        <button class="accordion-toggle" on:click={togglePricing}>
          <i class="fas fa-chevron-down"></i> {showPricing ? 'Hide Pricing' : 'Show Pricing'}
        </button>
        {#if showPricing}
          <div class="accordion">
            <div class="accordion-content">
              <div class="plans">
                <div class="plan free-plan">
                  <h3>FREE</h3>
                  <p>20,000 monthly calls</p>
                  <p>In-App & Browser Alerts</p>
                  <p>All Analytics</p>
                  <p class="price">$0</p>
                </div>
                <div class="plan starter-plan">
                  <h3>STARTER</h3>
                  <p>250,000 monthly calls</p>
                  <p>In-App, Browser & Email Alerts</p>
                  <p>All Analytics</p>
                  <p class="price">$9</p>
                </div>
                <div class="plan pro-plan">
                  <h3>PRO</h3>
                  <p>5,000,000 monthly calls</p>
                  <p>In-App, Browser & Email Alerts</p>
                  <p>All Analytics</p>
                  <p>Priority Support</p>
                  <p class="price">$39</p>
                </div>
              </div>
            </div>
          </div>
        {/if}
      </div>
      <hr>
      <div class="security-info">
        <h3>Security</h3>
        {#if !user.two_factor_enabled}
          <a href="javascript:void(0);" class="btn-link" on:click={enable2FA}>Enable 2FA</a>
        {:else}
          <a href="javascript:void(0);" class="btn-link" on:click={disable2FA}>Disable 2FA</a>
        {/if}
      </div>
      <hr>
      <div class="support-info">
          <h3>Have Feedback or Need Help?</h3>
          <p>Click here to <a href="mailto:support@whowhywhen.com">contact support</a> at support@whowhywhen.com</p>
      </div>
    </div>
  {/if}
</section>

{#if showChangePasswordPopup}
<ChangePasswordPopup on:close={closeChangePasswordPopup} />
{/if}

{#if showEnable2FAPopup}
<div class="enable-2fa-popup">
  <div class="popup-content">
    <h3>Scan the QR Code</h3>
    <img src={qrCodeUrl} alt="2FA QR Code">
    <p>Use your authenticator app to scan the QR code and complete the 2FA setup.</p>
    <input type="text" placeholder="Enter current 2FA code" bind:value={current2FAToken} />
    <button class="btn-primary" on:click={verifyAndEnable2FA}>Verify and Enable 2FA</button>
    <button class="btn-secondary" on:click={closeEnable2FAPopup}>Close</button>
  </div>
</div>
{/if}

<style>
.user-settings {
  padding: 60px 20px;
  background: linear-gradient(135deg, #f5f7fa, #e9eff6);
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  font-size: 2rem;
  color: #333;
}

.user-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  padding: 30px;
  max-width: 100%;
  margin: 0 auto;
  text-align: left;
}

.user-info, .plan-info, .security-info, .support-info {
  margin-bottom: 20px;
}

hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 20px 0;
}

.user-details p, .plan-info p, .security-info p {
  margin: 10px 0;
  font-size: 1rem;
  color: #555;
}

.btn-link {
  display: inline-block;
  color: #663399;
  text-decoration: none;
  font-size: 0.9rem;
  margin-top: 10px;
  cursor: pointer;
  transition: color 0.3s;
}

.btn-link:hover {
  color: #552288;
  text-decoration: underline !important;
}

.btn-primary, .btn-secondary {
  display: inline-block;
  background-color: #663399;
  color: #fff !important;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s, box-shadow 0.3s;
  text-align: center;
  margin-top: 10px;
}

.btn-secondary {
  background-color: #ccc;
}

.btn-primary:hover {
  background-color: #552288;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.manage-subscription {
  display: block;
  margin-top: 20px;
}

.accordion-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  background-color: #f5f7fa;
  border: none;
  color: #663399;
  font-size: 1rem;
  padding: 10px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s;
}

.accordion-toggle:hover {
  background-color: #e9eff6;
}

.accordion-toggle i {
  margin-right: 5px;
}

.popup-content h3 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.popup-content img {
  width: 100%;
  max-width: 200px;
  margin-bottom: 20px;
}

@media (min-width: 768px) {
  .user-card {
    max-width: 800px;
  }
}

.enable-2fa-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-content {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  max-width: 400px;
}

/* Accordion styles */
.accordion {
  margin-top: 20px;
  width: 100%;
}

.accordion-content {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.plans {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.plan {
  flex: 1 1 calc(33.33% - 20px); /* Adjust the width to fit 3 cards in a row */
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.plan.free-plan {
  border-left: 5px solid #043d16; 
}

.plan.starter-plan {
  border-left: 5px solid #663399; 
}

.plan.pro-plan {
  border-left: 5px solid #ff4500; 
}

.plan h3 {
  margin-bottom: 10px;
  font-size: 1.5rem;
  color: #333;
}

.plan p {
  margin-bottom: 10px;
  font-size: 1rem;
  color: #555;
}

.plan .price {
  margin-top: 10px;
  font-size: 1.5rem;
  color: #333;
  font-weight: bold;
}

/* Subscription Card */
.subscription-card {
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  color: #fff;
  text-align: center;
}

.subscription-card.free {
  background-color: #043d16; 
}

.subscription-card.starter {
  background-color: #663399; 
}

.subscription-card.pro {
  background-color: #ff4500; 
}

.subscription-card h4 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
}

.subscription-card p {
  margin: 10px 0 0;
  font-size: 1rem;
  color: #fff;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .plan {
    flex: 1 1 100%; /* 100% width on small screens */
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .plan {
    flex: 1 1 calc(50% - 20px); /* 50% width on medium screens */
  }
}
</style>
