<script>
    import { Bar, Pie } from 'svelte-chartjs';
    import { Chart, registerables } from 'chart.js';

    Chart.register(...registerables);

    export let topBotsData = [];
    export let isBotDataLoading = false;
    let isCollapsed = true;

    function toggleCollapse() {
        isCollapsed = !isCollapsed;
    }

    function getFavicon(url) {
        const hostname = new URL(url).hostname;
        return `https://www.google.com/s2/favicons?sz=64&domain=${hostname}`;
    }

    function createPieChartData(responseStatuses) {
        return {
            labels: Object.keys(responseStatuses),
            datasets: [{
                data: Object.values(responseStatuses),
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        };
    }

    function createBarChartData(endpoints) {
        return {
            labels: endpoints.map(endpoint => endpoint.path),
            datasets: [{
                data: endpoints.map(endpoint => endpoint.count),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };
    }

    function formatLastSeen(lastSeen) {
        const now = new Date().getTime();
        const lastSeenDate = new Date(lastSeen).getTime();
        const diff = now - lastSeenDate;

        const minutes = Math.floor(diff / 1000 / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 0) return `${days} days ago`;
        if (hours > 0) return `${hours} hours ago`;
        if (minutes > 0) return `${minutes} minutes ago`;
        return `just now`;
    }
</script>

{#if isBotDataLoading}
    <p>Loading...</p>
{:else}
    <div class="bot-highlights">
        <h3 on:click={toggleCollapse} class="collapsible-header">
            Top 10 Bots
            <span class="arrow">{isCollapsed ? '▼' : '▲'}</span>
        </h3>
        {#if !isCollapsed}
            <div class="bot-cards">
                {#each topBotsData as bot}
                    <div class="bot-card">
                        <div class="bot-header">
                            <img src={getFavicon(bot.bot_website)} alt="Favicon" />
                            <div class="bot-info">
                                <h4>{bot.bot_name} <br/><small style="font-size: x-small;">
                                    <i>Last seen: {bot.last_seen_text}</i>
                                </small></h4>
                                <a href={bot.bot_website} target="_blank" rel="noopener noreferrer">{bot.bot_website}</a>
                                <p><small>{bot.total_api_calls} calls within selected time range</small></p>
                            </div>
                            <div class="pie-chart-container">
                                <Pie data={createPieChartData(bot.top_response_statuses)} />
                            </div>
                        </div>
                        <div class="bot-details">
                            <p>Top Endpoints:</p>
                            <div class="bar-chart-container">
                                <Bar data={createBarChartData(bot.last_10_endpoints)} options={{
                                    indexAxis: 'y',
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: {
                                        legend: {
                                            display: false
                                        },
                                        tooltip: {
                                            callbacks: {
                                                label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw}`
                                            }
                                        }
                                    },
                                    scales: {
                                        x: {
                                            beginAtZero: true
                                        }
                                    }
                                }} />
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
{/if}

<style>
    .bot-highlights {
        text-align: center;
        margin-bottom: 20px;
        background-color: #f5f5f5; /* Light background for the section */
        padding: 20px;
        border-radius: 10px;
    }

    .collapsible-header {
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #e0e0e0; /* Light background for the header */
        padding: 10px;
        border-radius: 5px;
    }

    .arrow {
        margin-left: 10px;
        font-size: 0.8em;
    }

    .bot-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 10px; /* Added margin to separate from header */
    }

    .bot-card {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        text-align: left;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .bot-header {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .bot-info {
        flex-grow: 1;
        max-width: 200px; /* Fixed width for left side part */
    }

    .bot-card img {
        width: 32px;
        height: 32px;
    }

    .bot-card h4 {
        margin: 0;
        font-size: 1.2em;
        color: #333;
    }

    .bot-card a {
        color: #663399;
        text-decoration: none;
        font-size: 0.9em;
        word-break: break-all; /* Prevent overflow for long URLs */
    }

    .bot-card a:hover {
        text-decoration: underline;
    }

    .bot-details {
        margin-top: 10px;
    }

    .bot-details p {
        font-weight: bold;
        margin: 10px 0;
    }

    .bar-chart-container {
        height: 150px; /* Adjust height as needed */
    }

    .pie-chart-container {
        width: 100px;
        height: 100px;
        flex-shrink: 0;
    }
</style>
