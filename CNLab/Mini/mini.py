import random
import matplotlib.pyplot as plt

class Station:
    def __init__(self, station_id):
        self.id = station_id
        self.has_frame = True
        self.backoff_time = 0
        self.collision_count = 0
        self.total_backoff = 0

    def ready_to_send(self):
        return self.has_frame and self.backoff_time == 0

    def handle_collision(self):
        self.collision_count += 1
        k = min(self.collision_count, 10)
        wait = random.randint(0, 2 ** k - 1)
        self.backoff_time = wait
        self.total_backoff += wait

    def tick(self):
        if self.backoff_time > 0:
            self.backoff_time -= 1


class Channel:
    def __init__(self):
        self.state = "IDLE"

    def reset(self):
        self.state = "IDLE"


def simulate(num_stations=5, simulation_time=1000):
    stations = [Station(i) for i in range(num_stations)]
    channel = Channel()

    success = 0
    collisions = 0

    for _ in range(simulation_time):
        for s in stations:
            s.tick()

        ready = [s for s in stations if s.ready_to_send()]

        if len(ready) == 0:
            channel.reset()
            continue

        if channel.state == "IDLE":
            if len(ready) == 1:
                success += 1
                ready[0].has_frame = False
            else:
                collisions += 1
                for s in ready:
                    s.handle_collision()
        else:
            for s in ready:
                s.backoff_time += 1

        channel.reset()

    total_backoff = sum(s.total_backoff for s in stations)
    avg_backoff = total_backoff / (success + collisions) if (success + collisions) > 0 else 0
    efficiency = success / (success + collisions) * 100 if (success + collisions) > 0 else 0
    print("\n--- CSMA/CD Simulation Results ---")
    print(f"Total Stations       : {num_stations}")
    print(f"Simulation Time Slots: {simulation_time}")
    print(f"Successful Frames    : {success}")
    print(f"Collisions Detected  : {collisions}")
    print(f"Channel Efficiency   : {efficiency:.2f}%\n")
    return efficiency, avg_backoff


def run_analysis():
    station_counts = range(2, 21, 2)
    efficiencies = []
    avg_backoffs = []

    for n in station_counts:
        eff, back = simulate(num_stations=n, simulation_time=2000)
        efficiencies.append(eff)
        avg_backoffs.append(back)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(station_counts, efficiencies, marker='o')
    plt.title("Efficiency vs Number of Stations")
    plt.xlabel("Number of Stations")
    plt.ylabel("Efficiency (%)")

    plt.subplot(1, 2, 2)
    plt.plot(station_counts, avg_backoffs, marker='o', color='orange')
    plt.title("Average Backoff Delay vs Number of Stations")
    plt.xlabel("Number of Stations")
    plt.ylabel("Average Backoff Delay (slots)")

    plt.tight_layout()
    plt.show()



run_analysis()
