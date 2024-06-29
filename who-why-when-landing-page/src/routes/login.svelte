<script>
  import { createEventDispatcher } from 'svelte';

  let username = '';
  let password = '';
  const dispatch = createEventDispatcher();

  async function handleSubmit() {
    const response = await fetch('/auth/token', {
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
      dispatch('login', data);
      alert('Login successful!');
    } else {
      alert('Login failed!');
    }
  }
</script>

<section class="login-section">
  <div class="container">
    <h2>Login to Your Account</h2>
    <p class="hint">Please enter your username and password to access your account.</p>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" bind:value={username} placeholder="Enter your username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" bind:value={password} placeholder="Enter your password" required />
      </div>
      <button type="submit" class="btn-primary">Login</button>
    </form>
  </div>
</section>

<style>
  .login-section {
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
    transition: background-color 0.3s;
    margin-top: 20px;
  }

  .btn-primary:hover {
    background-color: #552288;
  }
</style>
