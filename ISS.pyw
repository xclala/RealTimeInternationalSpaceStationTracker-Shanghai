import ISS_Info
import turtle
from time import sleep, ctime
import json
import urllib.request

turtle.speed(0)
screen = turtle.Screen()
screen.setup(720, 360)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic("map.png")
screen.bgcolor("black")
screen.register_shape("isss.gif")
screen.title("Real time ISS tracker(ShangHai)")

iss = turtle.Turtle()
iss.shape("isss.gif")

iss.penup()  # Avoid a line being drawn from initiliation to first coord
iss.pen(pencolor="red", pensize=1)
style = ('Arial', 7, 'bold')

astronauts = turtle.Turtle()
astronauts.penup()
astronauts.color('black')
astronauts.goto(-178, 86)
astronauts.hideturtle()
url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
print("There are currently " + str(result["number"]) + " astronauts in space:")
print("")
astronauts.write("People in space: " + str(result["number"]), font=style)
astronauts.sety(astronauts.ycor() - 5)

# 上海
lat = 34.50000  #纬度
lon = 121.43333  #经度

people = result["people"]

for p in people:
    print(p["name"] + " on: " + p["craft"])
    astronauts.write(p["name"] + " on: " + p["craft"], font=style)
    astronauts.sety(astronauts.ycor() - 5)

url = 'http://api.open-notify.org/iss-pass.json?lat=' + \
    str(lat-90) + '&lon=' + str(lon)
response = urllib.request.urlopen(url)
result = json.loads(response.read())

over = result['response'][1]['risetime']
astronauts.write(f"ISS above Shanghai:{ctime(over)}", font=style)

screen.onkey(iss.clear(), "space")  # Allow us to clear history with spacebar
screen.listen()  # if screen gets too busy over time

while True:
    location = ISS_Info.iss_current_loc()
    lat = location['iss_position']['latitude']
    lon = location['iss_position']['longitude']
    print(f"Position: \n latitude: {lat}, longitude: {lon}")
    pos = iss.pos()
    posx = iss.xcor()
    if iss.xcor() >= (179.1):  # Stop drawing at the right edge of
        iss.penup()  # the screen to avoid a
        iss.goto(float(lon), float(lat))  # horizontal wrap round line
        sleep(0.5)
    else:
        iss.goto(float(lon), float(lat))
        iss.pendown()
        sleep(0.5)
