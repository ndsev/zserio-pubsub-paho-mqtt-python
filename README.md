# Zserio Pub/Sub Paho MQTT Backend

Sample implementation of Zserio Pub/Sub Paho MQTT backend in **Python**.

## Prerequisites

1. Install [Mosquitto](https://mosquitto.org) according to
[official instructions](https://mosquitto.org/download/). Mosquitto is the message broker which implements
MQTT protocol.
   * Check that mosquitto broker is running
     > On Ubuntu check `systemctl status mosquitto`.

2. Python 3 with Paho MQTT installed

   ```bash
   python3 -m pip install paho-mqtt
   ```

3. Zserio Python runtime library
4. Zserio compiler (`zserio.jar`)

> Zserio prerequisites are included in this repo in 3rdparty folder.

## Usage

### Calculator Example

```bash
cd examples/calculator
# generate service using Zserio
java -jar ../../3rdparty/zserio.jar calculator.zs -python gen

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=../../3rdparty/runtime:../../src:gen
python3 power_of_two_provider.py &
python3 square_root_of_provider.py &
python3 calculator_client.py
# follow client's instructions
# ...
# pres q + ENTER to quit the client
fg # and press Ctrl+C to quit the square_root_of_provider
fg # and press Ctrl+C to quit the power_of_two_provider
```

> For more understandable output run both providers and client in a separate terminal.
