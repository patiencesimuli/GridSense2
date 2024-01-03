import flask
import serial
import time

app = flask.Flask(__name__)

# Initialize serial communication with Arduino
ser = serial.Serial('COM3', 9600)

# Global variables to store sensor and fault data
voltage_values = []
current_values = []
fault_type = None

@app.route("/")
def index():
    # Retrieve sensor data and fault information from Arduino
    global voltage_values, current_values, fault_type

    while ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if line:
            values = line.split(',')
            voltage_values = values[:4]  # Collect the first 4 values for voltage
            current_values = values[4:8]  # Collect the next 4 values for current
            fault_type = values[-1]  # Extract fault type (string)

    # Prepare data for HTML template
    data = {
        "voltage_values": voltage_values,
        "current_values": current_values,
        "fault_type": fault_type
    }

    return flask.render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
