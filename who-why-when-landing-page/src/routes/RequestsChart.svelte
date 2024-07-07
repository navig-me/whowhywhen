<script>
  import { Bar } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';
  import { createEventDispatcher } from 'svelte';

  Chart.register(...registerables);

  export let chartData = null;
  export let frequency = "hour";
  const dispatch = createEventDispatcher();

  function handleFrequencyChange(event) {
    dispatch('frequencyChange', event.target.value);
  }
</script>

<div class="requests-chart">
  <div class="chart-controls">
    <label for="frequency">Frequency:</label>
    <select id="frequency" bind:value={frequency} on:change={handleFrequencyChange}>
      <option value="minute">Minute</option>
      <option value="hour">Hour</option>
      <option value="day">Day</option>
    </select>
  </div>
  <h3>Requests per {frequency.charAt(0).toUpperCase() + frequency.slice(1)}</h3>
  {#if chartData}
    <Bar
      data={chartData}
      options={{
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: `Requests per ${frequency.charAt(0).toUpperCase() + frequency.slice(1)}`
          }
        }
      }}
    />
  {/if}
</div>

<style>
  .requests-chart {
    flex: 1;
  }

  .chart-controls {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
  }

  .chart-controls label {
    margin-right: 10px;
    align-self: center;
  }

  .chart-controls select {
    padding: 5px;
  }
</style>
