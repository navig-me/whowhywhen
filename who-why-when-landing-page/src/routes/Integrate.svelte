<script>
    import { Link } from 'svelte-routing';
    import IntegrationSnippet from '../components/IntegrationSnippet.svelte';
    import { API_BASE_URL } from '../config';

    let apiKey = 'YOUR_API_KEY_HERE';
    let clientIp = 'YOUR_CLIENT_IP_HERE';
    let userAgent = 'YOUR_USER_AGENT_HERE';
    let showSnippetModal = false;
    let showCurlModal = false;
    let curlCommand = '';
    let selectedProxy = '';
    let proxyConfigDescription = '';
    let proxyConfigSnippet = '';

    let requestCode = `
POST /api/log HTTP/1.1
Host: api.whowhywhen.com
X-Api-Key: YOUR_API_KEY
Content-Type: application/json

{
  "url": "URL of the request",
  "ip_address": "IP address of the request",
  "user_agent": "User agent of the request",
  "response_code": "Response code of the request",
  "response_time": "Response time of the request in milliseconds"
}`;

    function openIntegrationSnippet() {
        showSnippetModal = true;
    }

    function closeModal() {
        showSnippetModal = false;
        showCurlModal = false;
    }

    function openCurlModal() {
        curlCommand = `curl -X POST ${API_BASE_URL}/api/log \\
-H "Content-Type: application/json" \\
-H "X-API-KEY: ${apiKey}" \\
-d '{
  "url": "www.whowhywhen.com/whowhywhen-test?q=test",
  "ip_address": "${clientIp}",
  "user_agent": "${userAgent}",
  "response_code": 200
}'`;
        showCurlModal = true;
    }

    function copyToClipboard(content) {
        navigator.clipboard.writeText(content);
        alert('Copied to clipboard');
    }

    const proxyConfigs = {
        traefik: {
            description: `To ensure that the IP address is captured correctly by WhoWhyWhen, you need to configure custom request headers in Traefik:`,
            snippet: `
- "traefik.http.middlewares.real-ip.headers.customrequestheaders.X-Forwarded-For=X-Real-IP,X-Forwarded-For,X-Forwarded-Proto,X-Forwarded-Host,X-Forwarded-Port"
- "traefik.http.routers.frontend.middlewares=real-ip"

# Example of a full configuration for Traefik:
services:
  my-service:
    image: my-image
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.my-router.rule=Host(\`example.com\`)"
      - "traefik.http.services.my-service.loadbalancer.server.port=80"
      - "traefik.http.middlewares.real-ip.headers.customrequestheaders.X-Forwarded-For=X-Real-IP,X-Forwarded-For,X-Forwarded-Proto,X-Forwarded-Host,X-Forwarded-Port"
      - "traefik.http.routers.my-router.middlewares=real-ip"
            `
        },
        nginx: {
            description: `To ensure the correct forwarding of headers for capturing the client's IP address in Nginx:`,
            snippet: `
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://your_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Example of a full configuration for Nginx:
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://your_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
            `
        },
        caddy: {
            description: `To capture the client's IP address correctly in Caddy, configure Caddy with the following settings:`,
            snippet: `
example.com {
    reverse_proxy {
        to http://your_backend
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
}

# Example of a full configuration for Caddy:
example.com {
    reverse_proxy {
        to http://your_backend
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
}
            `
        },
        haproxy: {
            description: `To correctly forward headers in HAProxy:`,
            snippet: `
frontend myfrontend
    bind *:80
    default_backend mybackend

backend mybackend
    server myserver 127.0.0.1:8000
    http-request set-header X-Forwarded-For %[src]
    http-request set-header X-Real-IP %[src]
    http-request set-header X-Forwarded-Proto https if { ssl_fc }

# Example of a full configuration for HAProxy:
frontend myfrontend
    bind *:80
    default_backend mybackend

backend mybackend
    server myserver 127.0.0.1:8000
    http-request set-header X-Forwarded-For %[src]
    http-request set-header X-Real-IP %[src]
    http-request set-header X-Forwarded-Proto https if { ssl_fc }
            `
        }
    };

    $: if (selectedProxy) {
        proxyConfigDescription = proxyConfigs[selectedProxy].description;
        proxyConfigSnippet = proxyConfigs[selectedProxy].snippet;
    }
</script>

