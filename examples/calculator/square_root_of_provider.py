import sys
import signal
import math

import zserio
from zserio_pubsub_paho_mqtt import MqttClient
import calculator.api as api

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            print("Usage: python %s [HOST [PORT]]")
            exit(0)

    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else 1883

    # instance of zserio_pubsub_paho_mqtt.MqttClient to be used as a PubsubInterface
    mqttClient = MqttClient(host, port)

    # square root of provider uses the Paho MQTT client backend
    squareRootOfProvider = api.SquareRootOfProvider(mqttClient)

    def callback(topic, value):
        print("SquareRootOfProvider: request=", value.getValue())
        response = api.Double.fromFields(math.sqrt(value.getValue()))
        squareRootOfProvider.publishSquareRootOf(response)

    squareRootOfProvider.subscribeRequest(callback)

    print("Square root of provider, waiting for calculator/request...")
    print("Press Ctrl+C to quit.")

    try:
        signal.pause()
    except:
        pass

    mqttClient.close()
