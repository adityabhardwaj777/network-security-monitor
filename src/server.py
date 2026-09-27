from flask import Flask, request, jsonify, render_template
from monitor import ConnectionMonitor
from alerts import AlertSystem

app = Flask(__name__)
monitor = ConnectionMonitor()
alert_system = AlertSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def handle_connection():
    data = request.get_json()
    ip = data.get('ip')
    username = data.get('username')
    success = data.get('success', False)

    event = monitor.log_attempt(ip, username, success)
    
    if event:
        alert_system.trigger_alert(event)
        return jsonify({
            "status": "blocked",
            "reason": event['reason'],
            "ip": ip
        }), 403

    return jsonify({
        "status": "success" if success else "failed",
        "ip": ip,
        "username": username
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(monitor.get_stats()), 200

@app.route('/reset', methods=['POST'])
def reset():
    monitor.reset()
    return jsonify({"status": "reset"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)