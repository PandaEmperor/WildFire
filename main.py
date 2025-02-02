import csv # used to manipulate the csv files
import heapq #men we love trees, used for the priority q
from datetime import datetime, timedelta # datetime managment


#The class fire is the main Object that represent the wildfire

class Fire:
    _id_counter_ = 0
    def __init__(self, timestamp, fire_start_time, severity,position): #main constrocter
        Fire._id_counter_ += 1 # keep track of uniue number for new id
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S") #given attribute
        self.fire_start_time = datetime.strptime(fire_start_time, "%Y-%m-%dT%H:%M:%S") #given attribute
        self.severity = severity#given attribute
        self.position = position#given attribute
        self.crew = None #which crews it was given
        self.ID = Fire._id_counter_ # its id
        self.mission_completion_time = None  # When will the crew end

    def __repr__(self): # printing the attribute
        return (f"Fire(timestamp={self.timestamp}, fire_start_time={self.fire_start_time}, "
                f"severity={self.severity}, latitude={self.latitude}, longitude={self.longitude})")

#Overloading the comparator based on the severity
    def __lt__(self, other):
        return self.severity < other.severity

    def __le__(self, other):
        return self.severity <= other.severity

    def __eq__(self, other):
        return self.severity == other.severity

    def __ne__(self, other):
        return self.severity != other.severity

    def __gt__(self, other):
        return self.severity > other.severity

    def __ge__(self, other):
        return self.severity >= other.severit

#priority q that has low severity at it is root and high at it leaf
class FirePriorityQueue:
    def __init__(self):
        self.heap = []

#function to add new object to the tree
    def add_fire(self, fire):
        # Use severity directly for min-heap behavior
        heapq.heappush(self.heap, (fire.severity, fire))
#function that is = to root.pop()
    def get_next_fire(self): #CUT THE HEAD MEN

        if self.heap:
            return heapq.heappop(self.heap)[1]  # Return the Fire object
        return None
#check if the tree is empty, return boolian
    def is_empty(self):
        return len(self.heap) == 0
#remove a fire object from the tree based on the id
    def remove(self, fire_id):
        # Find the index of the fire with the given ID
        for index, (severity, fire) in enumerate(self.heap):
            if fire.ID == fire_id:  # Access the Fire object from the tuple
                # Remove the fire from the heap
                self.heap[index] = self.heap[-1]  # Replace with the last element
                self.heap.pop()  # Remove the last element
                if index < len(self.heap):
                    heapq._siftup(self.heap, index)  # Restore heap property
                    heapq._siftdown(self.heap, 0, index)  # Restore heap property
                return  # Exit after removing the fire
#iterate over the tree that return tulips. TULIPS are stupid
    def iterate(self):
        """Iterate through the heap one by one without modifying it."""
        for fire in self.heap:
            yield fire  # Use a generator to yield each fire object
# the main class to discribe the available option
class Crew:
    def __init__(self, name, deployment_time, cost_per_operation, units_available):
        self.name = name
        self.deployment_time = deployment_time  # in minutes
        self.cost_per_operation = cost_per_operation  # in dollars
        self.units_available = units_available # this number will vary depends on the current

        self.total_units = units_available  # Initialize to the same number as units available

# function to determine the most important factor, we optimised based on the result
    @property
    def cost_per_minute(self):
        # Calculate cost per minute of deployment time
        return self.cost_per_operation / self.deployment_time

#update the fire object completion time to keep track of the crew
    def set_mission_completion_time(self, completion_time):
        """Set the mission completion time."""
        self.mission_completion_time = completion_time

    def get_mission_completion_time(self):
        """Get the mission completion time."""
        return self.mission_completion_time
#function to print the attributes
    def __str__(self):
        return (f"{self.name}: "
                f"Deployment Time: {self.deployment_time} minutes, "
                f"Cost per Operation: ${self.cost_per_operation}, "
                f"Units Available: {self.units_available}, "
                f"Total Units: {self.total_units}, "
                f"Mission Completion Time: {self.mission_completion_time}, "
                f"Cost per Minute: ${self.cost_per_minute:.2f}")


#convert String to number, for the severity
def severity_level(input_str):
    """
    Returns an integer based on the severity level.
    - Returns 1 for 'low'
    - Returns 2 for 'medium'
    - Returns 3 for 'high'
    - Returns None for invalid input
    """
    input_str = input_str.lower()  # Convert input to lowercase for case-insensitive comparison
    if input_str == 'low':
        return 0
    elif input_str == 'medium':
        return 1
    elif input_str == 'high':
        return 2
    else:
        return None  # Return None for invalid input
# the reverse of the function severity_levep()
def severity_string(level):
    """
    Returns a string based on the severity level.
    - Returns 'low' for 1
    - Returns 'medium' for 2
    - Returns 'high' for 3
    - Returns None for invalid input
    """
    if level == 0:
        return 'low'
    elif level == 1:
        return 'medium'
    elif level == 2:
        return 'high'
    else:
        return None  # Return None for invalid input

