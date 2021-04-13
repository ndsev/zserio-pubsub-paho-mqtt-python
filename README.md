# Zserio Pub/Sub Paho MQTT Backend

Sample implementation of Zserio Pub/Sub Paho MQTT backend in **Python**.

## Prerequisites

1. [Mosquitto](https://mosquitto.org) message broker running.
   > On Ubuntu check `systemctl status mosquitto`.
1. Java JRE 8+
1. Python 3.8+
1. Paho MQTT:

   ```
   python3 -m pip install paho-mqtt
   ```
1. Zserio compiler with Python runtime library:

   ```
   python3 -m pip install zserio
   ```

## Usage

### Calculator Example

```bash
cd examples/calculator
# generate service using Zserio
zserio calculator.zs -python ../../build/gen

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=../../src:../../build/gen
python3 power_of_two_provider.py &
python3 square_root_of_provider.py &
python3 calculator_client.py
# follow client's instructions
# ...
# press q + ENTER to quit the client
fg
# press Ctrl+C to quit the square_root_of_provider
fg
# press Ctrl+C to quit the power_of_two_provider

> For more understandable output run both providers and client in a separate terminal.
