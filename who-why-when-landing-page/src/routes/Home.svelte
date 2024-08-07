<script>
    import MainBanner from '../components/MainBanner.svelte';
    import FeatureSection from '../components/FeatureSection.svelte';
    import Questions from '../components/Questions.svelte';
    import Footer from '../components/Footer.svelte';
    import IntegrationSteps from '../components/IntegrationSteps.svelte';
    import GetStartedBanner from '../components/GetStartedBanner.svelte';

    const questions = [
        "Why is my endpoint failing so frequently?",
        "How can I reduce high bot traffic?",
        "Who are the visitors on my app?",
        "Where are my visitors located geographically?",
        "When does my API experience the most failures?",
        "At what times do people visit the most?",
        "Which browsers do my users prefer?",
        "Who are the most active users of my API?",
        "What times of day are the busiest for my API?",
        "When do I get the most error responses?",
        "What is the average response time for my API?",
        "Why should I monitor API performance?",
        "Who are the top users of my service?",
        "What devices are my users using?",
        "Who experiences the most errors on my API?",
        "Why do I need real-time analytics for my API?",
        "Which endpoints are the most popular?",
        "How can I detect and block bots and AI scrapers?",
        "How is bot traffic affecting my API performance?",
        "What strategies can I use to mitigate bot and AI scraper activity?"
    ];
</script>

<div class="page-wrapper">
    <div class="parallax-wrapper">
        <div class="parallax"></div>
        <MainBanner />
    </div>
    <FeatureSection />
</div>
<Questions {questions} />
<IntegrationSteps /> 
<GetStartedBanner />
<Footer />

<style>
    @import '../styles/global.css';

    .page-wrapper {
        position: relative;
    }

    .parallax-wrapper {
        position: relative;
        overflow: hidden;
    }

    .parallax {
        display: none;
    }

    .content-wrapper {
        position: relative;
        z-index: 1;
        padding: 50px 20px;
    }

    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* Dark overlay */
    }

    .container {
        position: relative;
        z-index: 2;
        padding: 50px 20px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    @media (max-width: 768px) {
        .container {
            padding: 20px;
        }
    }

    @media (max-width: 480px) {
        .container {
            padding: 10px;
        }
    }
</style>
