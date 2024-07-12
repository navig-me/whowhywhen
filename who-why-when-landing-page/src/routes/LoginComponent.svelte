<script>
  import { createEventDispatcher } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { setToken } from '../stores/userStore';
  import Toast from '../components/Toast.svelte';
  import { DASH_API_BASE_URL } from '../config'; // Import the base URL

  let username = '';
  let password = '';
  let twoFactorCode = '';
  let toastMessage = '';
  let toastType = '';
  let showTwoFactorInput = false;
  const dispatch = createEventDispatcher();

  async function handleSubmit() {
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username,
        password,
        grant_type: 'password'
      })
    });

    if (response.ok) {
      const data = await response.json();
      if (data.totp_required) {
        showTwoFactorInput = true;
      } else {
        setToken(data.access_token); // Save the token
        showToast('Login successful!', 'success');
        currentView.set('dashboard');
      }
    } else {
      showToast('Login failed!', 'error');
    }
  }

  async function handleTwoFactorSubmit() {
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/verify-2fa`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_email: username,
        token: twoFactorCode
      })
    });

    if (response.ok) {
      const data = await response.json();
      setToken(data.access_token); // Save the token
      showToast('Login successful!', 'success');
      currentView.set('dashboard');
    } else {
      showToast('2FA verification failed!', 'error');
    }
  }

  function showToast(message, type) {
    toastMessage = message;
    toastType = type;
  }
</script>

<section class="login-section">
  <div class="container">
    <h2>Login to Your Account</h2>
    <p class="hint">Please enter your username and password to access your account.</p>
    <form on:submit|preventDefault={showTwoFactorInput ? handleTwoFactorSubmit : handleSubmit}>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" bind:value={username} placeholder="Enter your username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" bind:value={password} placeholder="Enter your password" required />
      </div>
      {#if showTwoFactorInput}
        <div class="form-group">
          <label for="twoFactorCode">2FA Code</label>
          <input type="text" id="twoFactorCode" bind:value={twoFactorCode} placeholder="Enter your 2FA code" required />
        </div>
      {/if}
      <button type="submit" class="btn-primary">{showTwoFactorInput ? 'Verify 2FA' : 'Login'}</button>
    </form>
    <p class="support-message">If you face any issues, please contact <a href="mailto:support@whowhywhen.com">support@whowhywhen.com</a></p>
  </div>
</section>

{#if toastMessage}
  <Toast message={toastMessage} type={toastType} />
{/if}

<style>
  .login-section {
    padding: 150px 0;
    text-align: center;
    background: linear-gradient(135deg, #663399, #ff4000);
    color: #fff;
  }

  .container {
    max-width: 400px;
    margin: 0 auto;
    background: #fff;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    text-align: left;
  }

  h2 {
    margin-bottom: 20px;
    color: #663399;
    text-align: center;
  }

  .hint {
    margin-bottom: 20px;
    color: #888;
    text-align: center;
  }

  .form-group {
    margin-bottom: 20px;
  }

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #333;
  }

  input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1rem;
  }

  input::placeholder {
    color: #aaa;
  }

  .btn-primary {
    width: 100%;
    background-color: #663399;
    color: #fff;
    padding: 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s;
    margin-top: 20px;
  }

  .btn-primary:hover {
    background-color: #552288;
  }

  .support-message {
    margin-top: 20px;
    color: #888;
    text-align: center;
  }

  .support-message a {
    color: #00aaff;
    text-decoration: none;
  }

  .support-message a:hover {
    text-decoration: underline;
  }
</style>
