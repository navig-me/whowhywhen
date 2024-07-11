<script>
  import { Pie } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  export let pieChartData = null;
  export let isPieChartLoading = false;
</script>

<div class="pie-chart">
  {#if isPieChartLoading}
    <p class="loading">Loading...</p>
  {:else if pieChartData && pieChartData.labels && pieChartData.datasets}
    <div class="chart-container">
      <Pie data={pieChartData} options={{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#666',
              font: {
                size: 12,
                weight: 'bold',
              },
              boxWidth: 20,
              padding: 15,
              usePointStyle: true,
            }
          },
          title: {
            display: true,
            text: pieChartData.title,
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
        }
      }} />
    </div>
  {:else}
    <p>No data available</p>
  {/if}
</div>

<style>
  .pie-chart {
    flex: 1;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 450px;
  }

  .chart-container {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .chart-container canvas {
    max-width: 60%;
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

  .chartjs-legend {
    max-height: 400px;
    overflow-y: auto;
  }
</style>
