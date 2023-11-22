class Branch:
    def __init__(self, name):
        self.name = name
        self.service_points = {}
        self.customer_cloth = {}  

    def add_service_point(self, service_point):
        if service_point.name not in self.service_points:
            self.service_points[service_point.name] = service_point

    def add_cloth(self, destination, customer_id):
        if destination in self.edges:
            self.edges[destination].append(customer_id)
        else:
            self.edges[destination] = [customer_id]

    def receive_cloths_from_customer(self, customer_id, cloths):
        for service_point in self.service_points.values():
            service_point.receive_cloths(customer_id, cloths)

    def allocate_cloths_to_service_points(self, customer_id):
        for service_point in self.service_points.values():
            cloth_type = service_point.cloth_type
            if cloth_type in self.edges:
                self.add_edge(service_point.name, customer_id)
                service_point.receive_cloths(customer_id, self.edges[cloth_type])
                print(f"{self.name}: Cloths allocated to {service_point.name}")
            else:
                print(f"{self.name}: No customer info for cloth type {cloth_type}")

    def collect_cloths_from_service_points(self):
        for service_point in self.service_points.values():
            for customer_id in self.edges.get(service_point.name, []):
                returned_cloths = service_point.return_cloths(customer_id)
                self.edges[service_point.name].remove(customer_id)
                self.edges.setdefault("collected", []).extend(returned_cloths)
                print(f"{self.name}: Cloths collected from {service_point.name}")

    def return_cloths_to_customer(self, customer_id):
        if customer_id in self.edges:
            returned_cloths = self.edges.pop(customer_id, [])
            print(f"{self.name}: Cloths returned to customer {customer_id}")
            return returned_cloths
        else:
            print(f"{self.name}: No cloths received from customer {customer_id}")

