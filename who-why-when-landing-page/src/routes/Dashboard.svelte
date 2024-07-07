<script>
  import { onMount } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { isLoggedIn, clearToken } from '../stores/userStore';
  import { createEventDispatcher } from 'svelte';
  import Toast from '../components/Toast.svelte';
  import ProjectSelector from './ProjectSelector.svelte';
  import LogsTable from './LogsTable.svelte';
  import HourlyRequestsChart from './HourlyRequestsChart.svelte';

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
    let startDate = new Date();
    let periods = [];

    if (frequency === "minute") {
      startDate.setHours(startDate.getHours() - 1);
      periods = Array.from({ length: 60 }, (_, i) => {
        const date = new Date(startDate.getTime());
        date.setMinutes(startDate.getMinutes() + i);
        return date;
      });
    } else if (frequency === "day") {
      startDate.setDate(startDate.getDate() - 7);
      periods = Array.from({ length: 7 }, (_, i) => {
        const date = new Date(startDate.getTime());
        date.setDate(startDate.getDate() + i);
        return date;
      });
    } else {
      startDate.setHours(startDate.getHours() - 24);
      periods = Array.from({ length: 24 }, (_, i) => {
        const date = new Date(startDate.getTime());
        date.setHours(startDate.getHours() + i);
        return date;
      });
    }

    const periodCounts = hourlyRequestsData.reduce((acc, { period, count }) => {
      acc[new Date(period).getTime()] = count;
      return acc;
    }, {});

    const labels = periods.map(date => {
      if (frequency === "minute") {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      } else if (frequency === "day") {
        return date.toLocaleDateString();
      } else {
        return date.toLocaleTimeString([], { hour: '2-digit' });
      }
    });

    const data = {
      labels: labels,
      datasets: [
        {
          label: `${frequency.charAt(0).toUpperCase() + frequency.slice(1)}ly Requests`,
          data: periods.map(date => periodCounts[date.getTime()] || 0),
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

  function resetFilters() {
    searchParams = {};
    fetchApiLogs();
    fetchHourlyRequestsData();
  }
</script>

<section class="dashboard-section">
  <div class="container">
    <h2>Welcome to Your Dashboard</h2>
    <ProjectSelector {projects} bind:selectedProjectId on:reset={resetFilters} on:change={async () => { await fetchApiLogs(); await fetchHourlyRequestsData(); }} />
    <div class="selected-filters">
      <p>Selected Filters:</p>
      <ul>
        {#each Object.entries(searchParams) as [key, value]}
          <li>{key}: {value}</li>
        {/each}
      </ul>
    </div>
    <div class="dashboard-content">
      <LogsTable {apiLogs} {currentPage} {totalPages} on:changePage={changePage} on:cellClick={handleCellClick} />
      <HourlyRequestsChart {chartData} {frequency} on:frequencyChange={fetchHourlyRequestsData} />
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

  .dashboard-content {
    display: flex;
    justify-content: space-between;
  }
</style>
