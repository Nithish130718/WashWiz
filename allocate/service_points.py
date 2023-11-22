class ServicePoint:
    def __init__(self, name, cloth_type):
        self.name = name
        self.cloth_type = cloth_type
        self.customer_cloths = {}

    def receive_cloths(self, customer_id, cloths):
        if customer_id not in self.customer_cloths:
            self.customer_cloths[customer_id] = cloths
            print(f"{self.name}: Cloths received from customer {customer_id}")
        else:
            print(f"{self.name}: Cloths from customer {customer_id} already received")

    def return_cloths(self, customer_id):
        if customer_id in self.customer_cloths:
            returned_cloths = self.customer_cloths.pop(customer_id, [])
            print(f"{self.name}: Cloths returned to customer {customer_id}")
            return returned_cloths
        else:
            print(f"{self.name}: No cloths received from customer {customer_id}")

