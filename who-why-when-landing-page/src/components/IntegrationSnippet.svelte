<script>
    export let apiKey = '';
    export let clientIp = '';
    export let userAgent = '';
    export let close;

    let selectedLanguage = 'FastAPI';

    const snippets = {
        FastAPI: {
            description: `Integrate WhoWhyWhen as a middleware in your FastAPI application. Tasks related to WhoWhyWhen are done asynchronously in the background, ensuring minimal latency impact on your API performance.`,
            code: `
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTasks
import time
import httpx
import logging

logger = logging.getLogger(__name__)

class WhoWhyWhenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        response_time = time.time() - start_time
        
        log_data = {
            "url": str(request.url),
            "ip_address": request.headers.get("X-Forwarded-For", request.client.host),
            "user_agent": f"{request.headers.get('User-Agent', '')}",
            "response_code": response.status_code,
            "response_time": response_time
        }
        
        # Add the background task to send the log
        request.state.background_tasks.add_task(self.send_log_to_whowhywhen, log_data)
        
        return response
    
    async def send_log_to_whowhywhen(self, log_data):
        whowhywhen_api_url = "https://api.whowhywhen.com/api/log"
        headers = {"X-Api-Key": "${apiKey}"}
        
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    whowhywhen_api_url,
                    headers=headers,
                    json=log_data,
                    timeout=2  # Adjust the timeout as needed
                )
            except httpx.HTTPStatusError as exc:
                logger.error(f"Error sending log to WhoWhyWhen: {exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                logger.error(f"Error sending log to WhoWhyWhen: {str(exc)}")

app = FastAPI()
app.add_middleware(WhoWhyWhenMiddleware)

@app.middleware("http")
async def add_background_tasks(request: Request, call_next):
    request.state.background_tasks = BackgroundTasks()
    response = await call_next(request)
    response.background = request.state.background_tasks
    return response
            `
        },
        Django: {
            description: `Integrate WhoWhyWhen as a middleware in your Django application to log API requests and performance metrics asynchronously.`,
            code: `
import time
import httpx
import logging
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger(__name__)

class WhoWhyWhenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        response_time = time.time() - getattr(request, 'start_time', time.time())

        log_data = {
            "url": request.build_absolute_uri(),
            "ip_address": request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')),
            "user_agent": request.META.get('HTTP_USER_AGENT', ''),
            "response_code": response.status_code,
            "response_time": response_time
        }

        self.send_log_to_whowhywhen(log_data)
        
        return response

    def send_log_to_whowhywhen(self, log_data):
        whowhywhen_api_url = "https://api.whowhywhen.com/api/log"
        headers = {"X-Api-Key": "${apiKey}"}

        async def send_log():
            async with httpx.AsyncClient() as client:
                try:
                    await client.post(
                        whowhywhen_api_url,
                        headers=headers,
                        json=log_data,
                        timeout=2  # Adjust the timeout as needed
                    )
                except httpx.HTTPStatusError as exc:
                    logger.error(f"Error sending log to WhoWhyWhen: {exc.response.status_code} - {exc.response.text}")
                except Exception as exc:
                    logger.error(f"Error sending log to WhoWhyWhen: {str(exc)}")

        import asyncio
        asyncio.run(send_log())
            `
        },
        Flask: {
            description: `Integrate WhoWhyWhen as a middleware in your Flask application to log API requests and performance metrics asynchronously.`,
            code: `
from flask import Flask, request, g
import time
import httpx
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    response_time = time.time() - g.start_time

    log_data = {
        "url": request.url,
        "ip_address": request.headers.get("X-Forwarded-For", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
        "response_code": response.status_code,
        "response_time": response_time
    }

    send_log_to_whowhywhen(log_data)
    
    return response

def send_log_to_whowhywhen(log_data):
    whowhywhen_api_url = "https://api.whowhywhen.com/api/log"
    headers = {"X-Api-Key": "${apiKey}"}

    async def send_log():
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    whowhywhen_api_url,
                    headers=headers,
                    json=log_data,
                    timeout=2  # Adjust the timeout as needed
                )
            except httpx.HTTPStatusError as exc:
                logger.error(f"Error sending log to WhoWhyWhen: {exc.response.status_code} - {exc.response.text}")
            except Exception as exc:
                logger.error(f"Error sending log to WhoWhyWhen: {str(exc)}")

    import asyncio
    asyncio.run(send_log())
            `
        },
        SpringBoot: {
            description: `Integrate WhoWhyWhen as a middleware in your Spring Boot application to log API requests and performance metrics asynchronously.`,
            code: `
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.time.Instant;
import java.util.concurrent.CompletableFuture;
import org.springframework.web.client.RestTemplate;

@Component
public class WhoWhyWhenFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {
        long startTime = Instant.now().toEpochMilli();

        filterChain.doFilter(request, response);

        long responseTime = Instant.now().toEpochMilli() - startTime;

        String logData = String.format("{\\"url\\": \\"%s\\", \\"ip_address\\": \\"%s\\", \\"user_agent\\": \\"%s\\", \\"response_code\\": %d, \\"response_time\\": %d}",
                request.getRequestURL().toString(),
                request.getRemoteAddr(),
                request.getHeader("User-Agent"),
                response.getStatus(),
                responseTime);

        CompletableFuture.runAsync(() -> sendLogToWhoWhyWhen(logData));
    }

    private void sendLogToWhoWhyWhen(String logData) {
        String whowhywhenApiUrl = "https://api.whowhywhen.com/api/log";
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.set("X-Api-Key", "${apiKey}");
        HttpEntity<String> entity = new HttpEntity<>(logData, headers);
        try {
            restTemplate.postForEntity(whowhywhenApiUrl, entity, String.class);
        } catch (Exception e) {
            // Handle the exception
        }
    }
}
            `
        },
        Node: {
            description: `Integrate WhoWhyWhen as a middleware in your Node.js application to log API requests and performance metrics asynchronously.`,
            code: `
const express = require('express');
const app = express();
const axios = require('axios');

app.use(async (req, res, next) => {
    const startTime = Date.now();

    res.on('finish', async () => {
        const responseTime = Date.now() - startTime;

        const logData = {
            url: req.originalUrl,
            ip_address: req.headers['x-forwarded-for'] || req.connection.remoteAddress,
            user_agent: req.headers['user-agent'],
            response_code: res.statusCode,
            response_time: responseTime
        };

        try {
            await axios.post('https://api.whowhywhen.com/api/log', logData, {
                headers: {
                    'X-Api-Key': '${apiKey}'
                }
            });
        } catch (error) {
            console.error('Error sending log to WhoWhyWhen:', error.response ? error.response.status : error.message);
        }
    });

    next();
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
            `
        }
    };

    function copyToClipboard() {
        const snippet = snippets[selectedLanguage].code;
        navigator.clipboard.writeText(snippet);
    }
