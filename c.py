#Python iterators and generators
#1. Squares up to N
def squares(n):
    for i in range(n + 1):
        yield i * i
for x in squares(5):
    print(x)
#2. Even numbers
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
n = int(input("Enter a number: "))
print(','.join(str(i) for i in even_numbers(n)))
#3. Numbers divisible by 3 and 4
def div_by_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
for x in div_by_3_4(50):
    print(x)
#4. Squares between a and b
def squares_between(a, b):
    for i in range(a, b + 1):
        yield i * i
for x in squares_between(2, 5):
    print(x)
#5. Countdown
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
for x in countdown(5):
    print(x)
#Python Dates
#1. Subtract 5 days
from datetime import date, timedelta
today = date.today()
print("Today:", today)
print("5 days ago:", today - timedelta(days=5))
#2. Yesterday, Today, Tomorrow
from datetime import date, timedelta
today = date.today()
print("Yesterday:", today - timedelta(days=1))
print("Today:", today)
print("Tomorrow:", today + timedelta(days=1))
#3. Drop Microseconds
from datetime import datetime
now = datetime.now()
print("Without microseconds:", now.replace(microsecond=0))
#4. Date Difference in Seconds
from datetime import datetime
d1 = datetime(2025, 10, 1, 12, 0, 0)
d2 = datetime(2025, 10, 2, 12, 0, 0)
print("Difference in seconds:", (d2 - d1).total_seconds())
#Python Math
#1. Degree to Radian
import math
deg = 15
print("Radian:", math.radians(deg))
#2. Area of Trapezoid
h = 5
a = 5
b = 6
area = 0.5 * (a + b) * h
print("Area:", area)
#3. Area of Regular polygon
import math
n = 4
s = 25
area = (n * s**2) / (4 * math.tan(math.pi / n))
print("Area:", area)
#4. Area of Parallelogram
b = 5
h = 6
print("Area:", b * h)
#Python JSON
import json
with open("sample-data.json") as f:
    data = json.load(f)
print("Interface Status")
print("=" * 70)
print("DN".ljust(50), "Description".ljust(15), "Speed", "MTU")
print("-" * 70)
for item in data["imdata"]:
    a = item["l1PhysIf"]["attributes"]
    print(a["dn"].ljust(50), a["descr"].ljust(15), a["speed"], a["mtu"])
