from flask import Flask
from flask import render_template, redirect, request

app = Flask(__name__)

import hashlib, json, re, datetime
from abc import abstractmethod
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from math import *
import heapq

global total_transaction_count


def get_lat_long_from_address(address):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return (latitude, longitude)
    else:
        return None


with open("branches.json", "w") as file:
    homebranch = {
        "B1": {
            "name": "Kodambakkam",
            "email": "test1@example.com",
            "phone": "9784561230",
            "password": "Branch@123",
        }
    }
    json.dump(homebranch, file)

with open("service_points.json", "w") as file:
    test = {
        "S1": {
            "location": "Ashok Pillar",
            "type": "dry-cleaning",
            "work_load": 1,
            "lat": 13.0316543,
            "long": 80.2122049,
        }
    }
    json.dump(test, file)


with open("transactions.json", "w") as file:
    test = {
        "T1": {
            "date": str(datetime.datetime.today()),
            "type": "hot-water-wash",
            "service_point": "S1",
            "cost": 100,
            "quantity": 2,
            "state": "Order_Placed",
        }
    }
    json.dump(test, file)

global service_Points, branches, headquarters_data

with open("service_points.json", "r") as file:
    service_Points = json.load(file)

with open("branches.json", "r") as file:
    Branches = json.load(file)
    branch_usernames = [d["email"] for d in list(Branches.values())]
    admins = [
        (outer_key, list(inner_dict.items()))
        for outer_key, inner_dict in Branches.items()
    ]
    # temp = list(Branches.values())
    # Branch_emails = [d["email"] for d in temp]

with open("transactions.json", "r") as file:
    Transactions_data = json.load(file)


class HeadQuarters:
    instance = None

    def __init__(self, username, password) -> None:
        self.name = username
        self.password = password

    @staticmethod
    def get_instance(name, email, password):
        if HeadQuarters.instance is None:
            HeadQuarters.instance = HeadQuarters(name, email, password)
        return HeadQuarters.instance

    def remove_branch(self, b_id):
        del Branches[b_id]
        with open("branches.json", "w") as file:
            json.dump(Branches, file)

    def remove_Service_point(self, sid):
        del service_Points[sid]
        with open("service_points.json", "w") as file:
            json.dump(service_Points, file)


hq = HeadQuarters("hq@example.com", "Hq@123")
with open("headquarters.json", "w") as file:
    credentials = {hq.name: hq.password}
    json.dump(credentials, file)


class Branch(HeadQuarters):
    def __init__(self, name, email, phone):
        self.location = name
        self.email = email
        self.phone = phone
        self.password = "Branch@123"
        latest_id = ((list(Branches.keys()))[-1])[-1]
        self.id = "B" + str(int(latest_id) + 1)
        insert_data = {
            self.id: {
                "location": self.location,
                "email": self.email,
                "phone": self.phone,
                "password": self.password,
            }
        }
        Branches.update(insert_data)
        with open("branches.json", "w") as file:
            json.dump(Branches, file)


class Service_Point(HeadQuarters):
    def __init__(self, location, wtype, lat=None, long=None):
        latest_id = ((list(service_Points.keys()))[-1])[-1]
        self.id = "S" + str(int(latest_id) + 1)
        self.location = location
        self.type = wtype
        self.work_load = 0
        coordinates = get_lat_long_from_address(self.location + ", TamilNadu, India")
        if lat is None and long is None:
            self.lat = coordinates[0]
            self.long = coordinates[1]
        else:
            self.lat, self.long = lat, long
        if vars(self) not in list(service_Points.values()):
            insert_data = {
                self.id: {
                    "location": self.location,
                    "type": self.type,
                    "work_load": self.work_load,
                    "lat": self.lat,
                    "long": self.long,
                }
            }
            service_Points.update(insert_data)
            with open("service_points.json", "w") as file:
                json.dump(service_Points, file)


