<script>
    import { onMount } from 'svelte';

    let videoElement;

    onMount(() => {
        if (videoElement) {
            videoElement.playbackRate = 0.5; // Adjust the playback rate as needed
        }
    });
</script>

<div class="video-frame-wrapper">
    <div class="video-frame">
        <video bind:this={videoElement} autoplay muted loop playsinline class="video-content" loading="lazy">
            <source src='/screencap.mp4' type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
</div>

<style>
    .video-frame-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    .video-frame {
        width: 70%;
        height: auto;
        position: relative;
        background: #000; /* Optional: background color for the frame */
        margin-top: -80px; /* Adjust to overlap the Hero section */
        margin-bottom: -50px; /* Adjust to overlap the Feature section */
        z-index: 2;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }

    .video-content {
        width: 100%;
        height: auto;
        border-radius: 10px;
    }
</style>
