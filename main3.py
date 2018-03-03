from frequently_used import manipulate


class Car(object):
    """
    behave on the closest ride for a car
    """
    def __init__(self, key):
        self._id = key
        self._steps = 0
        self._position = [0, 0]
        self._available_rides = list()
        self._taken_rides = list()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        self._steps = value

    @property
    def available_rides(self):
        return self._available_rides

    @available_rides.setter
    def available_rides(self, value):
        self._available_rides = value

    @property
    def taken_rides(self):
        return self._taken_rides

    @taken_rides.setter
    def taken_rides(self, value):
        self._taken_rides = value

    def have_ride(self, ride):
        distance_to_ride = abs(self._position[0] - ride.start[0]) + abs(self._position[1] - ride.start[1])
        self._steps = self._steps + ride.distance + distance_to_ride
        self._position = ride.finish
        self._taken_rides.append(ride)

    def wait(self, steps):
        self._steps += steps

    def __str__(self):
        return 'car no: {},' \
               ' position: {},' \
               ' steps: {},' \
               ' available_rides:{}'.format(self._id,
                                            self._position,
                                            self._steps,
                                            self._available_rides)


class Ride(object):
    def __init__(self, key, start, finish, earliest_start, latest_finish):
        self._id = key
        self._start = start
        self._finish = finish
        self._earliest_start = earliest_start
        self._latest_finish = latest_finish
        self._distance = abs(self._start[0] - self._finish[0]) + abs(self._start[1] - self._finish[1])
        self._distance_from_car = int()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self.id = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, value):
        self._finish = value

    @property
    def earliest_start(self):
        return self._earliest_start

    @earliest_start.setter
    def earliest_start(self, value):
        self._earliest_start = value

    @property
    def latest_finish(self):
        return self._latest_finish

    @latest_finish.setter
    def latest_finish(self, value):
        self._latest_finish = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def distance_from_car(self):
        return self._distance_from_car

    @distance_from_car.setter
    def distance_from_car(self, value):
        self._distance_from_car = value

    def distance_from(self, car_position):
        self._distance_from_car = abs(self._start[0] - car_position[0]) + abs(self._start[1] - car_position[1])

    def __lt__(self, other):
        return self._distance_from_car < other.distance_from_car

    def __str__(self):
        return 'id: {},' \
               ' start:{},' \
               ' finish: {},' \
               ' earliest_start: {},' \
               ' latest finish: {},' \
               ' distance: {}'.format(self._id,
                                      self._start,
                                      self._finish,
                                      self._earliest_start,
                                      self._latest_finish,
                                      self._distance)


class CityMap(object):
    def __init__(self, filename):
        self._filename = filename
        self._extractor = manipulate(self._filename)
        self._rows = next(self._extractor)
        self._cls = next(self._extractor)
        self._cars_no = next(self._extractor)
        self._rides_no = next(self._extractor)
        self._bonus = next(self._extractor)
        self._steps = next(self._extractor)
        self._rides_objects = list()
        self._cars_objects = list()
        self._running = True
        self.init_rides()
        self.init_cars()
        self.assign_rides()

    @property
    def rows(self):
        return self._rows

    @property
    def cls(self):
        return self._cls

    @property
    def cars_no(self):
        return self._cars_no

    @property
    def rides_no(self):
        return self._rides_no

    @property
    def bonus(self):
        return self._bonus

    @property
    def steps(self):
        return self._steps

    @property
    def rides_objects(self):
        return self._rides_objects

    @rides_objects.setter
    def rides_objects(self, value):
        self._rides_objects = value

    @property
    def cars_objects(self):
        return self._cars_objects

    @cars_objects.setter
    def cars_objects(self, value):
        self._cars_objects = value

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        self._running = value

    def init_rides(self):
        for ride_no in range(self._rides_no):
            a = next(self._extractor)
            b = next(self._extractor)
            x = next(self._extractor)
            y = next(self._extractor)
            s = next(self._extractor)
            f = next(self._extractor)
            new_ride = Ride(ride_no, [a, b], [x, y], s, f)
            self._rides_objects.append(new_ride)

    def init_cars(self):
        for car_no in range(self._cars_no):
            car = Car(car_no)
            self._cars_objects.append(car)

    def assign_rides(self):
        while self._running:
            for car in self._cars_objects:
                self.calculate_trips(car.position)
                car.available_rides = sorted(self.rides_objects)

                for ride in car.available_rides:
                    whole_trip = ride.distance_from_car + ride.earliest_start
                    if whole_trip < ride.latest_finish:
                        if ride.earliest_start > car.steps:
                            car.wait(ride.earliest_start - car.steps)
                        car.have_ride(ride)
                        self._rides_objects.pop(self._rides_objects.index(ride))
                        break

            if self._rides_objects:
                self._running = True
            else:
                self._running = False

    def calculate_trips(self, car_position):
        for ride in self._rides_objects:
            ride.distance_from(car_position)


def main():
    file_names = ['a_example.in', 'b_should_be_easy.in', 'c_no_hurry.in', 'd_metropolis.in', 'e_high_bonus.in']
    file_index = 3
    city_map = CityMap(file_names[file_index])
    with open('{}.out'.format(file_names[file_index][:-3]), 'w') as file:
        for car in city_map.cars_objects:
            car_string = str(len(car.taken_rides))
            for ride in car.taken_rides:
                car_string += ' {}'.format(str(ride.id))
            car_string += '\n'
            file.write(car_string)


if __name__ == '__main__':
    print('Starting...\n-----------')
    main()
    print('-----------\nEnd')
