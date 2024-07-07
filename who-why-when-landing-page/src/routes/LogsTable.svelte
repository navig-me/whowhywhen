<script>
    import { createEventDispatcher } from 'svelte';
  
    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    const dispatch = createEventDispatcher();
  
    function handleCellClick(field, value) {
      dispatch('cellClick', { field, value });
    }
  
    function changePage(newPage) {
      dispatch('changePage', { page: newPage });
    }
  </script>
  
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
        {#if apiLogs.length === 0}
          <tr>
            <td colspan="5">No logs available</td>
          </tr>
        {:else}
          {#each apiLogs as log}
            <tr>
              <td on:click={() => handleCellClick('endpoint', log.endpoint)}>{log.endpoint}</td>
              <td on:click={() => handleCellClick('ip_address', log.ip_address)}>{log.ip_address}</td>
              <td on:click={() => handleCellClick('request_info', log.request_info)}>{log.request_info}</td>
              <td on:click={() => handleCellClick('location', log.location)}>{log.location}</td>
              <td>{new Date(log.created_at).toLocaleString()}</td>
            </tr>
          {/each}
        {/if}
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
  
  <style>
    .logs-table {
      flex: 1;
      margin-right: 20px;
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
  
    table {
      width: 100%;
      border-collapse: collapse;
      cursor: pointer;
      margin-bottom: 10px;
    }
  
    th, td {
      border: 1px solid #ddd;
      padding: 12px;
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
      justify-content: flex-end;
      gap: 10px;
    }
  
    .pagination button {
      padding: 10px 15px;
      background-color: #663399;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s ease;
    }
  
    .pagination button:hover {
      background-color: #7d42a6;
    }
  </style>