a2 = Branch(
    name="Anna Nagar",
    email="branch2@example.com",
    phone="9876543210",
)
a3 = Branch(
    name="Kelambakkam",
    email="branch3@example.com",
    phone="8765432109",
)
a4 = Branch(
    name="Selaiyur",
    email="branch4@example.com",
    phone="7654321098",
)
a5 = Branch(
    name="Medavakkam",
    email="branch5@example.com",
    phone="6543210987",
)
a6 = Branch(
    name="Guindy",
    email="branch6@example.com",
    phone="5432109876",
)
a7 = Branch(
    name="Poonamallee",
    email="branch7@example.com",
    phone="9876543204",
)


sp2 = Service_Point("Medavakkam", "cold-water-wash", 12.9229928, 80.1882897)
sp3 = Service_Point("Selaiyur", "hot-water-wash", 12.9187445, 80.1311172)
sp4 = Service_Point("Aminjikarai", "spot-wash", 13.0721399, 80.2205453)
sp5 = Service_Point(
    "Anna Nagar",
    "white-cloth-wash",
    13.0427322,
    80.2270781,
)


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


global wash_types
wash_types = 5


class WashTransaction:
    def __init__(self, wtype) -> None:
        self.wtype = wtype
        self.name = self.wtype.name

    def calculate_cost(self, quantity):
        return self.wtype.cost(quantity)


# s = Service_Point("Vandalur", "hot-water-wash")
# print(vars(s))


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
    total_transaction_count = 19

    def __init__(self, cust_phone, wtype, service_point, quantity):
        latest_id = ((list(Transactions_data.keys()))[-1])[-1]
        self.id = "T" + str(int(latest_id) + 1)
        self.cust_phone = cust_phone
        self.order_date = str(datetime.datetime.today())
        self.wtype = wtype
        self.quantity = quantity
        self.service_point = service_point
        self.state = Order_Placed()
        self.cost = self.calculate_cost()
        insert_data = {
            self.id: {
                "date": self.order_date,
                "type": self.wtype.name,
                "service_point": self.service_point,
                "cost": self.cost,
                "quantity": self.quantity,
                "state": self.get_state(),
            }
        }
        Transactions_data.update(insert_data)
        with open("transactions.json", "w") as file:
            json.dump(Transactions_data, file)
        Transaction.total_transaction_count += 1

    def calculate_cost(self):
        cost = self.wtype.calculate_cost(self.quantity)
        return cost

    def change_state(self):
        self.state = self.state.change_state()
        self.state = self.get_state()
        val_dict = Transactions_data[self.id]
        val_dict["state"] = self.state
        Transactions_data[self.id] = val_dict

    def get_state(self):
        return type(self.state).__name__


"""d = DryCleaning()
t1 = Transaction("T7", "7492893", "7282", WashTransaction(d), "S1", 2)
t1.calculate_cost()"""

d2 = ColdWaterWash()
t2 = Transaction("9876543210", WashTransaction(d2), "S2", 2)
d3 = SpotWashing()
t3 = Transaction(
    "9784561230",
    WashTransaction(d3),
    "S3",
    2,
)
d4 = DryCleaning()
t4 = Transaction("8997456123", WashTransaction(d4), "S4", 2)
# t4.change_state()
d5 = WhiteClothWash()
t5 = Transaction("6797944413", WashTransaction(d5), "S5", 2)
d6 = ColdWaterWash()
t6 = Transaction("9794613213", WashTransaction(d6), "S6", 2)


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


"""# Example usage
branch_location = "Tambaram"
wash_type = "hot-water-wash"
branch = next((b for b in Branches if b["location"] == branch_location), None)
print(allocate_clothes_to_service_point(branch, wash_type))"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("loginpage.html")


"""def get_live_trxns():
    with open("transactions.json", "r") as file:
        Transactions_data = json.load(file)
    live_count = len(Transactions_data)
    return live_count


def get_live_branches():
    with open("branches.json", "r") as file:
        Branches = json.load(file)
    live_count = len(Branches)
    return live_count
