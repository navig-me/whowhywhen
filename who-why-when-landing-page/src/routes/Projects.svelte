<script>
    import { onMount } from 'svelte';
    import { currentView } from '../stores/viewStore';
    import { isLoggedIn, clearToken } from '../stores/userStore';
    import { createEventDispatcher } from 'svelte';
    import Toast from '../components/Toast.svelte';
    import { API_BASE_URL } from '../config'; // Import the base URL

    let projects = [];
    let apiKeys = [];
    let newProjectName = '';
    let newApiKeyName = '';
    let showApiKeysModal = false;
    let selectedProjectId = null;
    let toastMessage = '';
    let toastType = '';
    let showToast = false;
    let clientIp = '';
    let clientLocation = {};

    const dispatch = createEventDispatcher();

    onMount(async () => {
      await fetchProjects();
      await fetchIpLocation();
    });

    async function fetchProjects() {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/auth/users/me/projects`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        projects = await response.json();
      } else {
        showToastMessage('Failed to fetch projects', 'error');
      }
    }

    async function fetchIpLocation() {
      const response = await fetch(`${API_BASE_URL}/api/ip-location`);
      if (response.ok) {
        const data = await response.json();
        clientIp = data.ip;
      } else {
        showToastMessage('Failed to fetch IP and location info', 'error');
      }
    }

    async function createProject() {
      if (projects.length >= 10) {
        showToastMessage('You have reached the maximum number of projects', 'error');
        return;
      }
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/auth/users/me/projects?project_name=${newProjectName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        newProjectName = '';
        await fetchProjects();
        showToastMessage('Project created successfully', 'success');
      } else {
        const errorData = await response.json();
        showToastMessage(errorData.detail || 'Failed to create project', 'error');
      }
    }

    async function fetchApiKeys(projectId) {
      selectedProjectId = projectId;
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/apikeys?user_project_id=${projectId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        apiKeys = await response.json();
        showApiKeysModal = true;
      } else {
        showToastMessage('Failed to fetch API keys', 'error');
      }
    }

    async function createApiKey() {
      if (apiKeys.length >= 3) {
        showToastMessage('You have reached the maximum number of API keys for this project', 'error');
        return;
      }
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/apikeys?user_project_id=${selectedProjectId}&name=${newApiKeyName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        newApiKeyName = '';
        await fetchApiKeys(selectedProjectId);
        showToastMessage('API key created successfully', 'success');
      } else {
        const errorData = await response.json();
        showToastMessage(errorData.detail || 'Failed to create API key', 'error');
      }
    }

    async function deleteApiKey(keyId) {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/apikeys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        await fetchApiKeys(selectedProjectId);
        showToastMessage('API key deleted successfully', 'success');
      } else {
        showToastMessage('Failed to delete API key', 'error');
      }
    }

    async function testApiKey(apiKey) {
      const response = await fetch(`${API_BASE_URL}/api/log`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-KEY': apiKey
        },
        body: JSON.stringify({
          url: 'www.whowhywhen.com/whowhywhen-test?q=test',
          ip_address: clientIp,
          user_agent: 'WhoWhyWhen Test',
          response_code: 200
        })
      });
      if (response.ok) {
        showToastMessage('Test request successful', 'success');
      } else {
        showToastMessage('Test request failed', 'error');
      }
    }

    function blurApiKey(apiKey, show) {
      return show ? apiKey : apiKey.slice(0, -4).replace(/./g, '*') + apiKey.slice(-4);
    }

    function logout() {
      clearToken();
      currentView.set('home');
    }

    function showToastMessage(message, type) {
      toastMessage = message;
      toastType = type;
      showToast = false; // Reset the toast visibility to force re-render
      setTimeout(() => {
        showToast = true;
      }, 0);
    }

    function viewDashboard(projectId) {
      selectedProjectId = projectId;
      currentView.set('dashboard');
    }
  </script>
  
  <div class="projects-container">
    <h2>Your Projects</h2>
    <button class="btn-back" on:click={() => currentView.set('dashboard')}>Back to Dashboard</button>
    <ul class="project-list">
      {#each projects as project}
        <li class="project-item">
          <div class="project-details">
            <span class="project-name">{project.name}</span>
            {#if project.is_default}
              <span class="default-star">★</span>
            {/if}
          </div>
          <div class="project-actions">
            <button class="btn-primary" on:click={() => fetchApiKeys(project.id)}>View API Keys</button>
            <button class="btn-secondary" on:click={() => viewDashboard(project.id)}>View Dashboard</button>
          </div>
        </li>
      {/each}
    </ul>
  
    <h3>Create New Project</h3>
    <input type="text" bind:value={newProjectName} placeholder="Project Name" class="input-field" />
    <button class="btn-primary" on:click={createProject}>Create Project</button>
    {#if projects.length >= 10}
      <p>You have reached the maximum number of projects.</p>
    {/if}
  
    {#if showApiKeysModal}
      <div class="modal">
        <div class="modal-content">
          <span class="close" on:click={() => showApiKeysModal = false}>&times;</span>
          <h3>API Keys</h3>
          <ul class="api-keys-list">
            {#each apiKeys as key}
              <li class="api-key-item">
                <div class="api-key-details">
                  <span class="api-key-name">{key.name}</span>
                  <span class={key.show ? 'unblurred' : 'blurred'}>{blurApiKey(key.key, key.show)}</span>
                </div>
                <div class="api-key-actions">
                  <button class="btn-secondary" on:click={() => deleteApiKey(key.id)}>Delete</button>
                  <button class="btn-secondary" on:click={() => key.show = !key.show}>{key.show ? 'Hide' : 'Show'}</button>
                  <button class="btn-secondary" on:click={() => testApiKey(key.key)}>Test API</button>
                </div>
              </li>
            {/each}
          </ul>
          {#if apiKeys.length >= 3}
            <p>You have reached the maximum number of API keys for this project. Delete an existing API key to create a new one.</p>
          {/if}
          <div class="create-api-key">
            <input type="text" bind:value={newApiKeyName} placeholder="API Key Name" class="input-field" />
            <button class="btn-primary" on:click={createApiKey}>Create New API Key</button>
          </div>
        </div>
      </div>
    {/if}
  </div>
  
  {#if showToast}
    <Toast message={toastMessage} type={toastType} />
  {/if}
  
  <style>
    .projects-container {
      padding: 40px 20px;
      max-width: 900px;
      margin: 0 auto;
      background-color: #f9f9f9;
      border-radius: 10px;
      box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
      text-align: center;
    }
  
    h2, h3 {
      color: #663399;
      margin-bottom: 20px;
    }
  
    .btn-back {
      background-color: #ff4000;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      margin-bottom: 30px;
      transition: background-color 0.3s ease;
    }

    .btn-back:hover {
      background-color: #e63900;
    }
  
    .project-list, .api-keys-list {
      list-style: none;
      padding: 0;
      margin-bottom: 30px;
    }
  
    .project-item, .api-key-item {
      background-color: #fff;
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
  
    .project-item:hover, .api-key-item:hover {
      transform: translateY(-5px);
      box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }
  
    .project-details {
      display: flex;
      align-items: center;
    }
  
    .project-name {
      font-weight: bold;
      margin-right: 10px;
    }
  
    .default-star {
      color: #ff4000;
      font-size: 1.2rem;
    }

    .project-actions {
      display: flex;
      gap: 10px;
    }
  
    .btn-primary, .btn-secondary {
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.3s ease;
    }
  
    .btn-primary {
      background-color: #663399;
      color: #fff;
    }
  
    .btn-primary:hover {
      background-color: #7d42a6;
      transform: translateY(-2px);
    }
  
    .btn-secondary {
      background-color: #ff4000;
      color: #fff;
    }
  
    .btn-secondary:hover {
      background-color: #e63900;
      transform: translateY(-2px);
    }
  
    .input-field {
      width: calc(100% - 22px);
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 5px;
      margin-bottom: 20px;
    }
  
    .modal {
      display: block;
      position: fixed;
      z-index: 1;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.5);
    }
  
    .modal-content {
      background-color: #fff;
      margin: 10% auto;
      padding: 30px;
      border: 1px solid #888;
      width: 80%;
      max-width: 600px;
      border-radius: 10px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
      position: relative;
    }
  
    .close {
      color: #aaa;
      position: absolute;
      top: 15px;
      right: 20px;
      font-size: 28px;
      font-weight: bold;
      cursor: pointer;
    }
  
    .close:hover, .close:focus {
      color: black;
      text-decoration: none;
    }
  
    .blurred {
      filter: blur(4px);
    }
  
    .unblurred {
      filter: none;
    }
  
    .api-key-details {
      display: flex;
      align-items: center;
    }
  
    .api-key-name {
      margin-right: 10px;
      font-weight: bold;
    }
  
    .api-key-actions {
      display: flex;
      gap: 10px;
    }
  
    .create-api-key {
      margin-top: 20px;
    }
  </style>
