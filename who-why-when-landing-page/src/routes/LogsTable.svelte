<script>
    import { createEventDispatcher, onMount } from 'svelte';
  
    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    const dispatch = createEventDispatcher();
  
    function handleCellClick(field, value) {
      dispatch('cellClick', { field, value });
    }
  
    function changePage(newPage) {
      if (newPage > 0 && newPage <= totalPages) {
        dispatch('changePage', { page: newPage });
      }
    }
  
    function handleScroll(event) {
      const { scrollTop, scrollHeight, clientHeight } = event.target;
      if (scrollTop + clientHeight >= scrollHeight && currentPage < totalPages) {
        changePage(currentPage + 1);
      }
    }
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
  </style>
  