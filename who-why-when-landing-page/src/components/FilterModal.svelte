<script>
  import { createEventDispatcher } from 'svelte';

  export let title = '';
  export let statusCodes = [];
  export let botTypes = [];
  const dispatch = createEventDispatcher();

  let selectedStatusCode = '';
  let selectedBotType = '';

  function close() {
    dispatch('close');
  }

  function applyFilters() {
    const filters = {
      statusCode: selectedStatusCode,
      botType: selectedBotType,
    };
    dispatch('applyFilters', filters);
    close();
  }
</script>

<div class="modal-overlay" on:click={close}>
  <div class="modal" on:click|stopPropagation>
    <div class="modal-header">
      <h3>{title}</h3>
      <button class="close" on:click={close}>&times;</button>
    </div>
    <div class="modal-content">
      <div class="filter-section">
        <label for="status-code-select">Status Code:</label>
        <select id="status-code-select" bind:value={selectedStatusCode}>
          <option value="">Select Status Code</option>
          {#each statusCodes as code}
            <option value={code}>{code}</option>
          {/each}
        </select>
      </div>
      <div class="filter-section">
        <label for="bot-type-select">Bot Type:</label>
        <select id="bot-type-select" bind:value={selectedBotType}>
          <option value="">Select Bot Type</option>
          {#each botTypes as type}
            <option value={type}>{type}</option>
          {/each}
        </select>
      </div>
      <button class="apply-button" on:click={applyFilters}>Apply Filters</button>
    </div>
  </div>
</div>

<style>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    width: 80%;
    max-width: 500px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .close {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
  }

  .modal-content {
    margin-top: 20px;
  }

  .filter-section {
    margin-bottom: 20px;
  }

  .apply-button {
    display: block;
    width: 100%;
    background: #663399;
    color: #fff;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
  }

  .apply-button:hover {
    background: #7d42a6;
  }
</style>