"""


with open("headquarters.json", "r") as file:
    headquarters_data = json.load(file)


def get_live_count(file):
    with open(file, "r") as f:
        data = json.load(f)
    live_count = len(data)
    return (live_count, data)


@app.route("/logindash", methods=["POST", "GET"])
def logindash():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if str(username) in headquarters_data:
            if password == headquarters_data[username]:
                tran_len = len(Transactions_data)
                backup_password = headquarters_data[username]
                # print(f"Backup Password: {backup_password}")
                # print(f"Hashed Input: {password}")
                live_trxn_count = get_live_count("transactions.json")[0]
                return render_template(
                    "admindash.html",
                    tran_len=tran_len,
                    total_transaction_count=Transaction.total_transaction_count,
                    live_trxn_count=live_trxn_count,
                    processed_trxn_count=Transaction.total_transaction_count
                    - live_trxn_count,
                    service_point_count=get_live_count("service_points.json")[0],
                    branches_count=get_live_count("branches.json")[0],
                    wash_types=wash_types,
                    transaction_set=get_live_count("transactions.json")[1],
                )
        if (
            str(username) in branch_usernames
        ):  # Convert username to string for comparison
            index = branch_usernames.index(str(username))
            tran_len = len(Transactions_data)
            backup_password = admins[index]["password"]
            # print(f"Backup Password: {backup_password}")
            # print(f"Hashed Input: {password}")
            live_trxn_count = get_live_count("transactions.json")[0]
            if password == backup_password:
                return render_template("index.html")
            else:
                return render_template("error.html")

    # No need for the else block here, it will only execute if the preceding if condition is not met
    return render_template("error.html")


@app.route("/track")
def track():
    return render_template("track_order.html")


@app.route("/searchtrxn", methods=["POST", "GET"])
def searchtrxn():
    if request.method == "POST":
        trxn_id = request.form.get("search")
        print(trxn_id)
        if trxn_id in Transactions_data:
            return render_template(
                "searchtrxn.html", id=trxn_id, transaction=Transactions_data[trxn_id]
            )
        else:
            pass
    return render_template("wrongtrxn_id.html")


@app.route("/admindash")
def admindash():
    tran_len = len(Transactions_data)
    # print(f"Backup Password: {backup_password}")
    # print(f"Hashed Input: {password}")
    live_trxn_count = get_live_count("transactions.json")[0]
    return render_template(
        "admindash.html",
        tran_len=tran_len,
        total_transaction_count=Transaction.total_transaction_count,
        live_trxn_count=live_trxn_count,
        processed_trxn_count=Transaction.total_transaction_count - live_trxn_count,
        service_point_count=get_live_count("service_points.json")[0],
        branches_count=get_live_count("branches.json")[0],
        wash_types=wash_types,
        transaction_set=get_live_count("transactions.json")[1],
    )


@app.route("/addbranch")
def addbranch():
    return render_template("addbranch.html")


@app.route("/addbranchsuccess", methods=["POST", "GET"])
def addbranchsuccess():
    if request.method == "POST":
        area = request.form.get("area")
        latest_id = ((list(Transactions_data.keys()))[-1])[-1]
        ID = "B" + str(int(latest_id) + 1)
        obj = Branch(area, "test@example.com", "6978791819")
        insert_data = {
            obj.id: {
                "location": obj.location,
                "email": obj.email,
                "phone": obj.phone,
                "password": obj.password,
            }
        }
        Branches.update(insert_data)
        with open("branches.json", "w") as file:
            json.dump(Branches, file)
        return render_template("addbranchsuccess.html", branches=len(Branches))


@app.route("/addsp")
def addservicepoint():
    return render_template("addservicepoint.html")


@app.route("/addspdata", methods=["POST", "GET"])
def savenewsp():
    if request.method == "POST":
        location = request.form.get("location")
        wtype = request.form.get("type")
        print(service_Points)
        sp = list(service_Points.values())
        temp = [(d["location"], d["type"]) for d in sp]
        if (location, wtype) in temp:
            return render_template("spalreadyexists.html")
        else:
            obj = Service_Point(location, wtype)
            number = len(list(service_Points.keys()))
            return render_template("addspsuccess.html", number=number)


@app.route("/admintransactions")
def admintrxns():
    return render_template(
        "admintransactions.html", transaction_set=get_live_count("transactions.json")[1]
    )


if __name__ == "__main__":
    app.run(debug=True)
