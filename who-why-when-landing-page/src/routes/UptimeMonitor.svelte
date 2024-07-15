<script>
    import { onMount } from 'svelte';
    import { selectedProjectIdStore } from '../stores/userStore'; 
    import { createEventDispatcher } from 'svelte';
    import Toast from '../components/Toast.svelte';
    import Modal from '../components/Modal.svelte';
    import { DASH_API_BASE_URL } from '../config'; // Import the base URL
  
    let monitors = [];
    let projects = [];
    let selectedProjectId = null;
    let toastMessage = '';
    let toastType = '';
    let showToast = false;
    let showModal = false;
    let isEditing = false;
    let monitorToEdit = null;
  
    let newMonitorName = '';
    let newMonitorUrl = '';
    let newMonitorType = 'http';
    let newMonitorInterval = 5;
  
    const dispatch = createEventDispatcher();
  
    onMount(async () => {
      selectedProjectIdStore.subscribe(async value => {
        selectedProjectId = value;
        await fetchProjects();
        if (selectedProjectId) {
          fetchMonitors();
        } else if (projects.length > 0) {
          selectedProjectId = projects[0].id;
          selectedProjectIdStore.set(selectedProjectId);
          fetchMonitors();
        }
      });
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
  
    async function createOrUpdateMonitor() {
      if (!selectedProjectId) {
        showToastMessage('Please select a project', 'error');
        return;
      }

      const token = localStorage.getItem('token');
      const endpoint = isEditing
        ? `${DASH_API_BASE_URL}/dashapi/monitors/${monitorToEdit.id}`
        : `${DASH_API_BASE_URL}/dashapi/projects/${selectedProjectId}/monitors`;
      const method = isEditing ? 'PUT' : 'POST';

      const response = await fetch(endpoint, {
        method: method,
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
        showModal = false;
        await fetchMonitors();
        showToastMessage(`Monitor ${isEditing ? 'updated' : 'created'} successfully`, 'success');
      } else {
        showToastMessage(`Failed to ${isEditing ? 'update' : 'create'} monitor`, 'error');
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

    function openCreateModal() {
      newMonitorName = '';
      newMonitorUrl = '';
      newMonitorType = 'http';
      newMonitorInterval = 5;
      isEditing = false;
      showModal = true;
    }

    function openEditModal(monitor) {
      monitorToEdit = monitor;
      newMonitorName = monitor.name;
      newMonitorUrl = monitor.url;
      newMonitorType = monitor.type;
      newMonitorInterval = monitor.check_interval;
      isEditing = true;
      showModal = true;
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
      <button class="btn-add" on:click={openCreateModal}>+</button>
      <ul class="monitor-list">
        {#each monitors as monitor}
          <li class="monitor-item">
            <div class="monitor-details" on:click={() => openEditModal(monitor)}>
              <span class="monitor-name">{monitor.name}</span>
              <span class="monitor-url">{monitor.url}</span>
              <span class="monitor-status">{monitor.status}</span>
            </div>
            <button class="edit-btn" on:click={() => openEditModal(monitor)}>
              ✏️
            </button>
          </li>
        {/each}
      </ul>
    {/if}
  
    {#if showToast}
      <Toast message={toastMessage} type={toastType} />
    {/if}
  
    {#if showModal}
      <Modal on:close={() => showModal = false}>
        <h3>{isEditing ? 'Edit Monitor' : 'Create New Monitor'}</h3>
        <input type="text" bind:value={newMonitorName} placeholder="Monitor Name" class="input-field" />
        <input type="url" bind:value={newMonitorUrl} placeholder="Monitor URL" class="input-field" />
        <select bind:value={newMonitorType} class="input-field">
          <option value="http">HTTP</option>
          <option value="https">HTTPS</option>
          <option value="ping">Ping</option>
        </select>
        <input type="number" bind:value={newMonitorInterval} placeholder="Check Interval (minutes)" class="input-field" />
        <button class="btn-primary" on:click={createOrUpdateMonitor}>{isEditing ? 'Update Monitor' : 'Create Monitor'}</button>
      </Modal>
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
      position: relative;
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
      cursor: pointer;
      position: relative;
    }
  
    .monitor-item:hover {
      transform: translateY(-5px);
      box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }
  
    .monitor-details {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 90%;
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
  
    .btn-add {
      position: absolute;
      top: 20px;
      right: 20px;
      background-color: #663399;
      color: #fff;
      border: none;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      font-size: 24px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    .btn-add:hover {
      background-color: #7d42a6;
    }
    
    .edit-btn {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 16px;
      margin-left: 10px;
    }

    .edit-btn:hover {
      color: #663399;
    }
  </style>