<div class="integrate-page">
    <h2>Integrate WhoWhyWhen with Your APIs</h2>
    <button class="btn-open-snippet" on:click={openIntegrationSnippet}>
        <i class="fas fa-code"></i> Sample Code Snippets
    </button>
    <p>Follow these steps to integrate WhoWhyWhen analytics into your APIs:</p>
    <div class="steps">
        <div class="card">
            <div class="icon-title">
                <i class="fas fa-project-diagram fa-3x"></i>
                <h3>Create a Project</h3>
            </div>
            <div class="card-content">
                <p>Go to <Link to="/projects">your projects</Link> and create a new project or view an existing project that you want to enable analytics for.</p>
            </div>
        </div>
        <div class="card">
            <div class="icon-title">
                <i class="fas fa-key fa-3x"></i>
                <h3>Create an API Key</h3>
            </div>
            <div class="card-content">
                <p>Click on "View API Keys" and either copy the API Key or create a new one.</p>
            </div>
        </div>
        <div class="card">
            <div class="icon-title">
                <i class="fas fa-code fa-3x"></i>
                <h3>Add a Middleware in your Code</h3>
            </div>
            <div class="card-content">
                <p>
                    To send logs to WhoWhyWhen, add a middleware to your application. The middleware should make a POST request to <code>https://api.whowhywhen.com/api/log</code> with the following headers and body:
                </p>
                <pre><code>{requestCode}</code></pre>
                <p>It's recommended to do this asynchronously to ensure it doesn't affect your application's performance and latency, and to handle all errors gracefully.</p>
                <div class="button-group">
                    <button class="btn-open-snippet" on:click={openIntegrationSnippet}>
                        <i class="fas fa-code"></i> Sample Code Snippets
                    </button>
                    <button class="btn-open-curl" on:click={openCurlModal}>
                        <i class="fas fa-terminal"></i> Sample cURL Request
                    </button>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="icon-title">
                <i class="fas fa-tachometer-alt fa-3x"></i>
                <h3>Start Using WhoWhyWhen!</h3>
            </div>
            <div class="card-content">
                <p>Start using WhoWhyWhen and view your data in the <Link to="/dashboard">Dashboard</Link>, the <Link to="/bots">Bots</Link> page, or the <Link to="/projects">Projects</Link> page.</p>
                <p>You can view alerts or unusual traffic by clicking on the <Link to="/alerts">Alerts</Link> tab.</p>
            </div>
        </div>
    </div>

    <h3>Using a Proxy?</h3>
    <p>If you are using a reverse proxy, ensure that the middleware is configured correctly to capture and forward the required headers and body.</p>
    <select bind:value={selectedProxy}>
        <option value="" disabled>Select a proxy</option>
        <option value="traefik">Traefik</option>
        <option value="nginx">Nginx</option>
        <option value="caddy">Caddy</option>
        <option value="haproxy">HAProxy</option>
    </select>

    {#if selectedProxy}
        <div class="proxy-config">
            <h4>{selectedProxy} Configuration</h4>
            <p>{proxyConfigDescription}</p>
            <pre>{proxyConfigSnippet}</pre>
            <button class="btn-copy" on:click={() => copyToClipboard(proxyConfigSnippet)}>Copy to Clipboard</button>
        </div>
    {/if}
</div>

{#if showSnippetModal}
    <IntegrationSnippet {apiKey} {clientIp} {userAgent} close={closeModal} />
{/if}

{#if showCurlModal}
    <div class="modal">
        <div class="modal-content">
            <span class="close" on:click={closeModal}>&times;</span>
            <h4>Sample cURL Request</h4>
            <pre>{curlCommand}</pre>
            <button class="btn-copy" on:click={() => copyToClipboard(curlCommand)}>Copy to Clipboard</button>
        </div>
    </div>
{/if}

<style>
    .integrate-page {
        padding: 40px 20px;
        max-width: 900px;
        margin: 0 auto;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        text-align: left;
    }

    h2, h3, h4 {
        color: #663399;
        margin-bottom: 20px;
    }

    p {
        margin-bottom: 20px;
    }

    .steps {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }

    .card {
        flex: 1 1 calc(40% - 20px);
        background: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        text-align: left;
        padding: 20px;
    }

    .icon-title {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }

    .card i {
        color: #663399;
    }

    .btn-open-snippet i, .btn-open-curl i {
        color: #fff;
    }

    .card-content {
        padding: 0 20px;
    }

    code {
        background: #f4f4f4;
        padding: 5px;
        border-radius: 3px;
        display: inline-block;
        margin: 0 3px;
    }

    pre {
        background: #f4f4f4;
        padding: 15px;
        border-radius: 5px;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-x: auto;
        margin: 10px 0;
        max-height: 300px;
    }

    .button-group {
        display: flex;
        gap: 10px;
    }

    select {
        margin: 20px 0;
        padding: 10px;
        font-size: 1rem;
        width: 100%;
    }

    .proxy-config {
        text-align: left;
        background: #f9f9f9;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }

    .proxy-config pre {
        background: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 10px 0;
        max-height: 300px;
        overflow-y: auto;
        text-align: left;
    }

    .btn-open-snippet, .btn-copy, .btn-open-curl {
        background-color: #663399;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 10px;
    }

    .btn-open-snippet:hover, .btn-copy:hover, .btn-open-curl:hover {
        background-color: #7d42a6;
    }

    .modal {
        display: block;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .modal-content {
        background-color: #fff;
        margin: 10% auto;
        padding: 30px;
        border: 1px solid #888;
        width: 80%;
        max-width: 800px;
        border-radius: 10px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        position: relative;
    }

    .close {
        color: #aaa;
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }

    .close:hover, .close:focus {
        color: black;
        text-decoration: none;
    }
</style>
