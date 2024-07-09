<script>
  import { Bar, Line } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';
  import { createEventDispatcher } from 'svelte';

  Chart.register(...registerables);

  export let chartData = null;
  export let frequency = "hour";
  export let isChartLoading = false; // New prop for loading state
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
  {#if isChartLoading}
    <p class="loading">Loading...</p>
  {:else if chartData}
    <Bar
      data={chartData}
      options={{
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Request Count'
            }
          },
          y1: {
            beginAtZero: true,
            position: 'right',
            grid: {
              drawOnChartArea: false
            },
            title: {
              display: true,
              text: 'Average Response Time (s)'
            }
          }
        },
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
  {:else}
    <p>No data available</p>
  {/if}
</div>

<style>
  .requests-chart {
    flex: 1;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
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
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1em;
  }

  h3 {
    margin-bottom: 20px;
    color: #663399;
  }

  p {
    text-align: center;
    color: #666;
  }

  .loading {
    text-align: center;
    font-size: 1.2em;
    color: #663399;
  }
</style>
