from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner


class PoloniexComponent(ApplicationSession):
    def onConnect(self):
        self.join(self.config.realm)

    def onJoin(self, details):
        def onTicker(*args):
            print("Ticker event received:", args)

        try:
            for b in self.subscribe(onTicker, 'ticker'):
                yield b

        except Exception as e:
            print("Could not subscribe to topic:", e)


def main():
    runner = ApplicationRunner(u"wss://api.poloniex.com:443", "realm1")
    runner.run(PoloniexComponent)


if __name__ == "__main__":
    main()