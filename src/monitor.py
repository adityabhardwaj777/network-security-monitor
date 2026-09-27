from collections import defaultdict
from datetime import datetime, timedelta

FAILED_ATTEMPT_THRESHOLD = 5
TIME_WINDOW_MINUTES = 2

class ConnectionMonitor:
    def __init__(self):
        self.attempts = defaultdict(list)
        self.blocked_ips = set()
        self.all_events = []

    def log_attempt(self, ip, username, success):
        now = datetime.now()

        event = {
            "ip": ip,
            "username": username,
            "success": success,
            "timestamp": now.isoformat()
        }
        self.all_events.append(event)

        if ip in self.blocked_ips:
            return {
                "reason": f"IP {ip} is permanently blocked due to repeated failed attempts",
                "ip": ip,
                "username": username
            }

        if not success:
            self.attempts[ip].append(now)

        # Remove attempts outside the time window
        cutoff = now - timedelta(minutes=TIME_WINDOW_MINUTES)
        self.attempts[ip] = [t for t in self.attempts[ip] if t > cutoff]

        if len(self.attempts[ip]) >= FAILED_ATTEMPT_THRESHOLD:
            self.blocked_ips.add(ip)
            return {
                "reason": f"Brute force detected: {len(self.attempts[ip])} failed attempts in {TIME_WINDOW_MINUTES} minutes",
                "ip": ip,
                "username": username
            }

        return None

    def get_stats(self):
        return {
            "total_events": len(self.all_events),
            "blocked_ips": list(self.blocked_ips),
            "recent_events": self.all_events[-10:]
        }

    def reset(self):
        self.attempts.clear()
        self.blocked_ips.clear()
        self.all_events.clear()