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
        return data.url || '';
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
        return data.url || '';
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
      const response = await fetch(`${DASH_API_BASE_URL}/dashauth/enable-2fa`, {
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
          <button class="btn-primary change-password" on:click={openChangePasswordPopup}>Change Password</button>
        </div>
        <div class="plan-info">
          <h3>Subscription Plan</h3>
          <p><strong>Plan:</strong> {user.subscription_plan.toUpperCase()}</p>
          <p><strong>Requests Used:</strong> {userRequestCount}/{user.monthly_credit_limit}</p>
          <p><strong>Plan Renews In:</strong> {daysUntilRenewal} days</p>
          {#if user.subscription_plan !== 'pro'}
            <a href={upgradeLink} class="btn-upgrade" target="_blank" rel="noopener noreferrer">Upgrade to {getNextPlan(user.subscription_plan).toUpperCase()}</a>
          {:else}
            <a href="mailto:upgrade@whowhywhen.com" class="btn-upgrade">Contact to Upgrade</a>
          {/if}
          {#if user.subscription_plan !== 'free'}
            <a href={customerPortalLink} class="btn-customerportal" target="_blank" rel="noopener noreferrer">Manage Subscription</a>
          {/if}
          {#if !user.two_factor_enabled}
            <button class="btn-primary enable-2fa" on:click={enable2FA}>Enable 2FA</button>
          {:else}
            <button class="btn-primary disable-2fa" on:click={disable2FA}>Disable 2FA</button>
          {/if}
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
      <button class="btn-primary" on:click={closeEnable2FAPopup}>Close</button>
    </div>
  </div>
{/if}

<style>
  .user-settings {
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa, #e9eff6);
    text-align: center;
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
    max-width: 800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .user-info, .plan-info {
    text-align: left;
  }

  .user-details p, .plan-info p {
    margin: 10px 0;
    font-size: 1rem;
    color: #555;
  }

  .btn-primary, .btn-upgrade, .btn-customerportal {
    display: inline-block;
    background-color: #663399;
    color: #fff;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s, box-shadow 0.3s;
    text-decoration: none;
    text-align: center;
  }

  .btn-primary:hover, .btn-upgrade:hover, .btn-customerportal:hover {
    background-color: #552288;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }

  .btn-upgrade {
    background-color: #ff4500;
  }

  .btn-upgrade:hover {
    background-color: #ff6347;
  }

  .btn-customerportal {
    background-color: #00aaff;
    margin-top: 10px;
  }

  .btn-customerportal:hover {
    background-color: #0099cc;
  }

  .change-password {
    margin-top: 20px;
    background-color: #ff4500;
  }

  .change-password:hover {
    background-color: #ff6347;
  }

  .plan-info h3 {
    font-size: 1.3rem;
    margin-bottom: 10px;
    color: #333;
  }

  @media (min-width: 768px) {
    .user-card {
      grid-template-columns: 1fr 1fr;
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

</style>
