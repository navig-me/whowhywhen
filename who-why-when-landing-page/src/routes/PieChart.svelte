<script>
  import { Pie } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  export let pieChartData = null;
  export let isPieChartLoading = false;

  $: console.log('Chart Data:', pieChartData);
</script>

<div class="pie-chart">
  {#if isPieChartLoading}
    <p class="loading">Loading...</p>
  {:else if pieChartData && pieChartData.labels && pieChartData.datasets}
    <Pie data={pieChartData} options={{
      responsive: true,
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
    margin: 20px;
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
