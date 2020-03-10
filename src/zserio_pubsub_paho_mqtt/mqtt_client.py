import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import zserio

class MqttClient(zserio.PubsubInterface):
    """
    Implementation of Zserio Pub/Sub client interface.
    """

    def __init__(self, host, port):
        """
        Constructor.

        :param host: Host to connect.
        :param port: Port to connect.
        """

        self._host = host
        self._port = port
        self._subscriptions = {}
        self._numIds = 0 # simple naive implementation, reusing of subscription ID is not safe

    def publish(self, topic, data, context):
        """
        Implementation of PubsubInterface.publish.
        """

        publish.single(topic, payload=data, hostname=self._host, port=self._port)

    def subscribe(self, topic, callback, context):
        """
        Implementation of PubsubInterface.subscribe.
        """

        subscriptionId = self._numIds
        self._numIds += 1
        self._subscriptions[subscriptionId] = _MqttSubscription(self._host, self._port, subscriptionId, topic,
                                                                callback, context)
        return subscriptionId

    def unsubscribe(self, subscriptionId):
        """
        Implementation of PubsubInterface.unsubscribe.
        """

        self._subscriptions.pop(subscriptionId).close()

    def close(self):
        """
        Closes all active subscriptions.
        """

        for subscription in self._subscriptions.values():
            subscription.close()
        self._subscriptions.clear()

_KEEPALIVE=60

class _MqttSubscription:
    def __init__(self, host, port, subscriptionId, topic, callback, context):
        self._topic = topic
        self._callback = callback
        self._context = context

        self._client = mqtt.Client()
        self._client.on_connect = self._onConnect
        self._client.on_message = self._onMessage
        self._client.connect(host, port, _KEEPALIVE)
        self._client.loop_start()

    def close(self):
        self._client.unsubscribe(self._topic)
        self._client.disconnect()
        self._client.loop_stop()

    def _onConnect(self, client, userdata, flags, rc):
        self._client.subscribe(self._topic)

    def _onMessage(self, client, userdata, msg):
        try:
            self._callback(msg.topic, msg.payload)
        except Exception as e:
            print("MqttSubscription error in callback:", e)
