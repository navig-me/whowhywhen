<script>
</script>

<div class="integration-steps">
    <h2>Integrate in 3 Easy Steps</h2>
    <div class="steps-container">
        <div class="step">
            <div class="icon-title">
                <i class="fas fa-project-diagram fa-3x"></i>
                <div>
                    <h3>Step 1</h3>
                    <h4>Create a Project</h4>
                </div>
            </div>
            <p class="time">1 min</p>
        </div>
        <div class="arrow">
            <svg width="100" height="50">
                <path d="M0,50 C50,0 50,0 100,50" stroke="#663399" stroke-width="4" stroke-dasharray="5,5" fill="transparent" />
            </svg>
        </div>
        <div class="step">
            <div class="icon-title">
                <i class="fas fa-key fa-3x"></i>
                <div>
                    <h3>Step 2</h3>
                    <h4>Create an API Key</h4>
                </div>
            </div>
            <p class="time">1 min</p>
        </div>
        <div class="arrow">
            <svg width="100" height="50">
                <path d="M0,0 C50,50 50,50 100,0" stroke="#663399" stroke-width="4" stroke-dasharray="5,5" fill="transparent" />
            </svg>
        </div>
        <div class="step">
            <div class="icon-title">
                <i class="fas fa-code fa-3x"></i>
                <div>
                    <h3>Step 3</h3>
                    <h4>Add Middleware in your Code</h4>
                </div>
            </div>
            <p class="time">5 min</p>
        </div>
    </div>
    <a class="learn-more" href="/setup-integration">Learn More</a>
</div>

<style>
    .integration-steps {
        text-align: center;
        padding: 50px 20px;
        background-color: #f9f9f9;
        overflow: hidden;
        position: relative;
    }

    h2 {
        color: #663399;
        margin-bottom: 40px;
        font-size: 2rem;
        position: relative;
        animation: slideIn 1s ease-out forwards;
    }
    
    h2::after {
        content: '';
        display: block;
        width: 50px;
        height: 4px;
        background: #663399;
        margin: 10px auto;
    }

    .steps-container {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        flex-wrap: wrap;
    }

    .step {
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        padding: 15px;
        width: 250px;
        text-align: center;
        position: relative;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 10px;
    }

    .step:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }

    .icon-title {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-direction: column;
        animation: fadeIn 1s ease-out forwards;
    }

    .icon-title .fas {
        color: #663399;
    }

    .icon-title div h3 {
        color: #663399;
        margin: 0;
        font-size: 1.2rem;
    }

    .icon-title div h4 {
        color: #ff4000;
        margin: 0;
        font-size: 1rem;
    }

    .time {
        color: #999;
        font-size: 0.9rem;
        margin-top: 10px;
    }

    .arrow {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .arrow svg path {
        stroke: #663399;
        stroke-width: 4;
        stroke-dasharray: 5,5;
        transition: stroke 0.3s;
    }

    .arrow svg path:last-child {
        stroke: #663399;
    }

    .arrow svg:hover path {
        stroke: #ff4000;
    }

    .learn-more {
        display: inline-block;
        margin-top: 30px;
        padding: 10px 20px;
        background-color: #663399;
        color: #ffffff !important;
        text-decoration: none;
        border-radius: 5px;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .learn-more:hover {
        background-color: #552288;
        transform: scale(1.05);
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @media (max-width: 768px) {
        .steps-container {
            flex-direction: column;
        }

        .arrow {
            display: none;
        }

        .step {
            width: 80%;
        }
    }

    @media (max-width: 480px) {
        h2 {
            font-size: 1.5rem;
        }

        .step {
            padding: 10px;
            width: 90%;
        }

        .icon-title div h3 {
            font-size: 1rem;
        }

        .icon-title div h4 {
            font-size: 0.9rem;
        }

        .learn-more {
            padding: 8px 16px;
            font-size: 0.9rem;
        }
    }
</style>
