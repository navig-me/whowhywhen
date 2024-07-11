<script>
  import { Bar, Line } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';
  import { createEventDispatcher } from 'svelte';

  Chart.register(...registerables);

  export let barChartData = null;
  export let frequency = "hour";
  export let isChartLoading = false;
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
  {#if isChartLoading}
    <p class="loading">Loading...</p>
  {:else if barChartData}
    <div class="chart-container">
      <Bar
        data={barChartData}
        options={{
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Request Count',
                color: '#666',
                font: {
                  size: 14,
                  weight: 'bold',
                }
              },
              grid: {
                color: 'rgba(200, 200, 200, 0.2)',
              },
            },
            y1: {
              beginAtZero: true,
              position: 'right',
              grid: {
                drawOnChartArea: false,
                color: 'rgba(200, 200, 200, 0.2)',
              },
              title: {
                display: true,
                text: 'Average Response Time (s)',
                color: '#666',
                font: {
                  size: 14,
                  weight: 'bold',
                }
              }
            },
            x: {
              grid: {
                color: 'rgba(200, 200, 200, 0.2)',
              },
            },
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: '#666',
                font: {
                  size: 12,
                  weight: 'bold',
                }
              }
            },
            title: {
              display: true,
              text: `Requests per ${frequency.charAt(0).toUpperCase() + frequency.slice(1)}`,
              color: '#333',
              font: {
                size: 16,
                weight: 'bold',
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              titleFont: {
                size: 14,
                weight: 'bold',
              },
              bodyFont: {
                size: 12,
              },
              bodySpacing: 4,
              padding: 10,
              cornerRadius: 4,
              caretSize: 6,
            },
          },
          elements: {
            line: {
              tension: 0.4,
            },
            point: {
              radius: 4,
              backgroundColor: '#fff',
              borderWidth: 2,
            }
          }
        }}
      />
    </div>
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
    font-weight: bold;
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

  .chart-container {
    position: relative;
    width: 100%;
    height: 400px; /* Ensure the chart has a minimum height */
  }

  @media (max-width: 768px) {
    .chart-controls {
      justify-content: center;
      margin-bottom: 20px;
    }

    .chart-container {
      height: 300px;
    }
  }

  @media (max-width: 480px) {
    .chart-controls {
      justify-content: center;
      margin-bottom: 20px;
    }

    .chart-container {
      height: 250px;
    }
  }
</style>
