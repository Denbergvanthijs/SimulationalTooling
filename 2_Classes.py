import simpy


def main(tijd):
    env = simpy.Environment()

    car = Car(env)
    TL = TrafficLight(env, car)

    env.run(until=tijd)
    print(f"Simulation gestopt op: {tijd}")


class TrafficLight(object):
    def __init__(self, env, other, groen_duur=30, geel_duur=5, rood_duur=20):
        self.env = env
        self.other = other

        self.groen_duur = groen_duur
        self.geel_duur = geel_duur
        self.rood_duur = rood_duur

        self.action = env.process(self.run())

    def run(self):
        while True:
            print(f"\x1b[0;32mGroen:{self.env.now:>20}")
            yield self.env.process(self.licht(self.groen_duur))

            print(f"\x1b[0;33mGeel:{self.env.now:>20}")
            yield self.env.process(self.licht(self.geel_duur))

            print(f"\x1b[0;31mRood:{self.env.now:>20}")
            yield self.env.process(self.licht(self.rood_duur))
            # self.other.action.interrupt()

    def licht(self, duration):
        yield self.env.timeout(duration)


class Car(object):
    def __init__(self, env, duur=10):
        self.env = env
        self.duur = duur

        self.action = env.process(self.run())

    def run(self):
        while True:
            try:
                print(f"\x1b[0mRijden:{self.env.now:>20}")
                yield self.env.process(self.rijtijd(self.duur))
            except simpy.Interrupt:
                pass

    def rijtijd(self, duration):
        yield self.env.timeout(duration)


if __name__ == '__main__':
    main(120)
