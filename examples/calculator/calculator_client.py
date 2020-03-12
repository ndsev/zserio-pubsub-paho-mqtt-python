import sys

import zserio
from zserio_pubsub_paho_mqtt import MqttClient
import calculator.api as api

def _printHelp():
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

def _publishRequest(client, line):
    try:
        request = api.I32.fromFields(int(line))
    except Exception as e:
        print("Error: '%s' cannot be converted to int32!" % line)
        print(e)
        return

    client.publishRequest(request)

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else 1883

    print("Welcome to Zserio Calculator Mosquitto Pub/Sub Client example!")
    print("Creating client and subscriptions (terminate with ^C) ...", end='', flush=True)

    # instance of zserio_pubsub_paho_mqtt.MqttClient to be used as a PubsubInterface
    mqttClient = MqttClient(host, port)

    # calculator client uses the Paho MQTT client backend
    client = api.CalculatorClient(mqttClient)

    powerOfTwoCallback = lambda topic, value: print("power of two:", value.getValue())
    powerOfTwoId = client.subscribePowerOfTwo(powerOfTwoCallback)
    powerOfTwoSubscribed = True

    squareRootOfCallback = lambda topic, value: print("square_root_of:", value.getValue())
    squareRootOfId = client.subscribeSquareRootOf(squareRootOfCallback)
    squareRootOfSubscribed = True

    print(" OK!")
    print("Write 'h' + ENTER for help.")

    while True:
        line = input(('p' if powerOfTwoSubscribed else "") + ('s' if squareRootOfSubscribed else "") + "> ")
        if not line:
            continue

        if line[0] == 'q':
            print("Quit.")
            break

        if line[0] == 'h':
            _printHelp()
            continue

        if line[0] == 'p':
            if powerOfTwoSubscribed:
                client.unsubscribe(powerOfTwoId)
                powerOfTwoSubscribed = False
            else:
                powerOfTwoId = client.subscribePowerOfTwo(powerOfTwoCallback)
                powerOfTwoSubscribed = True
            continue

        if line[0] == 's':
            if squareRootOfSubscribed:
                client.unsubscribe(squareRootOfId)
                squareRootOfSubscribed = False
            else:
                squareRootOfId = client.subscribeSquareRootOf(squareRootOfCallback)
                squareRootOfSubscribed = True
            continue

        _publishRequest(client, line)

    mqttClient.close()
