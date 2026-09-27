from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.alerts = []

    def trigger_alert(self, event):
        alert = {
            "alert_type": "SECURITY_BREACH",
            "timestamp": datetime.now().isoformat(),
            "ip": event['ip'],
            "username": event['username'],
            "reason": event['reason'],
            "severity": "HIGH"
        }
        
        self.alerts.append(alert)
        self._log_alert(alert)

    def _log_alert(self, alert):
        print("\n" + "="*50)
        print("🚨 SECURITY ALERT 🚨")
        print("="*50)
        print(f"Time:     {alert['timestamp']}")
        print(f"Severity: {alert['severity']}")
        print(f"IP:       {alert['ip']}")
        print(f"User:     {alert['username']}")
        print(f"Reason:   {alert['reason']}")
        print("="*50 + "\n")