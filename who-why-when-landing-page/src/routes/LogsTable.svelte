<script>
    import { createEventDispatcher } from 'svelte';
  
    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    export let isTableLoading = false; // New prop for loading state
    const dispatch = createEventDispatcher();
  
    function handleCellClick(field, value) {
      dispatch('cellClick', { field, value });
    }
  
    function changePage(newPage) {
      if (newPage > 0 && newPage <= totalPages) {
        dispatch('changePage', { page: newPage });
      }
    }
  
    function handleSort(field) {
      dispatch('sort', field);
    }
  </script>
  
  <div class="logs-table">
    <h3>API Logs</h3>
    <div class="table-container">
      {#if isTableLoading}
        <div class="loading">Loading...</div>
      {:else}
        <table>
          <thead>
            <tr>
              <th on:click={() => handleSort('endpoint')}>Endpoint</th>
              <th on:click={() => handleSort('ip_address')}>IP Address</th>
              <th>Request Info</th>
              <th on:click={() => handleSort('response_code')}>Response Code</th>
              <th on:click={() => handleSort('response_time')}>Response Time</th>
              <th on:click={() => handleSort('location')}>Location</th>
              <th on:click={() => handleSort('created_at')}>Created At</th>
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
      {/if}
    </div>
    <div class="pagination">
      <button on:click={() => changePage(1)} disabled={currentPage === 1}>First</button>
      <button on:click={() => changePage(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
      <button disabled>{currentPage}</button>
      <button on:click={() => changePage(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
      <button on:click={() => changePage(totalPages)} disabled={currentPage === totalPages}>Last</button>
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
  
    .pagination {
      display: flex;
      justify-content: center;
      gap: 5px;
      margin-top: 20px;
    }
  
    .pagination button {
      padding: 5px 10px;
      border: 1px solid #663399;
      background-color: #fff;
      color: #663399;
      cursor: pointer;
      border-radius: 5px;
    }
  
    .pagination button.active {
      background-color: #663399;
      color: #fff;
    }
  
    .pagination button:disabled {
      background-color: #ddd;
      color: #666;
      cursor: not-allowed;
    }
  
    .loading {
      text-align: center;
      padding: 20px;
      font-size: 1.2em;
      color: #663399;
    }
  </style>
  