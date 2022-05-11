import asyncio, random
from datetime import datetime
import random
import socket
import struct


class TrafficShaper:
    pass

    def __init__(self, **kwargs):
        pass

    def next(self):
        return None, None, None


class TCPTrafficShaper(TrafficShaper):

    def __init__(self, **kwargs):
        super(TCPTrafficShaper, self).__init__(**kwargs)

    def next(self):
        pass


class RandomPacketSizeBackAndForthTrafficShaper(TrafficShaper):

    last_direction = 1

    def __init__(self, **kwargs):
        super(RandomPacketSizeBackAndForthTrafficShaper, self).__init__(**kwargs)

    def next(self):
        number_of_packets = random.randint(1, 10)
        total_bytes = sum([random.randint(1, 65535) for _ in range(0, number_of_packets)])

        self.last_direction *= -1
        total_bytes = total_bytes * self.last_direction

        return number_of_packets, total_bytes, None


class ConversationEvent:

    conversation = None
    epoc_ts_utc = None

    def __init__(self, conversation):
        self.agent = conversation
        self.epoc_ts_utc = datetime.utcnow()


class ConversationEndEvent(ConversationEvent):

    def __init__(self, conversation_agent):
        super(ConversationEndEvent, self).__init__(conversation_agent)


class ConversationStartEvent(ConversationEvent):

    def __init__(self, conversation_agent):
        super(ConversationStartEvent, self).__init__(conversation_agent)


class ConversationDataSendEvent(ConversationEvent):

    _bytes_sent = 0
    _packets_sent = 0

    def __init__(self, conversation, packets_sent, bytes_sent):
        super(ConversationDataSendEvent, self).__init__(conversation)
        self._bytes_sent = bytes_sent
        self._packets_sent = packets_sent

    @property
    def bytes_sent(self):
        return self._bytes_sent

    @property
    def packets_sent(self):
        return self._packets_sent

    def __str__(self):
        if self._bytes_sent > -1:
            return f"{self.agent.client_ip} --{self.bytes_sent}/{self.packets_sent}-> {self.agent.server_ip}"
        else:
            return f"{self.agent.client_ip} <-{self.bytes_sent}/{self.packets_sent}-- {self.agent.server_ip}"


async def rnd_sleep(t):
    # sleep for T seconds on average
    await asyncio.sleep(t * random.random() * 2)


class ConversationAgent:

    _output_queue = None
    _client_ip = None
    _server_ip = None
    _conversation_profile = None
    _traffic_shaper = None

    def __init__(self, event_output_queue, client_ip, server_ip, conversation_profile=None, traffic_shaper=RandomPacketSizeBackAndForthTrafficShaper()):

        self._output_queue = event_output_queue
        self._client_ip = client_ip
        self._server_ip = server_ip

        self._traffic_shaper = traffic_shaper

    @property
    def client_ip(self):
        return self._client_ip

    @property
    def server_ip(self):
        return self._server_ip

    async def doConversation(self):
        await self._output_queue.put(ConversationStartEvent(self))

        for i in range(0, random.randint(1, 100)):
            number_of_packets, total_bytes, flags = self._traffic_shaper.next()

            await self._output_queue.put(ConversationDataSendEvent(self,
                                                                   number_of_packets,
                                                                   total_bytes,
                                                                   ))
            await asyncio.sleep(.1 * random.random() * 2)

        await self._output_queue.put(ConversationEndEvent(self))

        pass


async def consumer(queue):
    while True:
        token = await queue.get()

        # process the token received from a producer

        if type(token) == ConversationStartEvent:
            print(f"START CONVERSATION {token.agent.client_ip} -> {token.agent.server_ip}")
        elif type(token) == ConversationEndEvent:
            print(f"END CONVERSATION {token.agent.client_ip} -> {token.agent.server_ip}")
        elif type(token) == ConversationDataSendEvent:
            print(f"SEND CONVERSATION {token}")
        else:
            print("UNKNOWN TYPE {}".format(type(token)))

        queue.task_done()


async def main():
    queue = asyncio.Queue()

    conversation_consumer = asyncio.create_task(consumer(queue))

    # fire up the both producers and consumers
    agents = []
    for _ in range(0, 1):
        agents.append(ConversationAgent(event_output_queue=queue,
                                        client_ip=socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
                                        server_ip=socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))))

    agent_conversation_producers = []
    for agent in agents:
        agent_conversation_producers.append(asyncio.create_task(agent.doConversation()))

    await asyncio.gather(*agent_conversation_producers)

    print('---- done producing')

    # wait for the remaining tasks to be processed
    await queue.join()
    print("Join done")

    conversation_consumer.cancel()


asyncio.run(main())