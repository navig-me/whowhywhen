<script>
    import { createEventDispatcher } from 'svelte';
    import { onMount } from 'svelte';
  
    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    export let isTableLoading = false; // New prop for loading state
    const dispatch = createEventDispatcher();
    let showModal = false;
    let modalContent = [];
  
    function handleCellClick(field, value) {
      dispatch('cellClick', { field, value });
    }
  
    function changePage(newPage) {
      if (newPage > 0 && newPage <= totalPages) {
        dispatch('changePage', { page: newPage });
      }
    }
  
    function showQueryParams(params) {
      modalContent = params;
      showModal = true;
    }
  
    function closeModal() {
      showModal = false;
      modalContent = [];
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
              <th>Path</th>
              <th>IP Address</th>
              <th>User Agent</th>
              <th>Response Code</th>
              <th>Response Time</th>
              <th>Location</th>
              <th>Created At</th>
              <th>Query Parameters</th>
            </tr>
          </thead>
          <tbody>
            {#if apiLogs.length === 0}
              <tr>
                <td colspan="8">No logs available</td>
              </tr>
            {:else}
              {#each apiLogs as log}
                <tr>
                  <td on:click={() => handleCellClick('path', log.path)}>{log.path}</td>
                  <td on:click={() => handleCellClick('ip_address', log.ip_address)}>{log.ip_address}</td>
                  <td on:click={() => handleCellClick('user_agent', log.user_agent)}>{log.user_agent}</td>
                  <td on:click={() => handleCellClick('response_code', log.response_code)}>{log.response_code}</td>
                  <td>{log.response_time}</td>
                  <td on:click={() => handleCellClick('location', log.location)}>{log.location}</td>
                  <td>{new Date(log.created_at).toLocaleString()}</td>
                  <td on:click={() => showQueryParams(log.query_params)}>{log.query_params.length}</td>
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
  
  {#if showModal}
    <div class="modal">
      <div class="modal-content">
        <span class="close" on:click={closeModal}>&times;</span>
        <h3>Query Parameters</h3>
        <div class="query-params">
          {#each modalContent as param}
            <div class="param">
              <strong>{param.key}</strong>: {param.value}
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
  
  <style>
    .logs-table {
      flex: 1;
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
  
    .modal {
      display: flex;
      justify-content: center;
      align-items: center;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
    }
  
    .modal-content {
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      width: 50%;
      max-height: 80%;
      overflow-y: auto;
    }
  
    .close {
      float: right;
      font-size: 1.5em;
      cursor: pointer;
    }
  
    .query-params {
      margin-top: 10px;
    }
  
    .param {
      margin-bottom: 5px;
    }
  </style>
  