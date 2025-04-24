<script>
  import { onMount } from 'svelte';
  import { clearToken, isLoggedIn } from '../stores/userStore';
  import { DASH_API_BASE_URL } from '../config';
  import ChangePasswordPopup from './ChangePasswordPopup.svelte';
  import QRCode from 'qrcode';

  let user = null;
  let userRequestCount = 0;
  let showChangePasswordPopup = false;
  let showEnable2FAPopup = false;
  let totpUri = '';
  let qrCodeUrl = '';
  let current2FAToken = '';

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
    } else if (response.status === 401) {
      clearToken();
    }
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

// Pricing function removed for open source version
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

/* Pricing styles removed for open source version */
</style>
