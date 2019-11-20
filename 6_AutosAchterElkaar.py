import simpy


def main(tijd):
    env = simpy.Environment()
    wachtrij = simpy.Resource(env, capacity=4)

    TL = TrafficLight(env, groen_duur=30, geel_duur=7, rood_duur=22, grens=2)

    car0 = Car(env, TL, wachtrij, "Thijs", duurOp=10)
    car1 = Car(env, TL, wachtrij, "Freek", duurOp=9)
    car1 = Car(env, TL, wachtrij, "Casper", duurOp=8)
    car3 = Car(env, TL, wachtrij, "Stan", duurOp=4)
    car4 = Car(env, TL, wachtrij, "Lucas", duurOp=5)
    car5 = Car(env, TL, wachtrij, "Helez", duurOp=6)
    car6 = Car(env, TL, wachtrij, "Stijn", duurOp=7)
    car7 = Car(env, TL, wachtrij, "Tom", duurOp=8)
    car8 = Car(env, TL, wachtrij, "Reinier", duurOp=9)
    car9 = Car(env, TL, wachtrij, "David", duurOp=10)

    env.run(until=tijd)
    print(f"Simulation gestopt op: {tijd}")


class TrafficLight(object):
    def __init__(self, env, groen_duur=30, geel_duur=5, rood_duur=20, grens=2):
        self.env = env

        self.groen_duur = groen_duur  # Duur van stoplicht op groen
        self.geel_duur = geel_duur  # Duur van stoplicht op geel
        self.rood_duur = rood_duur  # Duur van stoplicht op rood

        self.grens = grens  # Grenswaarde binnen hoeveel t een auto veilig in rood kan zitten
        self.staat = 0  # Huidige staat van het stoplicht: groen/geel/rood
        self.action = env.process(self.run())

    def run(self):
        while True:
            print(f"\x1b[0;32mGroen:{self.env.now:>20}")
            self.staat = (1, self.env.now)  # Staat op groen zetten, tijd van huidige staat meegeven
            yield self.env.process(self.licht(self.groen_duur))

            print(f"\x1b[0;33mGeel:{self.env.now:>20}")
            self.staat = (2, self.env.now)  # Staat op geel zetten, tijd van huidige staat meegeven
            yield self.env.process(self.licht(self.geel_duur))

            print(f"\x1b[0;31mRood:{self.env.now:>20}")
            self.staat = (0, self.env.now)  # Staat op rood zetten, tijd van huidige staat meegeven
            yield self.env.process(self.licht(self.rood_duur))

    def licht(self, duration):
        yield self.env.timeout(duration)  # Actie uitvoeren gedurende `duration` aantal t


class Car(object):
    def __init__(self, env, other, wachtrij, name, duurOp=5):
        self.env = env
        self.other = other  # Object van stoplicht
        self.wachtrij = wachtrij  # De file waar iedere auto achteraan aansluit. self.env.now wordt groter in de file
        self.name = name  # Naam van de auto

        self.duurOp = duurOp  # Duur dat een auto op het kruispunt is
        self.action = env.process(self.run())

    def run(self):
        while True:
            with self.wachtrij.request() as req:
                # Reserveer een plekje in de file, kijk zodra je die plek hebt pas of stoplicht groen/geel is.
                # Als het stoplicht rood is: sluit na 1 eenheid direct weer aan in de file.

                yield req  # self.env.now wordt hier vergroot waardoor self.other.staat kan zijn veranderd
                if self.other.staat[0]:  # if groen/geels
                    print(f"\x1b[0m\t{self.name} op kruispunt vanaf {self.env.now} tot {self.env.now + self.duurOp}")
                    yield self.env.process(self.rijtijd(self.duurOp))  # Rijden voor self.duur eenheid

                    if not self.other.staat[0] and (self.env.now - self.other.staat[1]) > self.other.grens:  # if rood
                        print(f"\x1b[0;31m\t{self.name}\x1b[0m tot \x1b[0;31m{self.env.now}\x1b[0m op kruispunt")
                        break  # Stop de while-loop voor deze auto, deze auto wordt nooit meer uitgevoerd
                    else:
                        print(f"\x1b[0m\t{self.name} tot {self.env.now} op kruispunt")
                else:
                    # print("Kruispunt leeg")
                    yield self.env.process(self.rijtijd(1))  # Iedere seconde checken

        # print(f"\x1b[1;30;41mEinde der tijden voor {self.name}\t\x1b[0m")

    def rijtijd(self, duration):
        yield self.env.timeout(duration)


if __name__ == '__main__':
    main(240)
