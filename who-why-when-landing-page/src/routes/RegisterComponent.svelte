<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import Toast from '../components/Toast.svelte';
  import { DASH_API_BASE_URL, API_BASE_URL, GOOGLE_CLIENT_ID } from '../config';
  import { navigate } from 'svelte-routing';

  let name = '';
  let email = '';
  let password = '';
  let retypePassword = '';
  let project_name = '';
  let toastMessage = '';
  let toastType = '';
  const dispatch = createEventDispatcher();

  onMount(() => {
      initializeGoogleSignIn();
  });

  function initializeGoogleSignIn() {
    google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID, 
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

  async function handleSubmit() {

      if (password.length < 8 || !/[0-9]/.test(password)) {
          showToast('Password must be at least 8 characters long and include a number', 'error');
          return;
      }

      if (password !== retypePassword) {
          showToast('Passwords do not match', 'error');
          return;
      }

      const response = await fetch(`${DASH_API_BASE_URL}/dashauth/register`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              name,
              email,
              password,
              project_name
          })
      });

      if (response.ok) {
          const data = await response.json();
          showToast('Registration successful! Redirecting to login...', 'success');
          setTimeout(() => {
              dispatch('register', data);
              navigate('/login');
          }, 2000);
      } else {
          const errorData = await response.json();
          showToast(errorData.detail || 'Registration failed!', 'error');
      }
  }

  function showToast(message, type) {
      toastMessage = message;
      toastType = type;
      setTimeout(() => {
          toastMessage = '';
          toastType = '';
      }, 5000); 
  }
</script>

<section class="register-section">
  <div class="container">
      <h2>Create Your Account</h2>
      <div id="buttonDiv" class="google-signin-btn"></div>
      <p class="hint">Fill in the details below to create your account.</p>
      <form on:submit|preventDefault={handleSubmit}>
          <div class="form-group">
              <label for="name">Name</label>
              <input type="text" id="name" bind:value={name} placeholder="Enter your full name" required />
          </div>
          <div class="form-group">
              <label for="email">Email</label>
              <input type="email" id="email" bind:value={email} placeholder="Enter your email address" required />
          </div>
          <div class="form-group">
              <label for="password">Password</label>
              <input type="password" id="password" bind:value={password} placeholder="Create a password" required />
              <small>Password must be at least 8 characters long and include a number.</small>
          </div>
          <div class="form-group">
              <label for="retypePassword">Retype Password</label>
              <input type="password" id="retypePassword" bind:value={retypePassword} placeholder="Retype your password" required />
          </div>
          <div class="form-group">
              <label for="project_name">Default Project Name</label>
              <input type="text" id="project_name" bind:value={project_name} placeholder="Enter your default project name" required />
          </div>
          <button type="submit" class="btn-primary">Register</button>
      </form>
  </div>
</section>

{#if toastMessage}
  <Toast message={toastMessage} type={toastType} />
{/if}

<style>
  .register-section {
      padding: 80px 0;
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

  small {
      display: block;
      margin-top: 5px;
      color: #888;
  }

  .google-signin-btn {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
</style>
