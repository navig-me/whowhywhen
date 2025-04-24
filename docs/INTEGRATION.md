# WhoWhyWhen Integration Guide

This guide provides instructions for integrating WhoWhyWhen with different types of applications.

## Prerequisites

Before integration, make sure you have:

1. Set up the WhoWhyWhen server
2. Created a user account
3. Created a project
4. Generated an API key

## FastAPI Integration

### Middleware Approach

Add a middleware to your FastAPI application to automatically track all requests:

```python
from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import httpx

class WhoWhyWhenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str, api_url: str):
        super().__init__(app)
        self.api_key = api_key
        self.api_url = api_url

    async def dispatch(self, request: Request, call_next):
        # Record request start time
        start_time = datetime.now()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate request duration in seconds
        duration = (datetime.now() - start_time).total_seconds()
        
        # Get request details
        url = str(request.url)
        method = request.method
        status_code = response.status_code
        user_agent = request.headers.get("User-Agent", "")
        ip_address = request.client.host
        
        # Send data to WhoWhyWhen asynchronously
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{self.api_url}/api/log",
                    headers={"X-API-KEY": self.api_key},
                    json={
                        "url": url,
                        "method": method,
                        "status_code": status_code,
                        "response_time": duration,
                        "user_agent": user_agent,
                        "ip_address": ip_address,
                    },
                    timeout=2.0  # Short timeout to avoid affecting application performance
                )
        except Exception:
            # Fail silently - don't impact the main application if analytics fails
            pass
            
        return response

app = FastAPI()

# Add the middleware to your application
app.add_middleware(
    WhoWhyWhenMiddleware,
    api_key="your-api-key",
    api_url="http://localhost:8001"
)
```

## Express.js Integration

### Middleware Approach

Add a middleware to your Express.js application:

```javascript
const axios = require('axios');

function whoWhyWhenMiddleware(apiKey, apiUrl) {
  return (req, res, next) => {
    const startTime = Date.now();
    
    // Store the original end function
    const originalEnd = res.end;
    
    // Override the end function
    res.end = function(...args) {
      const duration = (Date.now() - startTime) / 1000;  // Convert to seconds
      
      // Call the original end function
      originalEnd.apply(res, args);
      
      // Send analytics data
      axios.post(`${apiUrl}/api/log`, {
        url: req.originalUrl || req.url,
        method: req.method,
        status_code: res.statusCode,
        response_time: duration,
        user_agent: req.headers['user-agent'] || '',
        ip_address: req.ip || req.connection.remoteAddress
      }, {
        headers: {
          'X-API-KEY': apiKey
        },
        timeout: 2000  // 2 second timeout
      }).catch(() => {
        // Fail silently
      });
    };
    
    next();
  };
}

// Add to your Express app
const express = require('express');
const app = express();

app.use(whoWhyWhenMiddleware(
  'your-api-key',
  'http://localhost:8001'
));
```

## Django Integration

### Middleware Approach

Create a middleware in your Django application:

```python
import time
import threading
import requests
from django.utils.deprecation import MiddlewareMixin

class WhoWhyWhenMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.api_key = "your-api-key"
        self.api_url = "http://localhost:8001"
    
    def __call__(self, request):
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Send analytics data in a background thread to avoid affecting response time
        threading.Thread(
            target=self._send_analytics,
            args=(request, response, duration),
            daemon=True
        ).start()
        
        return response
    
    def _send_analytics(self, request, response, duration):
        try:
            requests.post(
                f"{self.api_url}/api/log",
                headers={"X-API-KEY": self.api_key},
                json={
                    "url": request.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "response_time": duration,
                    "user_agent": request.META.get('HTTP_USER_AGENT', ''),
                    "ip_address": request.META.get('REMOTE_ADDR', ''),
                },
                timeout=2.0
            )
        except Exception:
            # Fail silently
            pass
```

Add the middleware to your Django settings:

```python
MIDDLEWARE = [
    # ... other middleware
    'your_app.middleware.WhoWhyWhenMiddleware',
]
```

## Ruby on Rails Integration

### Middleware Approach

Create a middleware in your Rails application:

```ruby
require 'net/http'
require 'uri'
require 'json'

class WhoWhyWhenMiddleware
  def initialize(app, api_key, api_url)
    @app = app
    @api_key = api_key
    @api_url = api_url
  end

  def call(env)
    start_time = Time.now
    
    # Process the request
    status, headers, response = @app.call(env)
    
    # Calculate duration
    duration = Time.now - start_time
    
    # Get request details
    request = Rack::Request.new(env)
    
    # Send analytics in a separate thread
    Thread.new do
      begin
        uri = URI.parse("#{@api_url}/api/log")
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = uri.scheme == 'https'
        http.open_timeout = 1
        http.read_timeout = 1
        
        request = Net::HTTP::Post.new(uri.path, {
          'Content-Type' => 'application/json',
          'X-API-KEY' => @api_key
        })
        
        request.body = {
          url: env['PATH_INFO'],
          method: env['REQUEST_METHOD'],
          status_code: status,
          response_time: duration,
          user_agent: env['HTTP_USER_AGENT'] || '',
          ip_address: env['REMOTE_ADDR'] || ''
        }.to_json
        
        http.request(request)
      rescue
        # Fail silently
      end
    end
    
    [status, headers, response]
  end
end
```

Add the middleware to your Rails application in `config/application.rb`:

```ruby
config.middleware.use WhoWhyWhenMiddleware, 'your-api-key', 'http://localhost:8001'
```

## Advanced Usage

### Tracking Additional Data

You can include additional data in your tracking requests:

```python
# Example with additional data
await client.post(
    f"{self.api_url}/api/log",
    headers={"X-API-KEY": self.api_key},
    json={
        "url": url,
        "method": method,
        "status_code": status_code,
        "response_time": duration,
        "user_agent": user_agent,
        "ip_address": ip_address,
        "user_id": "optional-user-id",
        "session_id": "optional-session-id",
        "custom_data": {
            "feature": "search",
            "params": {"query": "example"}
        }
    }
)
```

### Error Tracking

To specifically track errors:

```python
try:
    # Your code
except Exception as e:
    # Log the error
    requests.post(
        f"{api_url}/api/log",
        headers={"X-API-KEY": api_key},
        json={
            "url": "/your/endpoint",
            "method": "GET",
            "status_code": 500,
            "response_time": 0,
            "user_agent": "",
            "ip_address": "",
            "error": str(e),
            "error_type": e.__class__.__name__,
            "traceback": traceback.format_exc()
        }
    )
    raise
```

## Troubleshooting

### Common Issues

1. **No data appearing in dashboard**
   - Check your API key is correct
   - Verify the API URL is accessible from your application
   - Check for any firewall or network issues

2. **Performance concerns**
   - Use asynchronous requests or background threads to send analytics data
   - Set short timeouts to prevent affecting application performance
   - Consider implementing batch sending for high-traffic applications