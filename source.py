
"""
    A file with all backend code - no integration, pure backend 
"""

import hashlib, json, re, datetime
from abc import abstractmethod
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from math import *
import heapq


def get_lat_long_from_address(address):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return (latitude, longitude)
    else:
        return None


with open("customers.json", "w") as file:
    test = [
        {"name": "Alex", "email": "test1@example.com", "phone": "9784561230"},
        {"name": "Bob", "email": "user1@example.com", "phone": "9876543210"},
        {"name": "Cathy", "email": "user2@example.com", "phone": "8765432109"},
        {"name": "Daniel", "email": "user3@example.com", "phone": "7654321098"},
        {"name": "Evelyn", "email": "user4@example.com", "phone": "6543210987"},
        {"name": "Fahad", "email": "user5@example.com", "phone": "5432109876"},
    ]
    json.dump(test, file)


with open("branches.json", "w") as file:
    test = [
        {"id": "B1", "location": "Tambaram", "lat": "12.9245279", "long": "80.1150525"},
        {
            "id": "B2",
            "location": "Kelambakkam",
            "lat": "12.7871437",
            "long": "80.219987",
        },
        {"id": "B3", "location": "Mambakkam", "lat": "12.5579793", "long": "79.986037"},
        {"id": "B4", "location": "TNagar", "lat": "13.0294483", "long": "80.2309064"},
        {
            "id": "B5",
            "location": "Anna Nagar",
            "lat": "11.1475163",
            "long": "79.0729829",
        },
    ]

    json.dump(test, file)

with open("service_points.json", "w") as file:
    test = [
        {
            "id": "S1",
            "location": "Ashok Pillar",
            "type": "dry-cleaning",
            "work_load": 1,
            "lat": 13.0316543,
            "long": 80.2122049,
        },
        {
            "id": "S2",
            "location": "Medavakkam",
            "type": "cold-water-wash",
            "work_load": 1,
            "lat": 12.9229928,
            "long": 80.1882897,
        },
        {
            "id": "S3",
            "location": "Selaiyur",
            "type": "hot-water-wash",
            "work_load": 1,
            "lat": 12.9187445,
            "long": 80.1311172,
        },
        {
            "id": "S4",
            "location": "Aminjikarai",
            "type": "spot-wash",
            "work_load": 1,
            "lat": 13.0721399,
            "long": 80.2205453,
        },
        {
            "id": "S5",
            "location": "Anna Nagar",
            "type": "white-cloth-wash",
            "work_load": 1,
            "lat": 13.0427322,
            "long": 80.2270781,
        },
    ]

    json.dump(test, file)


with open("transactions.json", "w") as file:
    test = [
        {
            "trxn_id": "T1",
            "date": str(datetime.datetime.today()),
            "type": "hot-water-wash",
            "service_point": "B1",
            "cost": 100,
            "quantity": 2,
        },
        {
            "trxn_id": "T2",
            "date": str(datetime.datetime.today()),
            "type": "cold-water-wash",
            "service_point": "B2",
            "cost": 100,
            "quantity": 2,
        },
        {
            "trxn_id": "T3",
            "date": str(datetime.datetime.today()),
            "type": "spot-wash",
            "service_point": "B3",
            "cost": 100,
            "quantity": 2,
        },
        {
            "trxn_id": "T4",
            "date": str(datetime.datetime.today()),
            "type": "cold-wash",
            "service_point": "B4",
            "cost": 100,
            "quantity": 2,
        },
        {
            "trxn_id": "T5",
            "date": str(datetime.datetime.today()),
            "type": "white-cloth-wash",
            "service_point": "B5",
            "cost": 100,
            "quantity": 2,
        },
        {
            "trxn_id": "T6",
            "date": str(datetime.datetime.today()),
            "type": "dry-cleaning",
            "service_point": "B6",
            "cost": 100,
            "quantity": 2,
        },
    ]

    json.dump(test, file)


global customers, phone_data, service_Points, branches
with open("customers.json", "r") as file:
    customers = json.load(file)
phone_data = [i["phone"] for i in customers]

with open("service_points.json", "r") as file:
    service_Points = json.load(file)

with open("branches.json", "r") as file:
    Branches = json.load(file)

with open("transactions.json", "r") as file:
    Transactions_data = json.load(file)


class Admin:
    instance = None

    def __init__(self, name, email, password) -> None:
        self.name = name
        self.email = email
        self.password = hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def get_instance(name, email, password):
        if Admin.instance is None:
            Admin.instance = Admin(name, email, password)
        return Admin.instance


