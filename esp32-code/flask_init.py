from flask import Flask, request, jsonify


app = Flask(__name__)


latest_command = 'N'  

@app.route('/process', methods=['POST'])
def process_command():
    """
    Endpoint to receive commands from the red detection code.
    """
    global latest_command
    
    latest_command = request.form.get('data', 'N')  
    print(f"Received command: {latest_command}")
    return "Command received", 200

@app.route('/get_command', methods=['GET'])


def get_command():
    """
    Endpoint for Arduino to fetch the latest command.
    """
    return jsonify({"command": latest_command})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
