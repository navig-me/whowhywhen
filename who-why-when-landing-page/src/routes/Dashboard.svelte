<script>
  import { onMount } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { isLoggedIn, clearToken } from '../stores/userStore';
  import { createEventDispatcher } from 'svelte';
  import Toast from '../components/Toast.svelte';
  import { Bar } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  let projects = [];
  let selectedProjectId = null;
  let apiLogs = [];
  let toastMessage = '';
  let toastType = '';
  let currentPage = 1;
  let totalPages = 1;
  let logsPerPage = 10;
  let hourlyRequestsData = [];
  let chartData = null;
  let frequency = "hour";

  let searchParams = {};
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
      if (projects.length > 0) {
        selectedProjectId = projects[0].id;
        await fetchApiLogs();
        await fetchHourlyRequestsData();
      }
    } else {
      showToast('Failed to fetch projects', 'error');
    }
  }

  async function fetchApiLogs() {
    const token = localStorage.getItem('token');
    const response = await fetch(`http://localhost:8000/api/logs/project/${selectedProjectId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        page: currentPage,
        limit: logsPerPage,
        search_params: searchParams
      })
    });
    if (response.ok) {
      const data = await response.json();
      apiLogs = data.logs;
      totalPages = Math.ceil(data.total / logsPerPage);
    } else {
      showToast('Failed to fetch API logs', 'error');
    }
  }

  async function fetchHourlyRequestsData() {
    const token = localStorage.getItem('token');
    const response = await fetch(`http://localhost:8000/api/logs/project/stats/${selectedProjectId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        frequency: frequency,
        search_params: searchParams
      })
    });
    if (response.ok) {
      hourlyRequestsData = await response.json();
      updateChartData();
    } else {
      showToast('Failed to fetch hourly requests data', 'error');
    }
  }

  function showToast(message, type) {
    toastMessage = message;
    toastType = type;
  }

  function changePage(newPage) {
    currentPage = newPage;
    fetchApiLogs();
  }

  function updateChartData() {
    const labels = hourlyRequestsData.map(data => new Date(data.period).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    const data = {
      labels: labels,
      datasets: [
        {
          label: `${frequency.charAt(0).toUpperCase() + frequency.slice(1)}ly Requests`,
          data: hourlyRequestsData.map(data => data.count),
          backgroundColor: 'rgba(102, 51, 153, 0.2)',
          borderColor: 'rgba(102, 51, 153, 1)',
          borderWidth: 1
        }
      ]
    };
    chartData = data;
  }

  function handleCellClick(field, value) {
    searchParams = { [field]: value };
    fetchApiLogs();
    fetchHourlyRequestsData();
  }

  function resetFilters() {
    searchParams = {};
    fetchApiLogs();
    fetchHourlyRequestsData();
  }
</script>

<section class="dashboard-section">
  <div class="container">
    <h2>Welcome to Your Dashboard</h2>
    <div class="project-selector">
      <label for="project">Select Project:</label>
      <select id="project" bind:value={selectedProjectId} on:change={() => { fetchApiLogs(); fetchHourlyRequestsData(); }}>
        {#each projects as project}
          <option value={project.id}>{project.name}</option>
        {/each}
      </select>
      <button on:click={resetFilters} class="btn-reset">Reset</button>
    </div>
    <div class="selected-filters">
      <p>Selected Filters:</p>
      <ul>
        {#each Object.entries(searchParams) as [key, value]}
          <li>{key}: {value}</li>
        {/each}
      </ul>
    </div>
    <div class="dashboard-content">
      <div class="logs-table">
        <h3>API Logs</h3>
        <table>
          <thead>
            <tr>
              <th>Endpoint</th>
              <th>IP Address</th>
              <th>Request Info</th>
              <th>Location</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {#each apiLogs as log}
              <tr>
                <td on:click={() => handleCellClick('endpoint', log.endpoint)}>{log.endpoint}</td>
                <td on:click={() => handleCellClick('ip_address', log.ip_address)}>{log.ip_address}</td>
                <td on:click={() => handleCellClick('request_info', log.request_info)}>{log.request_info}</td>
                <td on:click={() => handleCellClick('location', log.location)}>{log.location}</td>
                <td>{new Date(log.created_at).toLocaleString()}</td>
              </tr>
            {/each}
          </tbody>
        </table>
        <div class="pagination">
          {#if currentPage > 1}
            <button on:click={() => changePage(currentPage - 1)}>Previous</button>
          {/if}
          {#if currentPage < totalPages}
            <button on:click={() => changePage(currentPage + 1)}>Next</button>
          {/if}
        </div>
      </div>
      <div class="hourly-requests-chart">
        <div class="chart-controls">
          <label for="frequency">Frequency:</label>
          <select id="frequency" bind:value={frequency} on:change={fetchHourlyRequestsData}>
            <option value="minute">Minute</option>
            <option value="hour">Hour</option>
            <option value="day">Day</option>
          </select>
        </div>
        <h3>{frequency.charAt(0).toUpperCase() + frequency.slice(1)}ly Requests (Last 24 Hours)</h3>
        {#if chartData}
          <Bar
            data={chartData}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: `${frequency.charAt(0).toUpperCase() + frequency.slice(1)}ly Requests`
                }
              }
            }}
          />
        {/if}
      </div>
    </div>
  </div>
</section>

{#if toastMessage}
  <Toast message={toastMessage} type={toastType} />
{/if}

<style>
  .dashboard-section {
    padding: 80px 0;
    text-align: center;
    background: #f9f9f9;
    color: #333;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    background: #fff;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  h2 {
    margin-bottom: 20px;
    color: #663399;
  }

  .project-selector {
    margin-bottom: 20px;
  }

  .selected-filters {
    margin-bottom: 20px;
  }

  .selected-filters ul {
    list-style: none;
    padding: 0;
  }

  .selected-filters li {
    display: inline-block;
    background: #663399;
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    margin-right: 10px;
  }

  .btn-reset {
    background-color: #ff4000;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-left: 10px;
  }

  .dashboard-content {
    display: flex;
    justify-content: space-between;
  }

  .logs-table {
    flex: 1;
    margin-right: 20px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    cursor: pointer;
  }

  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #663399;
    color: white;
  }

  .pagination {
    margin-top: 10px;
  }

  .pagination button {
    margin: 0 5px;
    padding: 5px 10px;
    background-color: #663399;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .hourly-requests-chart {
    flex: 1;
  }

  .chart-controls {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
  }

  .chart-controls label {
    margin-right: 10px;
    align-self: center;
  }

  .chart-controls select {
    padding: 5px;
  }
</style>
