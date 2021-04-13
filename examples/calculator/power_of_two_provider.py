import sys
import signal

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

    # power of two provider uses the Paho MQTT client backend
    power_of_two_provider = api.PowerOfTwoProvider(mqtt_client)

    def callback(_topic: str, request: api.I32):
        print("power_of_two_provider: request=", request.value)
        response = api.U64(request.value**2)
        power_of_two_provider.publish_power_of_two(response)

    power_of_two_provider.subscribe_request(callback)

    print("Power of two provider, waiting for calculator/request...")
    print("Press Ctrl+C to quit.")

    try:
        signal.pause()
    except Exception:
        pass

    mqtt_client.close()

if __name__ == "__main__":
    sys.exit(_main())