user = Admin.get_instance("Joe", "Admin@example.com", "Admin@123")


class Customer:
    def __init__(self, name, email, phone):
        if phone in phone_data:
            ind = phone_data.index(phone)
            data = customers[ind]
            self.name = data["name"]
            self.email = data["email"]
            self.phone = data["phone"]
        else:
            self.name = name
            self.email = email
            self.phone = phone
            customers.append(
                {"name": self.name, "email": self.email, "phone": self.phone}
            )
            with open("customers.json", "w") as file:
                json.dump(customers, file)

    @staticmethod
    def search(phone):
        if phone in phone_data:
            ind = phone_data.index(phone)
            data = customers[ind]
            return data


a1 = Customer("Georgia", "test5@example.com", "9876543204")


class Wash:
    @abstractmethod
    def cost(self):
        pass


class DryCleaning(Wash):
    def __init__(self) -> None:
        self.name = "dry-cleaning"

    def cost(self, quantity):
        return quantity * 5


class ColdWaterWash(Wash):
    def __init__(self) -> None:
        self.name = "cold-water-wash"

    def cost(self, quantity):
        return quantity * 6


class HotWaterWash(Wash):
    def __init__(self) -> None:
        self.name = "hot-water-wash"

    def cost(self, quantity):
        return quantity * 6


class SpotWashing(Wash):
    def __init__(self) -> None:
        self.name = "spot-wash"

    def cost(self, quantity):
        return quantity * 8


class WhiteClothWash(Wash):
    def __init__(self) -> None:
        self.name = "white-cloth-wash"

    def cost(self, quantity):
        return quantity * 7


class WashTransaction:
    def __init__(self, wtype) -> None:
        self.wtype = wtype
        self.name = self.wtype.name

    def calculate_cost(self, quantity):
        return self.wtype.cost(quantity)


class HeadQuarters:
    instance = None

    def __init__(self, name) -> None:
        self.name = name
        self.service_points = {}
        self.branches = {}

    @staticmethod
    def get_instance(name, email, password):
        if Admin.instance is None:
            Admin.instance = Admin(name, email, password)
        return Admin.instance

    def add_service_point(self, service_point):
        if service_point.location not in self.service_points:
            self.service_points[service_point.location] = service_point

    def remove_Service_point(self, service_point):
        if service_point.location:
            print("ys")


class Branch(HeadQuarters):
    def __init__(self, location):
        self.id = "B" + str(int(Branches[-1]["id"][-1]) + 1)
        self.location = location
        if vars(self) not in Branches:
            Branches.append(
                {
                    "id": self.id,
                    "location": self.location,
                    "lat": str(get_lat_long_from_address(self.location + ",India")[0]),
                    "long": str(get_lat_long_from_address(self.location + ",India")[1]),
                }
            )
            with open("branches.json", "w") as file:
                json.dump(Branches, file)


class Service_Point(HeadQuarters):
    def __init__(self, location, wtype):
        self.id = "B" + str(int(service_Points[-1]["id"][-1]) + 1)
        self.location = location
        self.type = wtype
        self.work_load = 0
        if vars(self) not in service_Points:
            service_Points.append(
                {
                    "id": self.id,
                    "location": self.location,
                    "type": self.type,
                    "work_load": self.work_load,
                }
            )
            with open("service_points.json", "w") as file:
                json.dump(service_Points, file)


# s = Service_Point("Vandalur", "hot-water-wash")
# print(vars(s))

b = Branch("Kodambakkam")


class Transaction:
    def __init__(self, id, cust_phone, order_date, wtype, service_point, quantity):
        self.id = id
        self.cust_phone = cust_phone
        self.order_date = order_date
        self.wtype = wtype
        self.quantity = quantity
        self.service_point = service_point
        self.cost = self.calculate_cost()
        Transactions_data.append(
            {
                "trxn_id": self.id,
                "date": str(datetime.datetime.today()),
                "type": self.wtype.name,
                "service_point": self.service_point,
                "cost": self.cost,
                "quantity": self.quantity,
            }
        )
        with open("transactions.json", "w") as file:
            json.dump(Transactions_data, file)

    def calculate_cost(self):
        cost = self.wtype.calculate_cost(self.quantity)
        return cost


"""
d = DryCleaning()
t1 = Transaction("T7", "7492893", "7282", WashTransaction(d), "S1", 2)
t1.calculate_cost()"""


class TransactionStates:
    @abstractmethod
    def change_state(self):
        pass


class Order_Placed(TransactionStates):
    def change_state(self):
        return Allocated_Service_Point()


class Allocated_Service_Point(TransactionStates):
    def change_state(self):
        return Processing()


