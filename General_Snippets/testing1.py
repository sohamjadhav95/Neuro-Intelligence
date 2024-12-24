import subprocess
import math

def calc_sqrt(num):
    try:
        result = math.sqrt(num)
        subprocess.Popen(['calc', str(result)])
        print(f"The square root of {num}, which is {result}, has been sent to Windows Calculator.")
    except TypeError:
        print("Invalid input. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Cannot calculate the square root of a negative number.")



calc_sqrt(59)