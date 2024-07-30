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
  import FilterModal from '../components/FilterModal.svelte';
  import BotHighlights from '../components/BotHighlights.svelte';
  import { API_BASE_URL, DASH_API_BASE_URL } from '../config';
  import { navigate } from 'svelte-routing';
  
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
  let responseCodeData = null;
  let botBrowserFamilyData = null;
  let userAgentData = null;
  let barChartData = null;
  let frequency = "hour";
  let searchParams = {};
  let query = '';
  let sort = null;
  let sortDirection = 'asc';
  let isTableLoading = false;
  let isChartLoading = false;
  let isPieChartLoading = true;
  let selectedTimeRange = 'last_24_hours';
  let showFilterModal = false;
  let modalTitle = '';
  let statusCodes = [];
  let botTypes = [];
  let topBotsData = [];
  let isBotDataLoading = true;
  
  const dispatch = createEventDispatcher();
  let showBanner = false;
  
  selectedProjectIdStore.subscribe(async (projectId) => {
    if (projectId) {
      selectedProjectId = projectId;
      gtag('event', 'select_project', {
        event_category: 'Project',
        event_label: projectId,
      });
      await fetchApiLogs();
      await fetchHourlyRequestsData();
      await fetchCountsData();
      await fetchTopBotsData();
    }
  });
  
  onMount(async () => {
    await fetchProjects();
    gtag('event', 'page_view', {
      page_title: 'Bots Dashboard',
      page_path: '/bots',
    });
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
        await fetchTopBotsData();
      }
    } else if (response.status === 401) {
      clearToken();
      navigate('/login');
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
    let url = `${DASH_API_BASE_URL}/dashapi/logs/project/${selectedProjectId}?page=${currentPage}&limit=${logsPerPage}&bots_only=true`;
    if (query) {
      url += `&query=${query}`;
    }
    if (sort) {
      url += `&sort=${sort}`;
    }
    if (sortDirection) {
      url += `&sort_direction=${sortDirection}`;
    }
    if (selectedTimeRange !== 'all') {
      const timeParams = getTimeRangeParams(selectedTimeRange);
      url += `&start_datetime=${timeParams.start_datetime}&end_datetime=${timeParams.end_datetime}`;
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
      showBanner = apiLogs.length <= 5;
    } else if (response.status === 401) {
      clearToken();
      navigate('/login');
    } else {
      showToast('Failed to fetch API logs', 'error');
    }
    isTableLoading = false;
  }
  
  async function fetchHourlyRequestsData() {
    isChartLoading = true;
    const token = localStorage.getItem('token');
    let url = `${DASH_API_BASE_URL}/dashapi/logs/project/stats/${selectedProjectId}?frequency=${frequency}&bots_only=true`;
    if (selectedTimeRange !== 'all') {
      const timeParams = getTimeRangeParams(selectedTimeRange);
      url += `&start_datetime=${timeParams.start_datetime}&end_datetime=${timeParams.end_datetime}`;
    }
    const response = await fetch(url, {
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
      navigate('/login');
    } else {
      showToast('Failed to fetch hourly requests data', 'error');
    }
    isChartLoading = false;
  }
  
  async function fetchCountsData() {
    isPieChartLoading = true;
    const token = localStorage.getItem('token');
    let url = `${DASH_API_BASE_URL}/dashapi/logs/project/device-stats/${selectedProjectId}?bots_only=true`;
    if (selectedTimeRange !== 'all') {
      const timeParams = getTimeRangeParams(selectedTimeRange);
      url += `&start_datetime=${timeParams.start_datetime}&end_datetime=${timeParams.end_datetime}`;
    }
    const response = await fetch(url, {
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
      navigate('/login');
    } else {
      showToast('Failed to fetch counts data', 'error');
    }
    isPieChartLoading = false;
  }
  
  async function fetchTopBotsData() {
    isBotDataLoading = true;
    const token = localStorage.getItem('token');
    let url = `${DASH_API_BASE_URL}/dashapi/logs/project/bot-stats/${selectedProjectId}`;
    if (selectedTimeRange !== 'all') {
        const timeParams = getTimeRangeParams(selectedTimeRange);
        url += `?start_datetime=${timeParams.start_datetime}&end_datetime=${timeParams.end_datetime}`;
    }
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    if (response.ok) {
        const data = await response.json();
        console.log('Fetched Top Bots Data:', data);
        topBotsData = data.bot_stats || [];
    } else if (response.status === 401) {
      clearToken();
      navigate('/login');
    } else {
      showToast('Failed to fetch top bots data', 'error');
    }
    isBotDataLoading = false;
  }
  
  function updateChartData() {
    const labels = hourlyRequestsData.map(data => data.period);
    const successCounts = hourlyRequestsData.map(data => data['2xx_count']);
    const redirectCounts = hourlyRequestsData.map(data => data['3xx_count']);
    const clientErrorCounts = hourlyRequestsData.map(data => data['4xx_count']);
    const serverErrorCounts = hourlyRequestsData.map(data => data['5xx_count']);
    const avgResponseTimes = hourlyRequestsData.map(data => data.avg_response_time);

    const data = {
      labels: labels,
      datasets: [
        {
          type: 'bar',
          label: '2xx Success',
          data: successCounts,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          stack: 'combined',
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: '3xx Redirects',
          data: redirectCounts,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          stack: 'combined',
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: '4xx Client Errors',
          data: clientErrorCounts,
          backgroundColor: 'rgba(255, 206, 86, 0.2)',
          borderColor: 'rgba(255, 206, 86, 1)',
          borderWidth: 1,
          stack: 'combined',
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: '5xx Server Errors',
          data: serverErrorCounts,
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
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 2,
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
      title: 'Browser'
    };
  
    responseCodeData = {
      labels: Object.keys(data.response_code_counts),
      datasets: [
        {
          data: Object.values(data.response_code_counts),
        }
      ],
      title: 'Response Code'
    };
  
    botBrowserFamilyData = {
      labels: Object.keys(data.bot_browser_family_counts),
      datasets: [
        {
          data: Object.values(data.bot_browser_family_counts),
        }
      ],
      title: 'Bot Visits'
    };
  
    userAgentData = {
      labels: Object.keys(data.user_agent_counts),
      datasets: [
        {
          data: Object.values(data.user_agent_counts),
        }
      ],
      title: 'User Agents'
    };

    statusCodes = responseCodeData.labels;
    botTypes = botBrowserFamilyData.labels;
  }
  
  function getTimeRangeParams(timeRange) {
    const endDate = new Date().toISOString();
    let startDate;
    switch (timeRange) {
      case 'last_hour':
        startDate = new Date(Date.now() - 60 * 60 * 1000).toISOString();
        break;
      case 'last_24_hours':
        startDate = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
        break;
      case 'last_7_days':
        startDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
        break;
      case 'last_30_days':
        startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
        break;
      case 'last_90_days':
        startDate = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString();
        break;
      default:
        startDate = null;
    }
    return { start_datetime: startDate, end_datetime: endDate };
  }
  
  function handleTimeRangeChange(event) {
    selectedTimeRange = event.target.value;
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
    fetchTopBotsData();
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
    fetchTopBotsData();
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
    fetchTopBotsData();
  }
  
  function resetFilters() {
    searchParams = {};
    currentPage = 1;
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
    fetchTopBotsData();
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
    fetchTopBotsData();
  }
  
  function openFiltersModal() {
    modalTitle = "Select Filter";
    showFilterModal = true;
  }

  function handleApplyFilters(event) {
    const { statusCode, botType } = event.detail;
    // Split response_code and get the first 3 characters
    const responseCode = statusCode.split(' ')[0].slice(0, 3);
    if (statusCode) {
      searchParams = { ...searchParams, response_code: responseCode };
    }
    if (botType) {
      searchParams = { ...searchParams, user_agent: botType };
    }
    fetchApiLogs();
    fetchHourlyRequestsData();
    fetchCountsData();
    fetchTopBotsData();
  }
</script>

<section class="dashboard-section">
<div class="container">
  {#if showBanner}
    <div class="banner">
      <p>Not enough data for the selected filters. Visit the <a href="/projects">Projects</a> page to test your API keys and see data on this chart. Click on <strong>Integrate</strong> to view the steps to integrate with your API.</p>
    </div>
  {/if}
  <div class="dashboard-content">
    <div class="left-column">
      <div class="project-selector-container">
        <ProjectSelector {projects} bind:selectedProjectId on:reset={resetFilters} on:change={async () => { await fetchApiLogs(); await fetchHourlyRequestsData(); await fetchCountsData(); await fetchTopBotsData(); }} />
      </div>
      <div class="filters-container">
        <div class="time-range">
          <label for="time-range-select">Show:</label>
          <select id="time-range-select" on:change={handleTimeRangeChange}>
            <option value="last_hour">Last Hour</option>
            <option value="last_24_hours">Last 24 Hours</option>
            <option value="last_7_days">Last 7 Days</option>
            <option value="last_30_days">Last 30 Days</option>
            <option value="last_90_days">Last 90 Days</option>
            <option value="all">All</option>
          </select>
        </div>
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
    <div class="right-column">
      <div class="filters-icon-container">
        <i class="fa fa-filter" aria-hidden="true" on:click={openFiltersModal}></i>
      </div>
      <BotHighlights {topBotsData} {isBotDataLoading} />
      <div class="charts-container">
        <RequestsChart {barChartData} {frequency} {isChartLoading} on:frequencyChange={handleFrequencyChange} class="full-width-chart"/>
      </div>
      <div class="pie-charts-container">
        <PieChart pieChartData={responseCodeData} {isPieChartLoading} />
        <PieChart pieChartData={botBrowserFamilyData} {isPieChartLoading} />
      </div>
      <LogsTable {apiLogs} {currentPage} {totalPages} {isTableLoading} on:changePage={(e) => changePage(e.detail.page)} on:cellClick={handleCellClick} on:addFilter={handleAddFilter} />
      </div>
  </div>
</div>
</section>

{#if showFilterModal}
<FilterModal title={modalTitle} {statusCodes} {botTypes} on:close={() => (showFilterModal = false)} on:applyFilters={handleApplyFilters} />
{/if}

{#if toastMessage}
<Toast message={toastMessage} type={toastType} />
{/if}

<style>
.dashboard-section {
  padding: 20px 0;
  text-align: center;
  background: linear-gradient(135deg, #f9f9f9 25%, #fff 75%);
  color: #333;
}

.banner {
  background: #ffcc00;
  color: #333;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.banner p {
  margin: 0;
}

.banner a {
  color: #663399;
  text-decoration: none;
}

.banner a:hover {
  text-decoration: underline;
}

.container {
  margin: 0 auto;
  background: #fff;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.1);
}

.dashboard-content {
  display: flex;
  gap: 20px;
}

.left-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 300px;
}

.right-column {
  flex: 4;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.project-selector-container {
  background: #f1f1f1;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.filters-container {
  background: #f1f1f1;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.time-range {
  display: flex;
  flex-direction: column;
  gap: 10px;
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
  flex-direction: column;
  gap: 10px;
}

.search-container input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  flex: 1;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.search-container button {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
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

.charts-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  flex-wrap: wrap;
}

.full-width-chart {
  width: 100%;
  min-height: 300px;
}

.pie-charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.pie-chart {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.filters-icon-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.filters-icon-container i {
  font-size: 1.5em;
  cursor: pointer;
  color: #663399;
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

  .dashboard-content {
    flex-direction: column;
  }

  .selected-filters ul {
    padding: 0 10px;
  }

  .selected-filters li {
    font-size: 0.8em;
    padding: 5px 10px;
  }

  .charts-container {
    flex-direction: column;
  }

  .pie-charts-container {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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

  .charts-container {
    flex-direction: column;
  }

  .pie-charts-container {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
