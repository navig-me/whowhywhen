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
      <h2>Login</h2>
      <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" bind:value={username} required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" bind:value={password} required />
        </div>
        <button type="submit" class="btn-primary">Login</button>
      </form>
    </div>
  </section>
  
  <style>
    .login-section {
      padding: 60px 0;
      text-align: center;
      background: #f9f9f9;
    }
  
    .container {
      max-width: 600px;
      margin: 0 auto;
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
  
    h2 {
      margin-bottom: 20px;
    }
  
    .form-group {
      margin-bottom: 20px;
      text-align: left;
    }
  
    label {
      display: block;
      margin-bottom: 5px;
    }
  
    input {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
  
    .btn-primary {
      background-color: #663399;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s;
    }
  
    .btn-primary:hover {
      background-color: #552288;
    }
  </style>
  