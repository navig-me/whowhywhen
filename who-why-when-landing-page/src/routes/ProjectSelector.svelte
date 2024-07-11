<script>
  import { createEventDispatcher } from 'svelte';

  export let projects = [];
  export let selectedProjectId = null;
  const dispatch = createEventDispatcher();

  function handleProjectChange(event) {
    dispatch('change', event.target.value);
  }

  function resetFilters() {
    dispatch('reset');
  }
</script>

<div class="project-selector">
  <label for="project">Select Project:</label>
  <select id="project" bind:value={selectedProjectId} on:change={handleProjectChange}>
      {#each projects as project}
          <option value={project.id}>{project.name}</option>
      {/each}
  </select>
  <button on:click={resetFilters} class="btn-reset">Reset</button>
</div>

<style>
  .project-selector {
      display: flex;
      flex-direction: column;
      gap: 10px;
      background: #fff;
      padding: 15px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  label {
      font-size: 1em;
      font-weight: bold;
      color: #333;
  }

  select {
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 5px;
      font-size: 1em;
  }

  .btn-reset {
      background-color: #ff4000;
      color: #fff;
      padding: 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s ease;
      width: 100%;
      text-align: center;
  }

  .btn-reset:hover {
      background-color: #ff6347;
  }
</style>
