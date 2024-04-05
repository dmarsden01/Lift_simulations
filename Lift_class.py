import numpy as np

class Lift(object):

    def __init__(self, terminal_vel, N_terminal, max_floors) -> None:
        self.terminal_vel = terminal_vel
        self.N_terminal = N_terminal
        self.max_floors = max_floors
        # self.t_stop = t_stop
        # pass
        self.requests = []
        self.requests_to = []
        self.location = 0
        self.direction = None
        self.num_drop_offs = 0
        self.num_stops = 0
        self.last_journey_distance = 0
        self.distance_travelled = 0
        self.total_time = 0
        self.time_operating = 0

    def info(self):
        print(f"Located at floor {self.location}.")
        print(f"Terminal velocity is {self.terminal_vel} floors per unit time.")
        print(f"Reaches terminal velocity after {self.N_terminal} floors.")
        print(f"Maximum floor is {self.max_floors}.")

    def request_from(self, floor, req_direction):
        self.requests.append({floor:req_direction})
    
    def request_to(self, floor):
        self.requests_to.append(floor)
    
    def move_to(self, floor):
        self.last_journey_distance = abs(floor-self.location)
        self.distance_travelled += abs(floor-self.location)
        self.location = floor
        self.num_stops += 1

    def calc_time_move(self, floors_moved):
        if (floors_moved < self.N_terminal):
            moving_time = np.sqrt(4*(floors_moved*self.N_terminal)/(self.terminal_vel**2))
        else:
            moving_time = (floors_moved+self.N_terminal)/self.terminal_vel

        return moving_time
        
    def add_time_move(self, floors_moved):
        if (floors_moved < self.N_terminal):
            moving_time = np.sqrt(4*(floors_moved*self.N_terminal)/(self.terminal_vel**2))
        else:
            moving_time = (floors_moved+self.N_terminal)/self.terminal_vel

        self.total_time += moving_time
        self.time_operating += moving_time

    # def add_time_stop(self): #So far we are ignoring stopping time.
    #     self.total_time += self.t_stop