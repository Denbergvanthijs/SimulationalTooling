import simpy


def main(tijd):
    env = simpy.Environment()

    TL = TrafficLight(env)
    car = Car(env, TL)

    env.run(until=tijd)
    print(f"Simulation gestopt op: {tijd}")


class TrafficLight(object):
    def __init__(self, env, groen_duur=30, geel_duur=5, rood_duur=20):
        self.env = env

        self.groen_duur = groen_duur
        self.geel_duur = geel_duur
        self.rood_duur = rood_duur
        self.staat = 0

        self.action = env.process(self.run())

    def run(self):
        while True:
            print(f"\x1b[0;32mGroen:{self.env.now:>20}")
            self.staat = 1
            yield self.env.process(self.licht(self.groen_duur))

            print(f"\x1b[0;33mGeel:{self.env.now:>20}")
            self.staat = 2
            yield self.env.process(self.licht(self.geel_duur))

            print(f"\x1b[0;31mRood:{self.env.now:>20}")
            self.staat = 0
            yield self.env.process(self.licht(self.rood_duur))

    def licht(self, duration):
        yield self.env.timeout(duration)


class Car(object):
    def __init__(self, env, other, duur=10):
        self.env = env
        self.duur = duur
        self.other = other

        self.action = env.process(self.run())

    def run(self):
        while True:
            try:
                if self.other.staat:
                    print(f"\x1b[0mRijden:{self.env.now:>20}")
                    yield self.env.process(self.rijtijd(self.duur))  # Rijden voor self.duur seconden
                else:
                    # print("Nog niet rijden", end="")
                    yield self.env.process(self.rijtijd(1))  # Iedere seconde checken
            except simpy.Interrupt:
                pass

    def rijtijd(self, duration):
        yield self.env.timeout(duration)


if __name__ == '__main__':
    main(120)
