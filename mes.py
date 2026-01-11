from datetime import datetime
from zoneinfo import ZoneInfo
import requests

def random_quote():
    r = requests.get("https://api.quotable.io/random", timeout=5)
    if r.ok:
        data = r.json()
        return f"{data['content']} — {data['author']}"
    return "Silence is also information."

TOKEN = "8488696823:AAE-LDSGwuhynh-n-yb8WGGll3wmzicl-Vk"
CHAT_ID = "269476468"


# ===== Timezone =====
tz = ZoneInfo("Asia/Jerusalem")
now = datetime.now(tz)

# ===== Reference times =====
start_nov_26 = datetime(now.year - 1, 11, 26, 0, 0, tzinfo=tz)
start_dec_22 = datetime(now.year - 1, 12, 22, 19, 0, tzinfo=tz)
end_feb_5    = datetime(now.year, 2, 5, 17, 0, tzinfo=tz)

# Progress bar period
progress_start = datetime(now.year-1, 11, 26, 0, 0, tzinfo=tz)
progress_end   = datetime(now.year, 3, 12, 0, 0, tzinfo=tz)

# ===== Helpers =====
def breakdown(delta):
    days = delta.days
    hours = delta.seconds // 3600
    total_hours = int(delta.total_seconds() // 3600)
    return f"{days}d {hours}h ({total_hours}h)"

def progress_bar(now, start, end, width=20):
    total = (end - start).total_seconds()
    elapsed = (now - start).total_seconds()

    ratio = min(max(elapsed / total, 0), 1)
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)

    percent = int(ratio * 100)
    return f"[{bar}] {percent}%"
    
def smooth_bar_4(now, start, end, width=20):
    levels = [" ", "░", "▒", "▓", "█"] # 0..3

    total = (end - start).total_seconds()
    elapsed = max(0, min((now - start).total_seconds(), total))
    ratio = elapsed / total

    units = ratio * width
    full = int(units)
    rem = units - full
    sub = int(rem * 4)  # 0..3

    # build
    bar = "█" * full
    if full < width:
        bar += levels[sub]  # partial cell
        bar += "░" * (width - full - 1)

    percent = int(ratio * 100)
    return f"[{bar}] {percent}% \n {sub}"

# ===== Message =====
msg = (
    f"⏱ Time update (IL)\n\n"
    f"Since Nov 26 00:00: {breakdown(now - start_nov_26)}\n"
    f"Since Dec 22 19:00: {breakdown(now - start_dec_22)}\n"
    f"Until Feb 5 17:00: {breakdown(end_feb_5 - now)}\n\n"
    f"Progress Dec 22 → Feb 5:\n"
    f"{smooth_bar_4(now, start_dec_22, end_feb_5)}\n\n"
    f"Progress Nov 26 → Mar 12:\n"
    f"{smooth_bar_4(now, progress_start, progress_end)}\n\n"
    f"another hour pass, yayy😶"
)


# ===== Send =====
try:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=10
    )
except Exception:
    pass







