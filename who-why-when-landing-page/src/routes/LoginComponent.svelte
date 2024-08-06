<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { navigate } from 'svelte-routing';
  import { setToken } from '../stores/userStore';
  import Toast from '../components/Toast.svelte';
  import { DASH_API_BASE_URL } from '../config';

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
        setToken(data.access_token);
        gtag('set', 'user_id', data.user_id); // Set user ID in Google Analytics
        gtag('event', 'login', { method: 'Password' });
        showToast('Login successful!', 'success');
        setTimeout(() => {
          navigate('/dashboard');
        }, 1500); // Add a slight delay before redirecting
      }
    } else {
      showToast('Login failed!', 'error');
    }
  }

  async function handleTwoFactorSubmit() {
    if (!/^\d{6}$/.test(twoFactorCode)) {
      showToast('Invalid 2FA code. Please enter a 6-digit code.', 'error');
      return;
    }

    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/verify-2fa?user_email=${username}&token=${twoFactorCode}`, {
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
      setToken(data.access_token);
      gtag('set', 'user_id', data.user_id); // Set user ID in Google Analytics
      gtag('event', 'login', { method: '2FA' });
      showToast('Login successful!', 'success');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500); // Add a slight delay before redirecting
    } else {
      showToast('2FA verification failed!', 'error');
    }
  }

  function showToast(message, type) {
    toastMessage = message;
    toastType = type;
  }

  function initializeGoogleSignIn() {
    google.accounts.id.initialize({
      client_id: '209311359644-gj97vlisirrf64jc3cp11fpf2m8ojd61.apps.googleusercontent.com', // Replace with your Google client ID
      callback: handleGoogleSignIn
    });
    google.accounts.id.renderButton(
      document.getElementById('buttonDiv'),
      { theme: 'outline', size: 'large' }  // customization attributes
    );
    google.accounts.id.prompt(); // also display the One Tap dialog
  }

  async function handleGoogleSignIn(response) {
    const idToken = response.credential;

    const googleResponse = await fetch(`${DASH_API_BASE_URL}/dashauth/google-login?id_token=${idToken}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (googleResponse.ok) {
      const data = await googleResponse.json();
      setToken(data.access_token);
      gtag('set', 'user_id', data.user_id); // Set user ID in Google Analytics
      gtag('event', 'login', { method: 'Google' });
      showToast('Login successful!', 'success');
      if (data.new_user) {
        setTimeout(() => {
          navigate('/projects');
        }, 1500); // Add a slight delay before redirecting
      } else {
        setTimeout(() => {
          navigate('/dashboard');
        }, 1500); // Add a slight delay before redirecting
      }
    } else {
      showToast('Google login failed!', 'error');
    }
  }

  // Initialize Google Sign-In when the component is mounted
  onMount(() => {
    initializeGoogleSignIn();
  });
</script>

<section class="login-section">
  <div class="container">
    <h2>Login to Your Account</h2>
    <div id="buttonDiv" class="google-signin-btn"></div>
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
          <input type="text" id="twoFactorCode" bind:value={twoFactorCode} placeholder="Enter your 2FA code" maxlength="6" required />
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
    transition: background-color 0.3s, transform 0.3s;
    margin-top: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .btn-primary:hover {
    background-color: #552288;
    transform: translateY(-2px);
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

  .google-signin-btn {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
</style>
