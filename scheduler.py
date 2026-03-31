import schedule
import time
from encar_parser import run

run()
schedule.every(24).hours.do(run)

print("[Scheduler] Running. Next update in 24h. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
