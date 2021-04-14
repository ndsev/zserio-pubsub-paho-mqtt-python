import sys
import time
import math

import calculator.api as api

from zserio_pubsub_paho_mqtt import MqttClient

def _main():
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print("Usage: python %s [HOST [PORT]]")
            sys.exit(0)

    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else 1883

    # instance of zserio_pubsub_paho_mqtt.MqttClient to be used as a PubsubInterface
    mqtt_client = MqttClient(host, port)

    # square root of provider uses the Paho MQTT client backend
    square_root_of_provider = api.SquareRootOfProvider(mqtt_client)

    def callback(_topic: str, request: api.I32):
        print("square_root_of_provider: request=", request.value)
        response = api.Double(math.sqrt(request.value))
        square_root_of_provider.publish_square_root_of(response)

    square_root_of_provider.subscribe_request(callback)

    print("Square root of provider, waiting for calculator/request...")
    print("Press Ctrl+C to quit.")

    # signal.pause() is missing for Windows - wait 100ms and loop instead
    while True:
        time.sleep(0.1)

    mqtt_client.close()

if __name__ == "__main__":
    sys.exit(_main())
