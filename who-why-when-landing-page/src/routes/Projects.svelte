<script>
    import { onMount } from 'svelte';
    import { currentView } from '../stores/viewStore';
    import { isLoggedIn, clearToken } from '../stores/userStore';
    import { createEventDispatcher } from 'svelte';
    import Toast from '../components/Toast.svelte';
  
    let projects = [];
    let apiKeys = [];
    let newProjectName = '';
    let newApiKeyName = '';
    let showApiKeysModal = false;
    let selectedProjectId = null;
    let toastMessage = '';
    let toastType = '';
  
    const dispatch = createEventDispatcher();
  
    onMount(async () => {
      await fetchProjects();
    });
  
    async function fetchProjects() {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/auth/users/me/projects', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        projects = await response.json();
      } else {
        showToast('Failed to fetch projects', 'error');
      }
    }
  
    async function createProject() {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/auth/users/me/projects?project_name=${newProjectName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        newProjectName = '';
        await fetchProjects();
        showToast('Project created successfully', 'success');
      } else {
        showToast('Failed to create project', 'error');
      }
    }
  
    async function fetchApiKeys(projectId) {
      selectedProjectId = projectId;
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/apikeys?user_project_id=${projectId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        apiKeys = await response.json();
        showApiKeysModal = true;
      } else {
        showToast('Failed to fetch API keys', 'error');
      }
    }
  
    async function createApiKey() {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/apikeys?user_project_id=${selectedProjectId}&name=${newApiKeyName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        newApiKeyName = '';
        await fetchApiKeys(selectedProjectId);
        showToast('API key created successfully', 'success');
      } else {
        showToast('Failed to create API key', 'error');
      }
    }
  
    async function deleteApiKey(keyId) {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/apikeys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        await fetchApiKeys(selectedProjectId);
        showToast('API key deleted successfully', 'success');
      } else {
        showToast('Failed to delete API key', 'error');
      }
    }
  
    async function testApiKey(apiKey) {
      const response = await fetch('http://localhost:8000/api/log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-KEY': apiKey
        },
        body: JSON.stringify({
          endpoint: '/test',
          ip_address: '<Source IP>',
          request_info: 'WhoWhyWhen Test',
          location: '<>'
        })
      });
      if (response.ok) {
        showToast('Test request successful', 'success');
      } else {
        showToast('Test request failed', 'error');
      }
    }
  
    function blurApiKey(apiKey, show) {
      return show ? apiKey : apiKey.slice(0, -4).replace(/./g, '*') + apiKey.slice(-4);
    }
  
    function logout() {
      clearToken();
      currentView.set('home');
    }
  
    function showToast(message, type) {
      toastMessage = message;
      toastType = type;
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
          <button class="btn-primary" on:click={() => fetchApiKeys(project.id)}>View API Keys</button>
        </li>
      {/each}
    </ul>
  
    <h3>Create New Project</h3>
    <input type="text" bind:value={newProjectName} placeholder="Project Name" class="input-field" />
    <button class="btn-primary" on:click={createProject}>Create Project</button>
  
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
          <div class="create-api-key">
            <input type="text" bind:value={newApiKeyName} placeholder="API Key Name" class="input-field" />
            <button class="btn-primary" on:click={createApiKey}>Create New API Key</button>
          </div>
        </div>
      </div>
    {/if}
  </div>
  
  {#if toastMessage}
    <Toast message={toastMessage} type={toastType} />
  {/if}
  
  <style>
    .projects-container {
      padding: 20px;
      max-width: 800px;
      margin: 0 auto;
      background-color: #f9f9f9;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
  
    h2, h3 {
      color: #663399;
    }
  
    .btn-back {
      background-color: #ff4000;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      margin-bottom: 20px;
    }
  
    .project-list, .api-keys-list {
      list-style: none;
      padding: 0;
    }
  
    .project-item, .api-key-item {
      background-color: #fff;
      padding: 15px;
      border-radius: 5px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
    }
  
    .btn-primary, .btn-secondary {
      background-color: #663399;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
  
    .btn-secondary {
      background-color: #ff4000;
    }
  
    .input-field {
      width: calc(100% - 22px);
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 5px;
      margin-bottom: 10px;
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
      background-color: rgba(0, 0, 0, 0.4);
    }
  
    .modal-content {
      background-color: #fff;
      margin: 15% auto;
      padding: 20px;
      border: 1px solid #888;
      width: 80%;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
  
    .close {
      color: #aaa;
      float: right;
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
    }
  
    .api-key-actions {
      display: flex;
      gap: 10px;
    }
  
    .create-api-key {
      margin-top: 10px;
    }
  </style>
  