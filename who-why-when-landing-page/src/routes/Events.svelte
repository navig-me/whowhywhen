<script>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import { DASH_API_BASE_URL } from '../config';
    
    let events = [];
    let activeTab = 'bots'; // Default to 'bots' tab
    let loading = true;
  
    async function fetchEvents(type) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashapi/events?type_filter=${type}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        if (response.ok) {
          return await response.json();
        } else {
          console.error('Failed to fetch events:', response.statusText);
          return [];
        }
      } catch (error) {
        console.error('Error fetching events:', error);
        return [];
      }
    }
  
    async function loadEvents(type) {
      loading = true;
      events = await fetchEvents(type);
      loading = false;
    }
  
    function handleTabChange(tab) {
      activeTab = tab;
      loadEvents(tab);
    }
  
    function handleEventClick(event) {
      if (activeTab === 'bots') {
        navigate(`/bots?bot_id=${event.bot_id}`);
      } else if (activeTab === 'endpoints') {
        navigate(`/dashboard?endpoint=${event.endpoint}`);
      }
    }
  
    onMount(() => {
      loadEvents(activeTab);
    });
  </script>
  
  <section class="events-section">
    <div class="container">
      <h2>Events</h2>
      <div class="tabs">
        <button class={`tab ${activeTab === 'bots' ? 'active' : ''}`} on:click={() => handleTabChange('bots')}>New Bots</button>
        <button class={`tab ${activeTab === 'endpoints' ? 'active' : ''}`} on:click={() => handleTabChange('endpoints')}>New Endpoints</button>
      </div>
      {#if loading}
        <p>Loading...</p>
      {:else}
        <div class="timeline">
          {#each events as event}
            <div class="timeline-item" on:click={() => handleEventClick(event)}>
              <div class="timeline-content">
                <p>{activeTab === 'bots' ? `Bot ID: ${event.bot_id}` : `Endpoint: ${event.path}`}</p>
                <span class="date">{new Date(event.created).toLocaleString()}</span>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </section>
  
  <style>
    .events-section {
      padding: 40px 20px;
      text-align: center;
    }
  
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
  
    .tabs {
      display: flex;
      justify-content: center;
      margin-bottom: 20px;
    }
  
    .tab {
      padding: 10px 20px;
      cursor: pointer;
      border: none;
      background-color: #f1f1f1;
      margin: 0 5px;
      transition: background-color 0.3s;
      font-size: 1rem;
    }
  
    .tab.active {
      background-color: #663399;
      color: #fff;
    }
  
    .timeline {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  
    .timeline-item {
      width: 100%;
      max-width: 600px;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 5px;
      margin-bottom: 10px;
      cursor: pointer;
      transition: background-color 0.3s;
    }
  
    .timeline-item:hover {
      background-color: #f1f1f1;
    }
  
    .timeline-content {
      text-align: left;
    }
  
    .date {
      display: block;
      color: #888;
      font-size: 0.8rem;
      margin-top: 5px;
    }
  </style>
  