import typing

import zserio

import paho.mqtt.client as mqtt # type: ignore
import paho.mqtt.publish as publish # type: ignore

class MqttClient(zserio.PubsubInterface):
    """
    Implementation of Zserio Pub/Sub client interface.
    """

    def __init__(self, host: str, port: int):
        """
        Constructor.

        :param host: Host to connect.
        :param port: Port to connect.
        """

        self._host = host
        self._port = port
        self._subscriptions: typing.Dict[int, _MqttSubscription] = {}
        self._num_ids: int = 0 # simple naive implementation, reusing of subscription ID is not safe

    def publish(self, topic: str, data: bytes, _context: typing.Any = None):
        """
        Implementation of PubsubInterface.publish.
        """

        publish.single(topic, payload=data, hostname=self._host, port=self._port)

    def subscribe(self, topic: str, callback: typing.Callable[[str, bytes], None],
                  context: typing.Any = None) -> int:
        """
        Implementation of PubsubInterface.subscribe.
        """

        subscription_id = self._num_ids
        self._num_ids += 1
        self._subscriptions[subscription_id] = _MqttSubscription(self._host, self._port, topic,
                                                                 callback, context)
        return subscription_id

    def unsubscribe(self, subscription_id: int):
        """
        Implementation of PubsubInterface.unsubscribe.
        """

        self._subscriptions.pop(subscription_id).close()

    def close(self):
        """
        Closes all active subscriptions.
        """

        for subscription in self._subscriptions.values():
            subscription.close()
        self._subscriptions.clear()

_KEEPALIVE=60

class _MqttSubscription:
    def __init__(self, host: str, port: int, topic: str, callback: typing.Callable[[str, bytes], None],
                 context: typing.Any):
        self._topic = topic
        self._callback = callback
        self._context = context

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(host, port, _KEEPALIVE)
        self._client.loop_start()

    def close(self):
        self._client.unsubscribe(self._topic)
        self._client.disconnect()
        self._client.loop_stop()

    def _on_connect(self, _client: mqtt.Client, _userdata: typing.Any, _flags: int, _rc: int):
        self._client.subscribe(self._topic)

    def _on_message(self, _client: mqtt.Client, _userdata: typing.Any, message: mqtt.MQTTMessage):
        try:
            self._callback(message.topic, message.payload)
        except Exception as excpt:
            print("MqttSubscription error in callback:", excpt)
