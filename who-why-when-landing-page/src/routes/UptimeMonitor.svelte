<script>
    import { onMount } from 'svelte';
    import { selectedProjectIdStore, clearToken } from '../stores/userStore'; 
    import { createEventDispatcher } from 'svelte';
    import Toast from '../components/Toast.svelte';
    import { DASH_API_BASE_URL } from '../config'; // Import the base URL
  
    let monitors = [];
    let newMonitorName = '';
    let newMonitorUrl = '';
    let newMonitorType = 'http';
    let newMonitorInterval = 5;
    let projects = [];
    let selectedProjectId = null;
    let toastMessage = '';
    let toastType = '';
    let showToast = false;
  
    const dispatch = createEventDispatcher();
  
    onMount(async () => {
      selectedProjectIdStore.subscribe(value => {
        selectedProjectId = value;
        if (selectedProjectId) {
          fetchMonitors();
        }
      });
      await fetchProjects();
    });
  
    async function fetchProjects() {
      const token = localStorage.getItem('token');
      const response = await fetch(`${DASH_API_BASE_URL}/dashauth/users/me/projects`, {
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
  
    async function fetchMonitors() {
      if (!selectedProjectId) {
        showToastMessage('Please select a project', 'error');
        return;
      }
  
      const token = localStorage.getItem('token');
      const response = await fetch(`${DASH_API_BASE_URL}/dashapi/projects/${selectedProjectId}/monitors`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        monitors = await response.json();
      } else {
        showToastMessage('Failed to fetch monitors', 'error');
      }
    }
  
    async function createMonitor() {
      if (!selectedProjectId) {
        showToastMessage('Please select a project', 'error');
        return;
      }
  
      const token = localStorage.getItem('token');
      const response = await fetch(`${DASH_API_BASE_URL}/dashapi/projects/${selectedProjectId}/monitors`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: newMonitorName,
          url: newMonitorUrl,
          type: newMonitorType,
          check_interval: newMonitorInterval
        })
      });
      if (response.ok) {
        newMonitorName = '';
        newMonitorUrl = '';
        newMonitorType = 'http';
        newMonitorInterval = 5;
        await fetchMonitors();
        showToastMessage('Monitor created successfully', 'success');
      } else {
        showToastMessage('Failed to create monitor', 'error');
      }
    }
  
    function changeProject(event) {
      selectedProjectId = event.target.value;
      selectedProjectIdStore.set(selectedProjectId);
      fetchMonitors();
    }
  
    function showToastMessage(message, type) {
      toastMessage = message;
      toastType = type;
      showToast = false; // Reset the toast visibility to force re-render
      setTimeout(() => {
        showToast = true;
      }, 0);
    }
  </script>
  
  <section class="uptime-monitors">
    <h2>Uptime Monitors</h2>
    <select class="project-selector" on:change={changeProject}>
      <option value="">Select a Project</option>
      {#each projects as project}
        <option value={project.id} selected={project.id === selectedProjectId}>{project.name}</option>
      {/each}
    </select>
    {#if selectedProjectId}
      <ul class="monitor-list">
        {#each monitors as monitor}
          <li class="monitor-item">
            <div class="monitor-details">
              <span class="monitor-name">{monitor.name}</span>
              <span class="monitor-url">{monitor.url}</span>
              <span class="monitor-status">{monitor.status}</span>
            </div>
          </li>
        {/each}
      </ul>
    
      <h3>Create New Monitor</h3>
      <input type="text" bind:value={newMonitorName} placeholder="Monitor Name" class="input-field" />
      <input type="url" bind:value={newMonitorUrl} placeholder="Monitor URL" class="input-field" />
      <select bind:value={newMonitorType} class="input-field">
        <option value="http">HTTP</option>
        <option value="https">HTTPS</option>
        <option value="ping">Ping</option>
      </select>
      <input type="number" bind:value={newMonitorInterval} placeholder="Check Interval (minutes)" class="input-field" />
      <button class="btn-primary" on:click={createMonitor}>Create Monitor</button>
    {/if}
  
    {#if showToast}
      <Toast message={toastMessage} type={toastType} />
    {/if}
  </section>
  
  <style>
    .uptime-monitors {
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
  
    .project-selector {
      padding: 10px;
      margin-bottom: 20px;
      font-size: 1rem;
    }
  
    .monitor-list {
      list-style: none;
      padding: 0;
      margin-bottom: 30px;
    }
  
    .monitor-item {
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
  
    .monitor-item:hover {
      transform: translateY(-5px);
      box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }
  
    .monitor-details {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
  
    .monitor-name {
      font-weight: bold;
      margin-bottom: 5px;
    }
  
    .monitor-url {
      color: #888;
      margin-bottom: 5px;
    }
  
    .monitor-status {
      color: #28a745;
    }
  
    .input-field {
      width: calc(100% - 22px);
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 5px;
      margin-bottom: 20px;
    }
  
    .btn-primary {
      background-color: #663399;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    .btn-primary:hover {
      background-color: #7d42a6;
    }
  </style>
  