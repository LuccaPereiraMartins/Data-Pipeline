
class vehicle():

    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

    def seating_capacity(self, capacity):
        return f'the bus has {capacity} capacity'

    
class bus(vehicle):

    def __init__(self, name, max_speed, mileage):
        super().__init__(name, max_speed, mileage)

    def seating_capacity(self, capacity=50):
        return super().seating_capacity(capacity=capacity)

    def __str__(self):
        return f'{self.name}'

school_bus = bus("route_12", 100, 40)
print(school_bus,school_bus.seating_capacity(),sep="\n")