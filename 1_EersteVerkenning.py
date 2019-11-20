import simpy


def main(tijd):
    env = simpy.Environment()

    env.process(traffic_light(env))
    env.process(car(env))

    env.run(until=tijd)
    print(f"Simulation gestopt op: {tijd}")


def traffic_light(env):
    while True:
        print(f"\x1b[0;32mGroen:{env.now:>20}")
        yield env.timeout(30)
        print(f"\x1b[1;33mGeel:{env.now:>20}")
        yield env.timeout(5)
        print(f"\x1b[0;31mRood:{env.now:>20}")
        yield env.timeout(20)


def car(env):
    while True:
        print("\x1b[0m", end="")
        print(f"Auto: {env.now:>20}")
        parking_duration = 10
        yield env.timeout(parking_duration)


if __name__ == '__main__':
    main(100)
