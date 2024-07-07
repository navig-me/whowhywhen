<script>
    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
  
    function changePage(newPage) {
      dispatch('changePage', newPage);
    }
  
    function handleCellClick(field, value) {
      dispatch('cellClick', { field, value });
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
  
  <style>
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
  </style>
  