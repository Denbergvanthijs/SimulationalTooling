import simpy


def main(tijd):
    env = simpy.Environment()
    kruispunt = simpy.Resource(env, capacity=1)

    TL = TrafficLight(env)

    car0 = Car(env, TL, kruispunt, "ThijsAuto")
    car1 = Car(env, TL, kruispunt, "FreekAuto")

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
    def __init__(self, env, other, kruispunt, name, duurOp=5, duurAf=11):
        self.env = env
        self.other = other
        self.kruispunt = kruispunt
        self.name = name

        self.duurOp = duurOp
        self.duurAf = duurAf
        self.action = env.process(self.run())

    def run(self):
        while True:
            with self.kruispunt.request() as req:
                yield req

                if self.other.staat:
                    print(f"\x1b[0m\t{self.name} Op:{self.env.now:>12}")
                    yield self.env.process(self.rijtijd(self.duurOp))  # Rijden voor self.duur seconden

                    print(f"\x1b[0m\t{self.name} Af:{self.env.now:>12}")
                    yield self.env.process(self.rijtijd(self.duurAf))
                else:
                    # print("Kruispunt leeg")
                    yield self.env.process(self.rijtijd(1))  # Iedere seconde checken

    def rijtijd(self, duration):
        yield self.env.timeout(duration)


if __name__ == '__main__':
    main(240)