class Processing(TransactionStates):
    def change_state(self):
        return Cloths_Retrieved()


class Cloths_Retrieved(TransactionStates):
    def change_state(self):
        return Order_Delivered()


class Order_Delivered(TransactionStates):
    def change_state(self):
        return 0


class Transaction:
    def _init_(self, id, cust_phone, order_date, wtype, service_point, quantity):
        self.id = id
        self.cust_phone = cust_phone
        self.order_date = order_date
        self.wtype = wtype
        self.quantity = quantity
        self.service_point = service_point
        self.state = Order_Placed()
        self.cost = self.calculate_cost()
        Transactions_data.append(
            {
                "trxn_id": self.id,
                "date": str(datetime.datetime.today()),
                "type": self.wtype.name,
                "service_point": self.service_point,
                "cost": self.cost,
                "quantity": self.quantity,
            }
        )
        with open("transactions.json", "w") as file:
            json.dump(Transactions_data, file)

    def calculate_cost(self):
        cost = self.wtype.calculate_cost(self.quantity)
        return cost

    def change_state(self):
        self.state = self.state.change_state()

    def get_state(self):
        return type(self.state).__name__


"""
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of Earth in kilometers (you can use 3958.8 for miles)
    R = 6371.0

    # Calculate the distance
    distance = R * c

    return distance


def dijkstra(graph, start):
    distances = {node: float("infinity") for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


def find_nearest_service_point(branch_location, service_points):
    graph = {}

    # Add branches to the graph
    for branch in Branches:
        graph[branch["location"]] = {}

    # Add service points to the graph
    for service_point in service_points:
        graph[service_point["location"]] = {}

    # Add edges with distances using Haversine formula
    for branch in Branches:
        for service_point in service_points:
            distance = haversine(
                float(branch["lat"]),
                float(branch["long"]),
                float(service_point["lat"]),
                float(service_point["long"]),
            )
            graph[branch["location"]][service_point["location"]] = distance

    # Run Dijkstra's algorithm
    distances = dijkstra(graph, branch_location)

    # Find the nearest service point
    nearest_service_point = min(distances.items(), key=lambda x: x[1])

    return nearest_service_point


# Example usage
nearest_service_point = find_nearest_service_point("Tambaram", service_Points)
print("Nearest Service Point:", nearest_service_point)
"""


def filter_service_points(branch, wash_type):
    matching_service_points = []
    for service_point in service_Points:
        # print(service_point["location"],branch["location"],service_point["type"],wash_type)
        if service_point["type"] == wash_type:
            matching_service_points.append(service_point)

    return matching_service_points


def calculate_distance(coords1, coords2):
    return geodesic(coords1, coords2).kilometers


def allocate_clothes_to_service_point(branch, wash_type):
    matching_service_points = filter_service_points(branch, wash_type)
    if not matching_service_points:
        for service_point in service_Points:
            matching_service_points.append(service_point)
    print(matching_service_points)

    branch_id = branch["id"]
    branch_coords = (float(branch["lat"]), float(branch["long"]))
    print("Branch ID:", branch_id)

    graph = {service_point["id"]: [] for service_point in matching_service_points}
    graph[branch_id] = [0, 0]

    for service_point in matching_service_points:
        service_point_coords = (
            float(service_point["lat"]),
            float(service_point["long"]),
        )
        distance = calculate_distance(branch_coords, service_point_coords)
        graph[service_point["id"]] = [distance, service_point["work_load"]]

    print("Graph:", graph)

    # Apply Dijkstra's algorithm
    distances = {node: float("infinity") for node in graph}
    distances[branch_id] = 0.0

    priority_queue = [(0, branch_id)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, value in graph.items():
            total_distance = current_distance + value[0]
            if total_distance < distances[neighbor]:
                distances[neighbor] = total_distance
                heapq.heappush(priority_queue, (total_distance, neighbor))

    # Display the distances in order
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    # print("Shortest Distances:")
    # for node, distance in sorted_distances:
    #     if not node.startswith("B"):
    #         print(f"Service Point ID: {node}, Distance: {distance}")
    allocate = {}
    for service_point in sorted_distances:
        if not service_point[0].startswith("B"):
            allocate[service_point[0]] = graph[service_point[0]][1]
    print(allocate)

    for point, work_load in allocate.items():
        if work_load < 5:
            return point


# Example usage
branch_location = "Tambaram"
wash_type = "hot-water-wash"
branch = next((b for b in Branches if b["location"] == branch_location), None)
print(allocate_clothes_to_service_point(branch, wash_type))
