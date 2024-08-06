<script>
  import { createEventDispatcher } from 'svelte';
  import Toast from '../components/Toast.svelte';
  import { DASH_API_BASE_URL } from '../config';

  let oldPassword = '';
  let newPassword = '';
  let retypeNewPassword = '';
  let toastMessage = '';
  let toastType = '';
  const dispatch = createEventDispatcher();

  async function handleChangePassword() {
      if (newPassword.length < 8 || !/[0-9]/.test(newPassword)) {
          showToast('New password must be at least 8 characters long and include a number', 'error');
          return;
      }

      if (newPassword !== retypeNewPassword) {
          showToast('Passwords do not match', 'error');
          return;
      }

      const token = localStorage.getItem('token');
      const response = await fetch(`${DASH_API_BASE_URL}/dashauth/change-password`, {
          method: 'POST',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              old_password: oldPassword,
              new_password: newPassword
          })
      });

      if (response.ok) {
          showToast('Password changed successfully!', 'success');
          dispatch('close');
      } else {
          const data = await response.json();
          showToast(data.detail || 'Password change failed', 'error');
      }
  }

  function showToast(message, type) {
      toastMessage = message;
      toastType = type;
  }
</script>

<div class="popup">
  <div class="popup-content">
      <h2>Change Password</h2>
      <form on:submit|preventDefault={handleChangePassword}>
          <div class="form-group">
              <label for="oldPassword">Old Password</label>
              <input type="password" id="oldPassword" bind:value={oldPassword} required />
          </div>
          <div class="form-group">
              <label for="newPassword">New Password</label>
              <input type="password" id="newPassword" bind:value={newPassword} required />
              <small>Password must be at least 8 characters long and include a number.</small>
          </div>
          <div class="form-group">
              <label for="retypeNewPassword">Retype New Password</label>
              <input type="password" id="retypeNewPassword" bind:value={retypeNewPassword} required />
          </div>
          <div class="form-actions">
              <button type="submit" class="btn-primary">Change Password</button>
              <button type="button" class="btn-secondary" on:click={() => dispatch('close')}>Cancel</button>
          </div>
      </form>
  </div>
</div>

{#if toastMessage}
  <Toast message={toastMessage} type={toastType} />
{/if}

<style>
  .popup {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
  }

  .popup-content {
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      max-width: 400px;
      width: 100%;
  }

  .form-group {
      margin-bottom: 20px;
  }

  label {
      display: block;
      margin-bottom: 8px;
      font-weight: bold;
  }

  input {
      width: 100%;
      padding: 12px;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 1rem;
  }

  small {
      display: block;
      margin-top: 5px;
      color: #888;
  }

  .form-actions {
      display: flex;
      justify-content: space-between;
  }

  .btn-primary {
      background-color: #663399;
      color: #fff;
      padding: 12px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.3s;
  }

  .btn-primary:hover {
      background-color: #552288;
  }

  .btn-secondary {
      background-color: #ccc;
      color: #333;
      padding: 12px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.3s;
  }

  .btn-secondary:hover {
      background-color: #bbb;
  }
</style>
