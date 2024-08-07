<script>
    import { navigate } from 'svelte-routing';
    import DeviceRibbon from './DeviceRibbon.svelte';

    function changeView(view) {
        navigate(view);
    }
</script>

<section class="combined-section">
    <div class="container">
        <div class="content">
            <div class="text-content">
                <h1><span class="supercharge">Supercharge</span> Your APIs, Protect Your Data</h1>
                <p>Get real-time analytics, track bots and AI scrapers, and optimize your resources.</p>
                <button class="btn-primary" on:click={() => changeView('/register')}>START FOR FREE</button>
            </div>
            <div class="image-wrapper">
                <img src="/devthree.png" alt="Description of image" />
            </div>
        </div>
    </div>
    <DeviceRibbon />
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
    }

    .text-content {
        flex: 2;
        margin-right: 20px;
    }

    .image-wrapper {
        flex: 1;
        max-width: 30%;
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

        .text-content, .image-wrapper {
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
