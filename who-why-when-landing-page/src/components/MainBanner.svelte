<script>
    import { navigate } from 'svelte-routing';
    import { onMount } from 'svelte';
    import DeviceRibbon from './DeviceRibbon.svelte';

    let videoElement;

    function changeView(view) {
        navigate(view);
    }

    onMount(() => {
        if (videoElement) {
            videoElement.playbackRate = 0.5; // Adjust the playback rate as needed
        }
    });
</script>

<section class="combined-section">
    <DeviceRibbon />
    <div class="container">
        <div class="content">
            <div class="text-content">
                <h1><span class="supercharge">Supercharge</span> Your APIs, Protect Your Data</h1>
                <p>Get real-time analytics, track bots and AI scrapers, and optimize your resources.</p>
                <button class="btn-primary" on:click={() => changeView('/register')}>START FOR FREE</button>
            </div>
            <div class="video-frame-wrapper">
                <div class="video-frame">
                    <video bind:this={videoElement} autoplay muted loop playsinline class="video-content" loading="lazy">
                        <source src='/screencap.mp4' type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
            <div class="image-wrapper">
                <img src="/devthree.png" alt="Description of image" />
            </div>
        </div>
    </div>
</section>

<style>
    .combined-section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #f8f8f8;
        color: #333;
        padding: 20px 20px;
        text-align: left;
        position: relative;
        background-image: url('https://www.transparenttextures.com/patterns/gplay.png'); /* Light pattern background */
        background-size: 200px 200px; /* Adjust the size to make the pattern more visible */
        opacity: 0.9; /* Adjust the opacity to make the pattern subtle but visible */
    }

    .container {
        max-width: 1200px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .content {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-top: 20px; /* Add margin to separate content from the ribbon */
    }

    .text-content {
        flex: 1;
        max-width: 25%;
    }

    .video-frame-wrapper {
        flex: 1;
        max-width: 50%; /* Adjust the width to balance the layout */
        margin: 0 20px;
    }

    .video-frame {
        width: 100%;
        height: auto;
        position: relative;
        background: #000;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }

    .video-content {
        width: 100%;
        height: auto;
        border-radius: 10px;
    }

    .image-wrapper {
        flex: 1;
        max-width: 25%; /* Adjust the width to balance the layout */
        margin-left: 20px;
    }

    .image-wrapper img {
        width: 100%;
        height: auto;
        border-radius: 10px;
    }

    h1 {
        font-size: 2.5rem;
        margin: 0 0 20px;
    }

    p {
        font-size: 1.2rem;
        margin: 0 0 30px;
    }

    .btn-primary {
        background-color: #ff4000;
        color: #fff;
        padding: 15px 30px;
        border: none;
        border-radius: 30px;
        text-transform: uppercase;
        font-size: 1rem;
        cursor: pointer;
    }

    .supercharge {
        background: linear-gradient(90deg, #ff4000, #ff7300, #ff00d0, #bb01ff, #0073ff);
        background-size: 600%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 5s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @media (max-width: 768px) {
        .content {
            flex-direction: column;
        }

        .text-content, .video-frame-wrapper, .image-wrapper {
            max-width: 100%;
            margin: 0;
            text-align: center;
        }

        h1 {
            font-size: 2rem;
        }

        p {
            font-size: 1rem;
        }

        .btn-primary {
            padding: 10px 20px;
        }
    }

    @media (max-width: 480px) {
        h1 {
            font-size: 1.8rem;
        }

        p {
            font-size: 0.9rem;
        }

        .btn-primary {
            padding: 10px 20px;
            font-size: 0.8rem;
        }
    }
</style>
