<script>
  import { Pie } from 'svelte-chartjs';
  import { Chart, registerables } from 'chart.js';

  Chart.register(...registerables);

  export let pieChartData = null;
  export let isPieChartLoading = false;

  // Function to sort the pie chart data
  function sortPieChartData(data) {
    if (data && data.labels && data.datasets && data.datasets[0] && data.datasets[0].data) {
      const labels = data.labels.slice();
      const values = data.datasets[0].data.slice();

      // Create an array of objects containing labels and values
      const combined = labels.map((label, index) => {
        return { label, value: values[index] };
      });

      // Sort the array by value in descending order
      combined.sort((a, b) => b.value - a.value);

      // Separate the sorted labels and values
      const sortedLabels = combined.map(item => item.label);
      const sortedValues = combined.map(item => item.value);

      return {
        ...data,
        labels: sortedLabels,
        datasets: [
          {
            ...data.datasets[0],
            data: sortedValues,
            backgroundColor: data.datasets[0].backgroundColor
          }
        ]
      };
    }

    return data;
  }

  // Function to truncate text with ellipses
  function truncateText(text, maxLength) {
    return text.length > maxLength ? text.substring(0, maxLength - 3) + '...' : text;
  }

  // Sort the pie chart data
  let sortedPieChartData = sortPieChartData(pieChartData);

  // Watch for changes to pieChartData and sort it again if it changes
  $: sortedPieChartData = sortPieChartData(pieChartData);
</script>

<div class="pie-chart">
  {#if isPieChartLoading}
    <p class="loading">Loading...</p>
  {:else if sortedPieChartData && sortedPieChartData.labels && sortedPieChartData.datasets}
    <div class="chart-container">
      <Pie data={sortedPieChartData} options={{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#666',
              font: {
                size: 12,
                weight: 'bold',
              },
              boxWidth: 20,
              padding: 15,
              usePointStyle: true,
              generateLabels: (chart) => {
                const data = chart.data;
                if (data.labels.length && data.datasets.length) {
                  return data.labels.map((label, i) => {
                    const value = data.datasets[0].data[i];
                    const backgroundColor = data.datasets[0].backgroundColor[i];
                    return {
                      text: truncateText(label, 30), // Truncate label text to 15 characters
                      fillStyle: backgroundColor,
                      hidden: isNaN(data.datasets[0].data[i]) || chart.getDatasetMeta(0).data[i].hidden,
                      lineCap: 'butt',
                      lineDash: [],
                      lineDashOffset: 0,
                      lineJoin: 'miter',
                      strokeStyle: 'transparent',
                      pointStyle: 'circle',
                      rotation: 0
                    };
                  });
                }
                return [];
              }
            }
          },
          title: {
            display: true,
            text: sortedPieChartData.title,
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
    flex-direction: column;
  }

  .chart-container canvas {
    max-width: 100%;
    max-height: 70%;
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
