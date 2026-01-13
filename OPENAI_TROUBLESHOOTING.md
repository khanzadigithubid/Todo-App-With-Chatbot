# OpenAI Integration Troubleshooting Guide

## Common Issues and Solutions

### 1. Connection Error (httpx.ConnectError: [Errno 11001] getaddrinfo failed)

**Problem**: The application cannot connect to OpenAI's API servers.

**Solutions**:
- Check your internet connection
- Verify your firewall/proxy settings allow outbound connections to api.openai.com
- Ensure your network allows HTTPS traffic on port 443

### 2. Invalid API Key

**Problem**: AuthenticationError or 401 Unauthorized.

**Solutions**:
- Verify your API key at https://platform.openai.com/api-keys
- Ensure the API key is correctly set in your environment variables
- Check for any leading/trailing spaces in the API key

### 3. Rate Limiting

**Problem**: RateLimitError or 429 status code.

**Solutions**:
- Check your OpenAI usage at https://platform.openai.com/usage
- Consider upgrading your plan if you're exceeding limits
- Implement retry logic with exponential backoff

## Environment Setup

### Setting up Environment Variables

1. Create a `.env` file in your project root
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

### Loading Environment Variables in Development

For local development, you can load environment variables using python-dotenv:

```bash
pip install python-dotenv
```

Then in your main.py or wherever you start your application:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
```

## Testing the Connection

To test if your OpenAI setup is working correctly, you can run this simple test:

```python
from openai import OpenAI
import os

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY environment variable not set")
else:
    client = OpenAI(api_key=api_key)
    
    try:
        # Simple test: list available models
        models = client.models.list()
        print("Connection successful! Available models:")
        for model in models.data:
            print(f"- {model.id}")
    except Exception as e:
        print(f"Connection failed: {e}")
```

## Network Configuration for Windows

If you're on a corporate network or using a VPN, you might need to configure proxy settings:

```python
from openai import OpenAI
import os

# If using a proxy
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(proxy="http://your-proxy:port")
)
```

## Best Practices

1. Never commit API keys to version control
2. Use environment variables for sensitive data
3. Implement proper error handling for API failures
4. Log errors appropriately without exposing sensitive information
5. Consider implementing a fallback mechanism if the AI service is unavailable