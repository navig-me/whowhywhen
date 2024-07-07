<script>
  import { onMount } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { isLoggedIn, clearToken } from '../stores/userStore';
  import { createEventDispatcher } from 'svelte';
  import Toast from '../components/Toast.svelte';
  import ProjectSelector from './ProjectSelector.svelte';
  import LogsTable from './LogsTable.svelte';
  import RequestsChart from './RequestsChart.svelte';
  import { API_BASE_URL } from '../config'; // Import the base URL

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
    const response = await fetch(`${API_BASE_URL}/auth/users/me/projects`, {
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
    const response = await fetch(`${API_BASE_URL}/api/logs/project/${selectedProjectId}?page=${currentPage}&limit=${logsPerPage}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...searchParams
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
    const response = await fetch(`${API_BASE_URL}/api/logs/project/stats/${selectedProjectId}?frequency=${frequency}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(searchParams)
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
    const labels = hourlyRequestsData.map(data => data.period);
    const data = {
      labels: labels,
      datasets: [
        {
          label: `Requests per ${frequency.charAt(0).toUpperCase() + frequency.slice(1)}`,
          data: hourlyRequestsData.map(data => data.count),
          backgroundColor: 'rgba(102, 51, 153, 0.2)',
          borderColor: 'rgba(102, 51, 153, 1)',
          borderWidth: 1
        }
      ]
    };
    chartData = data;
  }

  function handleCellClick(event) {
    const { field, value } = event.detail;
    searchParams = { ...searchParams, [field]: value };
    fetchApiLogs();
    fetchHourlyRequestsData();
  }

  function handleFrequencyChange(event) {
    frequency = event.detail;
    fetchHourlyRequestsData();
  }

  function removeFilter(key) {
    const { [key]: _, ...rest } = searchParams; // Destructure to remove the key
    searchParams = rest;
    fetchApiLogs();
    fetchHourlyRequestsData();
  }

  function resetFilters() {
    searchParams = {};
    fetchApiLogs();
    fetchHourlyRequestsData();
  }
  
  function formatKey(key) {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

</script>

<section class="dashboard-section">
  <div class="container">
    <ProjectSelector {projects} bind:selectedProjectId on:reset={resetFilters} on:change={async () => { await fetchApiLogs(); await fetchHourlyRequestsData(); }} />
    <div class="selected-filters">
      <p>Selected Filters:</p>
      <ul>
        {#if Object.keys(searchParams).length === 0}
          <li>Select values in the table to filter</li>
        {:else}
          {#each Object.entries(searchParams) as [key, value]}
            <li>
              {formatKey(key)}: {value} <button on:click={() => removeFilter(key)}>✖</button>
            </li>
          {/each}
        {/if}
      </ul>
    </div>
    <div class="dashboard-content">
      <LogsTable {apiLogs} {currentPage} {totalPages} on:changePage={changePage} on:cellClick={handleCellClick} />
      <RequestsChart {chartData} {frequency} on:frequencyChange={handleFrequencyChange} />
    </div>
  </div>
</section>

{#if toastMessage}
  <Toast message={toastMessage} type={toastType} />
{/if}

<style>
  .dashboard-section {
    padding: 60px 0;
    text-align: center;
    background: #f9f9f9;
    color: #333;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    background: #fff;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 6px 30px rgba(0, 0, 0, 0.1);
  }

  h2 {
    margin-bottom: 30px;
    color: #663399;
    font-size: 2.5em;
  }

  .selected-filters {
    margin-bottom: 30px;
    padding: 10px;
    background: #f1f1f1;
    border-radius: 10px;
  }

  .selected-filters ul {
    list-style: none;
    padding: 0;
  }

  .selected-filters li {
    display: inline-block;
    background: #663399;
    color: #fff;
    padding: 5px 15px;
    border-radius: 20px;
    margin: 5px;
    font-size: 0.9em;
    transition: background 0.3s ease;
  }

  .selected-filters li button {
    background: none;
    border: none;
    color: #fff;
    margin-left: 10px;
    cursor: pointer;
    font-size: 1.2em;
  }

  .selected-filters li:hover {
    background: #7d42a6;
  }

  .dashboard-content {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 15px 30px;
    border-radius: 30px;
    box-shadow: 0 6px 30px rgba(0, 0, 0, 0.1);
    color: white;
    font-weight: bold;
    z-index: 1000;
    animation: fadeInOut 6s ease-in-out;
  }

  .toast.info {
    background-color: #663399;
  }

  .toast.success {
    background-color: #28a745;
  }

  .toast.error {
    background-color: #dc3545;
  }

  @keyframes fadeInOut {
    0% { opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { opacity: 0; }
  }
</style>
