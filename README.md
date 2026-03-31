# Simple API Key Rotator

When APIs have strict rate limits, you can sometimes unblock your use case by using multiple API keys.

The idea is simple: every time you hit the rate limit, record the usage and pick the next available key.

This works best for personal use cases when the amount of API traffic is low.