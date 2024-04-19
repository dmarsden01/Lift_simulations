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
        

class Lift_timesteps(object):

    def __init__(self, terminal_vel, N_terminal, max_floors) -> None:
        self.terminal_vel = terminal_vel
        self.N_terminal = N_terminal
        self.max_floors = max_floors
        # self.t_stop = t_stop
        # pass
        self.timesteps = 0
        self.target_floor = None
        self.velocity = 0
        self.acceleration = 0
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
        print(f"Current time is {self.timesteps} timesteps.")
        print(f"Current target floor is {self.target_floor}.")
        print(f"Current velocity is {str(self.velocity)}.")

    def Calculate_distance(self, time_units=1):
        distance = self.velocity*time_units + 0.5*self.acceleration*time_units**2

        return distance
    
    def Update_target(self, New_target):

        self.target_floor = New_target

    def Check_floor(self): #Need to tell it to go.
        if (self.acceleration == 0) and (self.velocity == 0):
            if self.target_floor != None:
                if self.location > self.target_floor:
                    self.acceleration = self.N_terminal/self.terminal_vel**2
                elif self.location < self.target_floor:
                    self.acceleration = -1*self.N_terminal/self.terminal_vel**2

    def Update_position(self, distance):
        if self.target_floor != None:
            distance_to_go = self.target_floor - self.location

            if abs(distance_to_go) <= abs(distance): #distance can be negative
                self.location = self.target_floor
                
            else:
                self.location += distance

    def Update_velocity_acc(self, time_units=1):
        added_vel = self.acceleration*time_units
        if abs(self.velocity+added_vel) >= abs(self.terminal_vel):
            self.velocity = self.terminal_vel
            self.acceleration = 0
        else:
            self.velocity += self.acceleration*time_units

    def Perform_timestep(self, time_steps):
        self.Check_floor()
        distance_calc = self.Calculate_distance(time_units=time_steps)
        self.Update_position(distance_calc)
        self.Update_velocity_acc(time_steps)

        # self.Update_target()

        self.timesteps +=1


    # def Update_acceleration(self, time_units=1):
    #     if self.velocity

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

    def add_step(self):

        self.timesteps +=1


    # def add_time_stop(self): #So far we are ignoring stopping time.
    #     self.total_time += self.t_stop