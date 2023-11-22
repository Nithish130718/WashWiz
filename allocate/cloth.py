from abc import ABC, abstractmethod

class Cloth(ABC):
    def __init__(self, quantity, time_taken):
        self.quantity = quantity
        self.time_taken = time_taken

    @abstractmethod
    def calculate_cost(self):
        pass

    @abstractmethod
    def get_cloth_details(self):
        pass

class WoolCloth(Cloth):
    def __init__(self, quantity, time_taken):
        super().__init__(quantity, time_taken)

    def calculate_cost(self):
        return 5.0 * self.quantity

    def get_cloth_details(self):
        return f"Wool Cloth - Quantity: {self.quantity}, Time Taken: {self.time_taken} hours"

class SilkCloth(Cloth):
    def __init__(self, quantity, time_taken):
        super().__init__(quantity, time_taken)

    def calculate_cost(self):
        return 8.0 * self.quantity

    def get_cloth_details(self):
        return f"Silk Cloth - Quantity: {self.quantity}, Time Taken: {self.time_taken} hours"

class WhiteCloth(Cloth):
    def __init__(self, quantity, time_taken):
        super().__init__(quantity, time_taken)

    def calculate_cost(self):
        return 4.0 * self.quantity

    def get_cloth_details(self):
        return f"White Cloth - Quantity: {self.quantity}, Time Taken: {self.time_taken} hours"

class CottonCloth(Cloth):
    def __init__(self, quantity, time_taken):
        super().__init__(quantity, time_taken)

    def calculate_cost(self):
        return 6.0 * self.quantity

    def get_cloth_details(self):
        return f"Cotton Cloth - Quantity: {self.quantity}, Time Taken: {self.time_taken} hours"

class PolyesterCloth(Cloth):
    def __init__(self, quantity, time_taken):
        super().__init__(quantity, time_taken)

    def calculate_cost(self):
        return 7.0 * self.quantity

    def get_cloth_details(self):
        return f"Polyester Cloth - Quantity: {self.quantity}, Time Taken: {self.time_taken} hours"

class LinenCloth(Cloth):
    def __init__(self, quantity, time_taken):
        super().__init__(quantity, time_taken)

    def calculate_cost(self):
        return 9.0 * self.quantity

    def get_cloth_details(self):
        return f"Linen Cloth - Quantity: {self.quantity}, Time Taken: {self.time_taken} hours"
