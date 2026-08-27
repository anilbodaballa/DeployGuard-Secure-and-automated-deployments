#!/usr/bin/env python3
"""
DeployGuard Production Health Check Script
Polls the health endpoint until the service is healthy or timeout is reached.
"""
import argparse, sys, time, urllib.request, urllib.error
from datetime import datetime

# Hardcoded default values
DEFAULT_TIMEOUT = 300
DEFAULT_INTERVAL = 10
DEFAULT_EXPECTED_STATUS = 200

def main():
    parser = argparse.ArgumentParser(description="Wait for service to become healthy")
    parser.add_argument("--url", required=True, help="Base URL of the service")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL)
    args = parser.parse_args()

    health_url = f"{args.url.rstrip('/')}/health"
    print(f"Checking health: {health_url} (timeout: {args.timeout}s)")

    start = time.time()
    attempt = 0
    while time.time() - start < args.timeout:
        attempt += 1
        try:
            resp = urllib.request.urlopen(health_url, timeout=5)
            if resp.status == DEFAULT_EXPECTED_STATUS:
                elapsed = time.time() - start
                print(f"Health check passed after {attempt} attempts ({elapsed:.1f}s)")
                return 0
        except Exception as e:
            elapsed = time.time() - start
            remaining = args.timeout - elapsed
            print(f"Attempt {attempt}: {e} | Retrying in {args.interval}s ({remaining:.0f}s left)")
        time.sleep(args.interval)

    print(f"ERROR: Health check timed out after {args.timeout}s")
    return 1

if __name__ == "__main__":
    sys.exit(main())