</script>

<div class="modal">
    <div class="modal-content">
        <span class="close" on:click={close}>&times;</span>
        <h3>Integration Snippet</h3>
        <p>Select your framework or library to view the integration snippet.</p>
        <select bind:value={selectedLanguage}>
            <option value="FastAPI">FastAPI (Python)</option>
            <option value="Django">Django (Python)</option>
            <option value="Flask">Flask (Python)</option>
            <option value="SpringBoot">Spring Boot (Java)</option>
            <option value="Node">Node.js</option>
        </select>
        <p>{snippets[selectedLanguage].description}</p>
        <div class="code-container">
            <pre>{snippets[selectedLanguage].code}</pre>
        </div>
        <button class="btn-copy" on:click={copyToClipboard}>Copy to Clipboard</button>
    </div>
</div>

<style>
    .modal {
        display: block;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.6);
    }

    .modal-content {
        background-color: #fff;
        margin: 5% auto;
        padding: 20px;
        border: 1px solid #888;
        width: 80%;
        max-width: 600px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        position: relative;
    }

    .close {
        color: #aaa;
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }

    .close:hover, .close:focus {
        color: #000;
        text-decoration: none;
        cursor: pointer;
    }

    .code-container {
        background: #f4f4f4;
        padding: 15px;
        border-radius: 5px;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 10px 0;
        max-height: 300px;
        overflow-y: auto;
        text-align: left;
        font-family: monospace;
    }

    pre {
        margin: 0;
    }

    select {
        margin: 10px 0;
        padding: 10px;
        font-size: 1rem;
        width: 100%;
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
        display: block;
        width: 100%;
        font-size: 1rem;
        text-align: center;
    }

    .btn-copy:hover {
        background-color: #7d42a6;
    }

    h3 {
        margin-bottom: 10px;
        color: #333;
    }

    p {
        color: #555;
        font-size: 1rem;
        margin-bottom: 20px;
    }
</style>
