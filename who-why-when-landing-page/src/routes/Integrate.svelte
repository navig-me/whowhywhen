<script>
    import { Link } from 'svelte-routing';
    import IntegrationSnippet from '../components/IntegrationSnippet.svelte';

    let apiKey = 'YOUR_API_KEY_HERE';
    let clientIp = 'YOUR_CLIENT_IP_HERE';
    let userAgent = 'YOUR_USER_AGENT_HERE';
    let showSnippetModal = false;
    let selectedProxy = '';
    let proxyConfigDescription = '';
    let proxyConfigSnippet = '';

    function openIntegrationSnippet() {
        showSnippetModal = true;
    }

    function closeModal() {
        showSnippetModal = false;
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
    <p>Follow these steps to integrate WhoWhyWhen analytics into your APIs:</p>
    <ol>
        <li>Go to <Link to="/projects">your projects</Link> and create a new project or view an existing project that you want to enable analytics for.</li>
        <li>Click on "View API Keys" and either copy the API Key or create a new one.</li>
        <li>
            Add a middleware to your application to send logs to the URL 
            <code>https://api.whowhywhen.com/api/log</code> 
            with the appropriate headers and request body. It is recommended to do this asynchronously to ensure that it does not affect the performance and latency of your application, and to handle all errors gracefully. The middleware should capture details of each request, including the URL, IP address, user agent, response code, and response time. The following request body parameters are required:
            <ol>
                <li>url: The URL of the request.</li>
                <li>ip_address: The IP address of the request.</li>
                <li>user_agent: The user agent of the request.</li>
                <li>response_code: The response code of the request.</li>
                <li>response_time: The response time of the request in milliseconds.</li>
            </ol>
            The middleware should make a POST request with this data to the WhoWhyWhen API.
        </li>
        <li>If you are using a reverse proxy, ensure that the middleware is configured correctly to capture and forward the required headers and body.</li>
    </ol>
    <button class="btn-open-snippet" on:click={openIntegrationSnippet}>Sample Code Snippets</button>

    <h3>Using a Proxy?</h3>
    <p>Select your reverse proxy service to view the additional configuration steps to ensure that the IP address is captured correctly.</p>
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

    ol {
        text-align: left;
        margin-bottom: 20px;
        padding-left: 20px;
    }

    li {
        margin-bottom: 10px;
    }

    .btn-open-snippet {
        background-color: #663399;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 10px;
    }

    .btn-open-snippet:hover {
        background-color: #7d42a6;
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

    .btn-copy {
        background-color: #663399;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: 10px;
    }

    .btn-copy:hover {
        background-color: #7d42a6;
    }
</style>
