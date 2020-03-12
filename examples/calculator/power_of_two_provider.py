import sys
import signal

import zserio
from zserio_pubsub_paho_mqtt import MqttClient
import calculator.api as api

if __name__ == "__main__":
    if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Usage: python %s [HOST [PORT]]" % sys.argv[0])
        exit(0)

    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else 1883

    # instance of zserio_pubsub_paho_mqtt.MqttClient to be used as a PubsubInterface
    mqttClient = MqttClient(host, port)

    # power of two provider uses the Paho MQTT client backend
    powerOfTwoProvider = api.PowerOfTwoProvider(mqttClient)

    def callback(topic, value):
        print("PowerOfTwoProvider: request=", value.getValue())
        response = api.U64.fromFields(value.getValue()**2)
        powerOfTwoProvider.publishPowerOfTwo(response)

    powerOfTwoProvider.subscribeRequest(callback)

    print("Power of two provider, waiting for calculator/request...")
    print("Press Ctrl+C to quit.")

    try:
        signal.pause()
    except:
        pass

    mqttClient.close()
