from agno.tools import Toolkit

class MathToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="math_toolkit")
        self.register(self.add_numbers)
        self.register(self.sub_numbers)
        self.register(self.multiply_numbers)
        self.register(self.divide_numbers)

    def add_numbers(self, a: int, b: int) -> str:  # Return as string
        return str(a + b)
    
    def sub_numbers(self, a: int, b: int) -> str:  # Return as string
        return str(a - b)
    
    def multiply_numbers(self, a: int, b: int) -> str:  # Return as string
        return str(a * b)

    def divide_numbers(self, a: int, b: int) -> str:  # Return as string
        if b == 0:
            return "Error: Division by zero"
        return str(a / b)  # Ensure the result is a string
