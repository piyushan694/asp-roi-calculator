"""
ASP Partner ROI Calculator — Share Launcher
============================================
Run this script to start the dashboard and create a shareable public URL.

Usage:
    python dashboard/share.py

First-time setup:
    1. Sign up free at https://dashboard.ngrok.com/signup
    2. Copy your auth token from https://dashboard.ngrok.com/get-started/your-authtoken
    3. Run: ngrok config add-authtoken YOUR_TOKEN
       (or paste it when this script prompts you)
"""

import subprocess
import sys
import time
import webbrowser

def main():
    # Check for ngrok auth token
    from pyngrok import ngrok, conf

    try:
        # Test if auth token is configured
        tunnels = ngrok.get_tunnels()
    except Exception as e:
        if "authtoken" in str(e).lower() or "ERR_NGROK" in str(e):
            print("\n" + "=" * 60)
            print("  FIRST-TIME SETUP: ngrok auth token needed")
            print("=" * 60)
            print("\n  1. Go to: https://dashboard.ngrok.com/signup")
            print("     (free account, no credit card)")
            print("\n  2. Copy your auth token from:")
            print("     https://dashboard.ngrok.com/get-started/your-authtoken")
            print()
            token = input("  Paste your auth token here: ").strip()
            if token:
                ngrok.set_auth_token(token)
                print("  ✓ Token saved!\n")
            else:
                print("  ✗ No token provided. Exiting.")
                sys.exit(1)

    # Start Streamlit in background
    print("\n🚀 Starting ASP Partner ROI Calculator...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/roi_calculator.py",
         "--server.port", "8501", "--server.headless", "true",
         "--browser.gatherUsageStats", "false"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    # Wait for Streamlit to start
    print("   Waiting for app to start...", end="", flush=True)
    for _ in range(15):
        time.sleep(1)
        print(".", end="", flush=True)
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:8501")
            break
        except Exception:
            continue
    print(" ready!")

    # Open ngrok tunnel
    print("\n🌐 Creating shareable link...")
    try:
        tunnel = ngrok.connect(8501)
        public_url = tunnel.public_url

        # Force HTTPS
        if public_url.startswith("http://"):
            public_url = public_url.replace("http://", "https://", 1)

        print("\n" + "=" * 60)
        print("  ✅ DASHBOARD IS LIVE!")
        print("=" * 60)
        print(f"\n  🔗 Share this link with partners & BD team:")
        print(f"\n     {public_url}")
        print(f"\n  📋 Local access: http://localhost:8501")
        print(f"\n  ⚠️  Link stays active while this script runs.")
        print(f"     Press Ctrl+C to stop sharing.\n")
        print("=" * 60)

        # Open in browser
        webbrowser.open(public_url)

        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")

    except Exception as e:
        print(f"\n❌ Error creating tunnel: {e}")
        print("\nFallback: The app is still running locally at http://localhost:8501")
        print("You can share your screen during the meeting instead.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")

    finally:
        ngrok.kill()
        proc.terminate()
        print("   Done. Dashboard stopped.\n")


if __name__ == "__main__":
    main()
