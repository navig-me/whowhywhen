<script>
    import { onMount } from 'svelte';
    import { currentView } from '../stores/viewStore';
    import { isLoggedIn } from '../stores/userStore';
    import { createEventDispatcher } from 'svelte';
  
    let projects = [];
    let apiKeys = [];
    let newProjectName = '';
    let showApiKeysModal = false;
    let selectedProjectId = null;
  
    const dispatch = createEventDispatcher();
  
    onMount(async () => {
      await fetchProjects();
    });
  
    async function fetchProjects() {
      const response = await fetch('http://localhost:8000/auth/users/me/projects', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        projects = await response.json();
      } else {
        console.error('Failed to fetch projects');
      }
    }
  
    async function createProject() {
      const response = await fetch(`http://localhost:8000/auth/users/me/projects?project_name=${newProjectName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        newProjectName = '';
        await fetchProjects();
      } else {
        console.error('Failed to create project');
      }
    }
  
    async function fetchApiKeys(projectId) {
      selectedProjectId = projectId;
      const response = await fetch(`http://localhost:8000/api/apikeys?user_project_id=${projectId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        apiKeys = await response.json();
        showApiKeysModal = true;
      } else {
        console.error('Failed to fetch API keys');
      }
    }
  
    async function createApiKey() {
      const response = await fetch('http://localhost:8000/api/apikeys', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_project_id: selectedProjectId
        })
      });
      if (response.ok) {
        await fetchApiKeys(selectedProjectId);
      } else {
        console.error('Failed to create API key');
      }
    }
  
    async function deleteApiKey(keyId) {
      const response = await fetch(`http://localhost:8000/api/apikeys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        await fetchApiKeys(selectedProjectId);
      } else {
        console.error('Failed to delete API key');
      }
    }
  
    function blurApiKey(apiKey) {
      return apiKey.slice(0, -4).replace(/./g, '*') + apiKey.slice(-4);
    }
  
    function logout() {
      isLoggedIn.set(false);
      currentView.set('home');
    }
  </script>
  
  <template>
    <div>
      <h2>Your Projects</h2>
      <button on:click={() => currentView.set('dashboard')}>Back to Dashboard</button>
      <ul>
        {#each projects as project}
          <li>
            {project.name} {project.is_default ? '★' : ''}
            <button on:click={() => fetchApiKeys(project.id)}>View API Keys</button>
          </li>
        {/each}
      </ul>
  
      <h3>Create New Project</h3>
      <input type="text" bind:value={newProjectName} placeholder="Project Name" />
      <button on:click={createProject}>Create Project</button>
  
      {#if showApiKeysModal}
        <div class="modal">
          <div class="modal-content">
            <span class="close" on:click={() => showApiKeysModal = false}>&times;</span>
            <h3>API Keys</h3>
            <ul>
              {#each apiKeys as key}
                <li>
                  <span class="blurred">{blurApiKey(key.key)}</span>
                  <button on:click={() => deleteApiKey(key.id)}>Delete</button>
                  <button on:click={() => key.show = !key.show}>{key.show ? 'Hide' : 'Show'}</button>
                </li>
              {/each}
            </ul>
            <button on:click={createApiKey}>Create New API Key</button>
          </div>
        </div>
      {/if}
    </div>
  </template>
  
  <style>
    .modal {
      display: block;
      position: fixed;
      z-index: 1;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgb(0, 0, 0);
      background-color: rgba(0, 0, 0, 0.4);
    }
  
    .modal-content {
      background-color: #fefefe;
      margin: 15% auto;
      padding: 20px;
      border: 1px solid #888;
      width: 80%;
    }
  
    .close {
      color: #aaa;
      float: right;
      font-size: 28px;
      font-weight: bold;
    }
  
    .close:hover,
    .close:focus {
      color: black;
      text-decoration: none;
      cursor: pointer;
    }
  
    .blurred {
      filter: blur(4px);
    }
  </style>
  