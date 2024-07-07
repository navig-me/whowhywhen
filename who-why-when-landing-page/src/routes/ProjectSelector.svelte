<script>
    export let projects = [];
    export let selectedProjectId = null;
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
  
    function handleChange() {
      dispatch('change');
    }
  
    function resetFilters() {
      dispatch('reset');
    }
  </script>
  
  <div class="project-selector">
    <label for="project">Select Project:</label>
    <select id="project" bind:value={selectedProjectId} on:change={handleChange}>
      {#each projects as project}
        <option value={project.id}>{project.name}</option>
      {/each}
    </select>
    <button on:click={resetFilters} class="btn-reset">Reset</button>
  </div>
  
  <style>
    .project-selector {
      margin-bottom: 20px;
    }
  
    .btn-reset {
      background-color: #ff4000;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      margin-left: 10px;
    }
  </style>
  