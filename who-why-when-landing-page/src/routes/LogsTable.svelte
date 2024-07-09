<script>
    import { createEventDispatcher, onMount } from 'svelte';
  
    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    let logsEnd = false; // Flag to check if all logs are loaded
    const dispatch = createEventDispatcher();
  
    function handleCellClick(field, value) {
      dispatch('cellClick', { field, value });
    }
  
    function changePage(newPage) {
      dispatch('changePage', { page: newPage });
    }
  
    function handleScroll(event) {
      const { scrollTop, scrollHeight, clientHeight } = event.target;
      if (scrollTop + clientHeight >= scrollHeight && !logsEnd) {
        changePage(currentPage + 1);
      }
    }
  
    onMount(() => {
      // Check if all logs are loaded
      logsEnd = currentPage >= totalPages;
    });
  </script>
  
  <div class="logs-table">
    <h3>API Logs</h3>
    <div class="table-container" on:scroll={handleScroll}>
      <table>
        <thead>
          <tr>
            <th>Endpoint</th>
            <th>IP Address</th>
            <th>Request Info</th>
            <th>Response Code</th>
            <th>Response Time</th>
            <th>Location</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {#if apiLogs.length === 0}
            <tr>
              <td colspan="7">No logs available</td>
            </tr>
          {:else}
            {#each apiLogs as log}
              <tr>
                <td on:click={() => handleCellClick('endpoint', log.endpoint)}>{log.endpoint}</td>
                <td on:click={() => handleCellClick('ip_address', log.ip_address)}>{log.ip_address}</td>
                <td>{log.request_info}</td>
                <td on:click={() => handleCellClick('response_code', log.response_code)}>{log.response_code}</td>
                <td>{log.response_time}</td>
                <td on:click={() => handleCellClick('location', log.location)}>{log.location}</td>
                <td>{new Date(log.created_at).toLocaleString()}</td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>
  </div>
  
  <style>
    .logs-table {
      flex: 1;
      margin-right: 20px;
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      max-width: 100%;
      overflow-x: auto;
    }
  
    .table-container {
      height: 400px; /* Adjust height for scrolling */
      overflow-y: auto;
    }
  
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8em; /* Smaller font size */
      cursor: pointer;
      margin-bottom: 10px;
    }
  
    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
  
    th {
      background-color: #663399;
      color: white;
      font-size: 1.1em;
    }
  
    tr:hover {
      background-color: #f1f1f1;
    }
  </style>
  