<script>
  import { onMount } from 'svelte';
  import { currentView } from '../stores/viewStore';
  import { selectedProjectIdStore, isLoggedIn, clearToken } from '../stores/userStore';
  import { createEventDispatcher } from 'svelte';
  import Toast from '../components/Toast.svelte';
  import ProjectSelector from './ProjectSelector.svelte';
  import LogsTable from './LogsTable.svelte';
  import RequestsChart from './RequestsChart.svelte';
  import PieChart from './PieChart.svelte';
  import { API_BASE_URL, DASH_API_BASE_URL } from '../config';

  let projects = [];
  let selectedProjectId = null;
  let apiLogs = [];
  let toastMessage = '';
  let toastType = '';
  let currentPage = 1;
  let totalPages = 1;
  let logsPerPage = 20;
  let hourlyRequestsData = [];
  let browserFamilyData = null;
  let osFamilyData = null;
  let deviceTypeData = null;
  let barChartData = null;
  let frequency = "hour";
  let searchParams = {};
  let query = '';
  let sort = null;
  let sortDirection = 'asc';
  let isTableLoading = false;
  let isChartLoading = false;
  let isPieChartLoading = true;

  const dispatch = createEventDispatcher();

  selectedProjectIdStore.subscribe(async (projectId) => {
    if (projectId) {
      selectedProjectId = projectId;
      await fetchApiLogs();
      await fetchHourlyRequestsData();
      await fetchCountsData();
    }
  });

  onMount(async () => {
    await fetchProjects();
  });

  async function fetchProjects() {
    isTableLoading = true;
    isChartLoading = true;
    isPieChartLoading = true;
    const token = localStorage.getItem('token');
    const response = await fetch(`${DASH_API_BASE_URL}/dashauth/users/me/projects`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.ok) {
      projects = await response.json();
      if (projects.length > 0 && !selectedProjectId) {
        selectedProjectId = projects[0].id;
        await fetchApiLogs();
        await fetchHourlyRequestsData();
        await fetchCountsData();
      }
    } else if (response.status === 401) {
      clearToken();
      currentView.set('login');
    } else {
      showToast('Failed to fetch projects', 'error');
    }
    isTableLoading = false;
    isChartLoading = false;
    isPieChartLoading = false;
  }

  async function fetchApiLogs() {
    isTableLoading = true;
    const token = localStorage.getItem('token');
    let url = `${DASH_API_BASE_URL}/dashapi/logs/project/${selectedProjectId}?page=${currentPage}&limit=${logsPerPage}`;
    if (query) {
      url += `&query=${query}`;
    }
    if (sort) {
      url += `&sort=${sort}`;
    }
    if (sortDirection) {
      url += `&sort_direction=${sortDirection}`;
    }
    const response = await fetch(url, {
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
    } else if (response.status === 401) {
      clearToken();
      currentView.set('login');
    } else {
      showToast('Failed to fetch API logs', 'error');
    }
    isTableLoading = false;
  }

  async function fetchHourlyRequestsData() {
    isChartLoading = true;
    const token = localStorage.getItem('token');
    const response = await fetch(`${DASH_API_BASE_URL}/dashapi/logs/project/stats/${selectedProjectId}?frequency=${frequency}`, {
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
    } else if (response.status === 401) {
      clearToken();
      currentView.set('login');
    } else {
      showToast('Failed to fetch hourly requests data', 'error');
    }
    isChartLoading = false;
  }

  async function fetchCountsData() {
    isPieChartLoading = true;
    const token = localStorage.getItem('token');
    const response = await fetch(`${DASH_API_BASE_URL}/dashapi/logs/project/device-stats/${selectedProjectId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(searchParams)
    });
    if (response.ok) {
      let data = await response.json();
      data = data.counts;
      updatePieChartData(data);
    } else if (response.status === 401) {
      clearToken();
      currentView.set('login');
    } else {
      showToast('Failed to fetch counts data', 'error');
    }
    isPieChartLoading = false;
  }

  function updateChartData() {
    const labels = hourlyRequestsData.map(data => data.period);
    const successCounts = hourlyRequestsData.map(data => data.success_count);
    const errorCounts = hourlyRequestsData.map(data => data.error_count);
    const avgResponseTimes = hourlyRequestsData.map(data => data.avg_response_time);

    const data = {
      labels: labels,
      datasets: [
        {
          type: 'bar',
          label: 'Success Count',
          data: successCounts,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          stack: 'combined',
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: 'Error Count',
          data: errorCounts,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          stack: 'combined',
          yAxisID: 'y'
        },
        {
          type: 'line',
          label: 'Avg Response Time',
          data: avgResponseTimes,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          yAxisID: 'y1'
        }
      ]
    };
    barChartData = data;
  }

  function updatePieChartData(data) {
    browserFamilyData = {
      labels: Object.keys(data.browser_family_counts),
      datasets: [
        {
          data: Object.values(data.browser_family_counts),
        }
      ],
      title: 'Browser Family'
    };

    osFamilyData = {
      labels: Object.keys(data.os_family_counts),
      datasets: [
        {
          data: Object.values(data.os_family_counts),
        }
      ],
      title: 'OS Family'
    };

    deviceTypeData = {
      labels: Object.keys(data.device_type_counts),
      datasets: [
        {
          data: Object.values(data.device_type_counts),
        }
      ],
      title: 'Device Type'
    };
  }

  function showToast(message, type) {
    toastMessage = message;
    toastType = type;
  }

  function changePage(newPage) {
    currentPage = newPage;
    fetchApiLogs();
  }

  function handleCellClick(event) {
    const { field, value } = event.detail;
    searchParams = { ...searchParams, [field]: value };
    currentPage = 1;
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
  }

  function handleFrequencyChange(event) {
    frequency = event.detail;
    fetchHourlyRequestsData();
  }

  function removeFilter(key) {
    const { [key]: _, ...rest } = searchParams;
    searchParams = rest;
    currentPage = 1;
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
  }

  function resetFilters() {
    searchParams = {};
    currentPage = 1;
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
  }

  function formatKey(key) {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  function handleSearchInput(event) {
    query = event.target.value;
  }

  function triggerSearch() {
    fetchApiLogs();
  }

  function handleSort(field) {
    if (sort === field) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sort = field;
      sortDirection = 'asc';
    }
    fetchApiLogs();
  }

  function handleAddFilter(event) {
    const { field, value } = event.detail;
    searchParams = { ...searchParams, [field]: value };
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
  }
</script>

<section class="dashboard-section">
  <div class="container">
    <div class="dashboard-header">
      <div class="left-column">
        <ProjectSelector {projects} bind:selectedProjectId on:reset={resetFilters} on:change={async () => { await fetchApiLogs(); await fetchHourlyRequestsData(); await fetchCountsData(); }} />
      </div>
      <div class="right-column">
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
        <div class="search-container">
          <input type="text" placeholder="Search..." on:input={handleSearchInput} />
          <button on:click={triggerSearch}>Search</button>
        </div>
      </div>
    </div>
    <div class="dashboard-content">
      <LogsTable {apiLogs} {currentPage} {totalPages} {isTableLoading} on:changePage={(e) => changePage(e.detail.page)} on:cellClick={handleCellClick} on:addFilter={handleAddFilter} />
      <div class="charts-container">
        <RequestsChart {barChartData} {frequency} {isChartLoading} on:frequencyChange={handleFrequencyChange} class="full-width-chart"/>
      </div>
      <div class="pie-charts-container">
        <PieChart pieChartData={browserFamilyData} {isPieChartLoading} />
        <PieChart pieChartData={osFamilyData} {isPieChartLoading} />
        <PieChart pieChartData={deviceTypeData} {isPieChartLoading} />
      </div>
    </div>
  </div>
</section>

{#if toastMessage}
  <Toast message={toastMessage} type={toastType} />
{/if}

<style>
  .dashboard-section {
    padding: 40px 20px;
    text-align: center;
    background: linear-gradient(135deg, #f9f9f9 25%, #fff 75%);
    color: #333;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    background: #fff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 30px rgba(0, 0, 0, 0.1);
  }

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
  }

  .left-column {
    flex: 1;
    margin-right: 20px;
  }

  .right-column {
    flex: 2;
    display: flex;
    flex-direction: column;
  }

  .selected-filters {
    margin-bottom: 10px;
    padding: 10px;
    background: #f1f1f1;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
    border-radius: 15px;
    margin: 5px;
    font-size: 0.8em;
    transition: background 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }

  .selected-filters li button {
    background: none;
    border: none;
    color: #fff;
    margin-left: 10px;
    cursor: pointer;
    font-size: 1em;
  }

  .selected-filters li:hover {
    background: #7d42a6;
  }

  .search-container {
    display: flex;
    justify-content: flex-start;
  }

  .search-container input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px 0 0 5px;
    font-size: 1em;
    flex: 1;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  .search-container button {
    padding: 10px 20px;
    border: 1px solid #ddd;
    border-left: none;
    border-radius: 0 5px 5px 0;
    background-color: #663399;
    color: #fff;
    cursor: pointer;
    font-size: 1em;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: background 0.3s ease;
  }

  .search-container button:hover {
    background-color: #7d42a6;
  }

  .dashboard-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 20px;
  }

  .charts-container {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    flex-wrap: wrap;
  }

  .full-width-chart {
    width: 100%;
    min-height: 300px; /* Ensure the chart has a minimum height */
  }

  .pie-charts-container {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    flex-wrap: wrap;
  }

  .pie-chart {
    flex: 1;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    margin: 20px;
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


  @keyframes fadeInOut {
    0% { opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { opacity: 0; }
  }

  @media (max-width: 768px) {
    .container {
      padding: 20px;
    }

    .dashboard-header {
      flex-direction: column;
    }

    .right-column {
      margin-top: 20px;
    }

    .selected-filters ul {
      padding: 0 10px;
    }

    .selected-filters li {
      font-size: 0.8em;
      padding: 5px 10px;
    }

    .dashboard-content {
      gap: 10px;
    }

    .charts-container {
      flex-direction: column;
    }

    .pie-charts-container {
      flex-direction: column;
    }
  }

  @media (max-width: 480px) {
    .container {
      padding: 10px;
    }

    .selected-filters ul {
      padding: 0 5px;
    }

    .selected-filters li {
      font-size: 0.7em;
      padding: 5px 8px;
    }

    .toast {
      padding: 10px 20px;
      font-size: 0.9em;
    }

    .dashboard-content {
      gap: 5px;
    }

    .charts-container {
      flex-direction: column;
    }

    .pie-charts-container {
      flex-direction: column;
    }
  }
</style>