# converting time to an unified format
def convert_timestamp_format(timestamp):
    """
    Convert a timestamp from '%Y-%m-%d %H:%M:%S' to '%Y-%m-%dT%H:%M:%S'.

    Args:
    - timestamp: A string representing the timestamp in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
    - A string representing the timestamp in the format '%Y-%m-%dT%H:%M:%S'.
    """
    # Replace the space with 'T'
    return timestamp.replace(" ", "T")

#function that read the csv file and create object fire and return array fires
def read_fires_from_csv(file_path):
    fires = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header
        for row in csv_reader:
            if row:  # Check if the row is not empty
                fire = Fire(
                    timestamp=convert_timestamp_format(row[0]),
                    fire_start_time=convert_timestamp_format(row[1]),
                    severity=severity_level(row[3]),  # Read severity
                    position = row[2]
                )
                fires.append(fire)
    return fires


def time_difference(timestamp1, timestamp2):
    """
    Calculate the difference in minutes between two timestamps.

    Args:
    - timestamp1: A string representing the first timestamp in the format "YYYY-MM-DDTHH:MM:SS".
    - timestamp2: A string representing the second timestamp in the same format.

    Returns:
    - The absolute difference in minutes between the two timestamps.
    """
    # Parse the timestamps into datetime objects


    # Calculate the difference in minutes
    difference = (timestamp2-timestamp1).total_seconds() / 60
    return difference


def Damage_Costs_for_Missed_Responses(input_number):
    """
    Returns specific damage cost based on the input number.

    Args:
    - input_number: An integer (1, 2, or 3).

    Returns:
    - 50000 if input is 1
    - 100000 if input is 2
    - 200000 if input is 3
    - None for invalid input
    """
    if input_number == 0:
        return 50000
    elif input_number == 1:
        return 100000
    elif input_number == 2:
        return 200000
    else:
        return None  # Return None for invalid input
#function to return crews in priority based on the crew_array order
def find_available_crew(crews):
    for crew in crews:
        if crew.units_available > 0:
            crew.units_available -= 1# Decrement the available units
            return crew
    return None
#convert crew name to int to use as index
def crew_type_index(crew_type):
    if crew_type == "Fire Engines":
        return 0
    elif crew_type == "Ground Crews":
        return 1
    elif crew_type == "Tanker Planes":
        return 2
    elif crew_type == "Smoke Jumpers":
        return 3
    elif crew_type == "Helicopters":
        return 4
    else:
        return None  # Return None for unrecognized input
# main function
if __name__ == "__main__":

    total_operation_cost =0
    total_damage_cost = 0
    delayed_fires = 0
    addressed_fires = 0
    fire_type = [0, 0, 0]

    file_path = 'current_wildfiredata.csv'  # Path to your CSV file
    fires = read_fires_from_csv(file_path)

    # Creating instances for each type of crew
    # Positioned based on the Cost/Minute
    crew_array = [
        Crew("Fire Engines", 60, 2000, 10),
        Crew("Ground Crews", 90, 3000, 8),
        Crew("Tanker Planes", 120, 15000, 2),
        Crew("Smoke Jumpers", 30, 5000, 5),
        Crew("Helicopters", 45, 8000, 3)
    ]

    fire_queue = FirePriorityQueue()

    # Main loop where the magic happens
    for fyre in fires:
        if not (fire_queue.is_empty()):
            for severity, update in fire_queue.iterate():# Unpack the tuple here
                if time_difference(fyre.timestamp,update.mission_completion_time)<= 0:
                    crew_array[update.crew].units_available += 1
                    fire_queue.remove(update.ID)
                    addressed_fires+=1
                    fire_type[update.severity] += 1

#       find the chpeapest crew available
        crewx = find_available_crew(crew_array)
        if crewx is not None:
            fyre.crew = crew_type_index(crewx.name)
            total_operation_cost += crewx.cost_per_operation
            fyre.mission_completion_time = fyre.timestamp + timedelta(minutes=crewx.deployment_time)
            fire_queue.add_fire(fyre)
        else:
            if not fire_queue.is_empty() :
                temp = fire_queue.get_next_fire() # have to check if none or not

                if fyre.severity > temp.severity :
                    fyre.crew = temp.crew
                    fyre.mission_completion_time = fyre.timestamp + timedelta(minutes=crew_array[fyre.crew].deployment_time)
                    total_damage_cost += Damage_Costs_for_Missed_Responses(temp.severity)
                else:
                    delayed_fires += 1
                    fire_type[fyre.severity] += 1
#Empty the q at the end
    if not (fire_queue.is_empty()):
        for severity, update in fire_queue.iterate():  # Unpack the tuple here
            temp = fire_queue.get_next_fire()
            addressed_fires += 1
            fire_type[temp.severity] += 1



    print(f'Number of fires addressed: {addressed_fires}')
    print(f'Number of fires delayed: {delayed_fires}')
    print(f'Total operation costs: {total_operation_cost}')
    print(f'Estimated damage costs from delayed response: {total_damage_cost}')
    print("Fire severity report: {'low': " + str(fire_type[0]) + ".'medium': " + str(fire_type[1]) + ".'high': " + str(
        fire_type[2]) + "}")
