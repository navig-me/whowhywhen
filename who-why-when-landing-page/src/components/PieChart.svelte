<script>
    import { Pie } from 'svelte-chartjs';
    import { Chart, registerables } from 'chart.js';
  
    Chart.register(...registerables);
  
    export let chartData = null;
    export let isChartLoading = false;
  </script>
  
  <div class="pie-chart">
    {#if isChartLoading}
      <p class="loading">Loading...</p>
    {:else if chartData}
      <Pie data={chartData} options={{
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
            text: chartData.title,
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
  