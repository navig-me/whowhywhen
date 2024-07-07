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
  