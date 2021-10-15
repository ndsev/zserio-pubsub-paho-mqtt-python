import sys
import time

import calculator.api as api

from zserio_pubsub_paho_mqtt import MqttClient

def _print_help():
    print(
        "Help:",
        " INPUT        Any valid 32bit integer.",
        " p            Subscribes/Unsubscribes calculator/power_of_two topic.",
        " s            Subscribes/Unsubscribes calculator/square_root_of topic.",
        " h            Prints this help.",
        " q            Quits the client.",
        "",
        "Note that the letters before the '>' denotes the subscribed topics.",
        sep='\n'
    )

def _publish_request(client: api.CalculatorClient, line: str):
    try:
        request = api.I32(int(line))
    except Exception as excpt:
        print("Error: '%s' cannot be converted to int32!" % line)
        print(excpt)
        return

    client.publish_request(request)

def _main():
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print("Usage: python %s [HOST [PORT]]")
            sys.exit(0)

    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else 1883

    print("Welcome to Zserio Calculator Paho MQTT Pub/Sub Client example!")
    print("Creating client and subscriptions (terminate with ^C) ...", end='', flush=True)

    # instance of zserio_pubsub_paho_mqtt.MqttClient to be used as a PubsubInterface
    mqtt_client = MqttClient(host, port)

    # calculator client uses the Paho MQTT client backend
    client = api.CalculatorClient(mqtt_client)

    power_of_two_callback = lambda topic, response: print("power_of_two:", response.value)
    power_of_two_id = client.subscribe_power_of_two(power_of_two_callback)
    power_of_two_subscribed = True

    square_root_of_callback = lambda topic, response: print("square_root_of:", response.value)
    square_root_of_id = client.subscribe_square_root_of(square_root_of_callback)
    square_root_of_subscribed = True

    print(" OK!")
    print("Write 'h' + ENTER for help.")

    while True:
        line = input(('p' if power_of_two_subscribed else "") +
                     ('s' if square_root_of_subscribed else "") +
                     "> ")
        if not line:
            continue

        if line[0] == 'q':
            print("Quitting.")
            time.sleep(1) # wait a little bit for a potential responses
            break

        if line[0] == 'h':
            _print_help()
            continue

        if line[0] == 'p':
            if power_of_two_subscribed:
                client.unsubscribe(power_of_two_id)
                power_of_two_subscribed = False
            else:
                power_of_two_id = client.subscribe_power_of_two(power_of_two_callback)
                power_of_two_subscribed = True
            continue

        if line[0] == 's':
            if square_root_of_subscribed:
                client.unsubscribe(square_root_of_id)
                square_root_of_subscribed = False
            else:
                square_root_of_id = client.subscribe_square_root_of(square_root_of_callback)
                square_root_of_subscribed = True
            continue

        _publish_request(client, line)

    mqtt_client.close()

if __name__ == "__main__":
    sys.exit(_main())
