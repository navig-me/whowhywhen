<script>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import { DASH_API_BASE_URL } from '../config';
    import { selectedProjectIdStore } from '../stores/userStore';

    let alerts = [];
    let currentPage = 1;
    let totalPages = 1;
    let isLoading = true;

    async function fetchAlerts(page = 1) {
        isLoading = true;
        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashapi/alerts?page=${page}&limit=10`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            alerts = data.results;
            totalPages = Math.ceil(data.total / 10);
        } else if (response.status === 401) {
            navigate('/login');
        }
        isLoading = false;
    }

    function handleNotificationClick(projectId) {
        selectedProjectIdStore.set(projectId); // Update the selected project ID
        navigate('/dashboard'); // Navigate to the dashboard
    }

    function nextPage() {
        if (currentPage < totalPages) {
            currentPage++;
            fetchAlerts(currentPage);
        }
    }

    onMount(() => {
        fetchAlerts(currentPage);
    });
</script>

{#if isLoading}
    <p>Loading...</p>
{:else}
    <section class="alerts-section">
        <div class="container">
            <h2>Alerts</h2>
            <div class="timeline">
                {#each alerts as alert}
                    <div class="timeline-item" on:click={() => handleNotificationClick(alert.user_project_id)}>
                        <div class="timeline-marker">
                            <span class="date">{alert.created_text}</span>
                            <div class="dot"></div>
                        </div>
                        <div class="timeline-content">
                            <h3>{alert.user_project_name}</h3>
                            <p>{alert.description}</p>
                        </div>
                    </div>
                {/each}
            </div>
            {#if currentPage < totalPages}
                <button on:click={nextPage} class="next-button">Next</button>
            {/if}
        </div>
    </section>
{/if}

<style>
    .alerts-section {
        padding: 20px 0;
        text-align: center;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
    }

    h2 {
        margin-bottom: 20px;
        font-size: 2rem;
        color: #663399;
    }

    .timeline {
        position: relative;
        margin: 0 auto;
        padding: 10px 0;
        width: 100%;
    }

    .timeline::before {
        content: '';
        position: absolute;
        top: 0;
        bottom: 0;
        left: 30px; /* Adjust the position to match the dot */
        width: 2px;
        background: #ddd;
    }

    .timeline-item {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        cursor: pointer;
        transition: background 0.3s;
    }

    .timeline-item:hover .timeline-content {
        background: #f1f1f1;
    }

    .timeline-marker {
        display: flex;
        align-items: center;
        position: relative;
        margin-right: 20px;
        min-width: 150px; /* Adjust this value to ensure enough space for the date */
    }

    .dot {
        width: 10px;
        height: 10px;
        background: #ff4000;
        border-radius: 50%;
        position: absolute;
        left: 30px; /* Position on the timeline line */
        transform: translateX(-50%);
    }

    .date {
        font-size: 0.8rem;
        color: #888;
        margin-right: 10px;
        position: absolute;
        left: -140px; /* Adjust this value to position the date properly */
        white-space: nowrap;
    }

    .timeline-content {
        padding: 10px 20px;
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        flex: 1;
        text-align: left;
    }

    .timeline-content h3 {
        margin: 0 0 5px;
        font-size: 1.2rem;
        color: #663399;
    }

    .timeline-content p {
        margin: 0;
        color: #555;
    }

    .next-button {
        margin-top: 20px;
        padding: 10px 20px;
        font-size: 1rem;
        color: #fff;
        background: #ff4000;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background 0.3s;
    }

    .next-button:hover {
        background: #e63900;
    }
</style>
