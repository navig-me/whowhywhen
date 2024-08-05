<script>
    import { onMount } from 'svelte';
    import { DASH_API_BASE_URL } from '../config';

    let deviceDetails = {
        browser: 'Unknown',
        browser_version: 'Unknown',
        os: 'Unknown',
        os_version: 'Unknown',
        device: 'Unknown',
        is_mobile: false,
        is_tablet: false,
        is_pc: false,
        is_bot: false,
    };

    let error = null;

    onMount(async () => {
        try {
            const response = await fetch(`${DASH_API_BASE_URL}/dashapi/device-details`);
            if (response.ok) {
                deviceDetails = await response.json();
                console.log('Device details:', deviceDetails);  // Log the response to check its content
            } else {
                error = 'Failed to fetch device details';
            }
        } catch (err) {
            error = 'Error fetching device details';
            console.error(err);  // Log the error to check what went wrong
        }
    });
</script>

<div class="ribbon">
    <div class="container">
        <div class="text-info">
            {#if error}
                <p class="error">{error}</p>
            {:else}
                <div class="info">
                    {#if !(deviceDetails.browser === 'Unknown' &&
                           deviceDetails.browser_version === 'Unknown' &&
                           deviceDetails.os === 'Unknown' &&
                           deviceDetails.os_version === 'Unknown' &&
                           deviceDetails.device === 'Unknown')}
                        <div class="icon-text">
                            <div class="icon-container">
                                {#if deviceDetails.is_mobile}
                                    <i class="fas fa-mobile-alt"></i>
                                {:else if deviceDetails.is_tablet}
                                    <i class="fas fa-tablet-alt"></i>
                                {:else if deviceDetails.is_pc}
                                    <i class="fas fa-desktop"></i>
                                {:else if deviceDetails.is_bot}
                                    <i class="fas fa-robot"></i>
                                {:else}
                                    <i class="fas fa-question-circle"></i>
                                {/if}
                            </div>
                            <p class="device-info">
                                You are viewing this site on a <strong>{deviceDetails.browser}</strong> <em>{deviceDetails.browser_version}</em> browser running <strong>{deviceDetails.os}</strong> <em>{deviceDetails.os_version} ({deviceDetails.device})</em>.
                            </p>
                        </div>
                    {/if}
                    <p class="description">
                        Understand your users. Detect <span class="highlight">bots</span>, <span class="highlight">scrapers</span>, <span class="highlight">users</span>, and <span class="highlight">devices</span> accessing your APIs, and <span class="highlight big">answer key questions</span> about <span class="highlight">performance</span>.
                    </p>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    .ribbon {
        width:70%;
        background: rgba(0, 0, 0, 0.5); /* Make background semi-transparent to blend with banner */
        color: white;
        padding: 10px 0; /* Adjust padding to fit nicely within the banner */
        font-size: 14px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        align-items: center;
    }
    .text-info {
        flex: 2;
        display: flex;
        flex-direction: column;
        gap: 8px;
        text-align: center; /* Center-align text for consistency */
    }
    .info {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .icon-text {
        display: flex;
        align-items: center;
        gap: 10px;
        justify-content: center; /* Center align icon and text */
    }
    .icon-container {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    .icon-container i {
        font-size: 16px;
    }
    .device-info {
        font-size: 16px;
        font-weight: 600;
    }
    .description {
        font-size: 14px;
        max-width: 800px;
        line-height: 1.5;
        font-weight: 500;
    }
    .highlight {
        color: #ffd700;
        font-weight: 700;
    }
    .highlight.big {
        font-size: 1.2em;
    }
    .error {
        color: #ff4000;
        font-weight: bold;
    }
</style>