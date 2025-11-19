import subprocess
import time
import sys
import os
from keep_alive import keep_alive

def run_bot():
    """Run the bot with auto-restart functionality"""
    restart_count = 0
    max_restarts = 50  # Prevent infinite restart loops

    while restart_count < max_restarts:
        try:
            # Log restart attempt (will be sent once bot is online)
            restart_reason = "Manual restart" if restart_count == 0 else f"Auto-restart after crash (Attempt {restart_count})"
            print(f"⚡ Starting RXT ENGINE... (Attempt {restart_count + 1})")

            # Run the main bot file
            process = subprocess.run([sys.executable, "main.py"], check=True)

            # If we reach here, the bot exited normally
            print("⚡ RXT ENGINE stopped normally.")
            break

        except subprocess.CalledProcessError as e:
            restart_count += 1
            print(f"❌ Bot crashed with exit code {e.returncode}")
            print(f"🔄 Restarting in 5 seconds... (Restart #{restart_count})")

            if restart_count >= max_restarts:
                print(f"❌ Maximum restart attempts ({max_restarts}) reached. Stopping.")
                break

            time.sleep(5)  # Wait 5 seconds before restarting

        except KeyboardInterrupt:
            print("\n🛑 Manual stop detected. Exiting...")
            break

        except Exception as e:
            restart_count += 1
            print(f"❌ Unexpected error: {e}")
            print(f"🔄 Restarting in 5 seconds... (Restart #{restart_count})")

            if restart_count >= max_restarts:
                print(f"❌ Maximum restart attempts ({max_restarts}) reached. Stopping.")
                break

            time.sleep(5)

if __name__ == "__main__":
    print("⚡ RXT ENGINE Auto-Restart Manager Starting...")

    # Start keep-alive server
    keep_alive()

    # Start bot with auto-restart
    run_bot()