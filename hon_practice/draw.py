import turtle
def draw_square(arrow):
    for i in range(1,5):
        arrow.forward(100)
        arrow.right(90)


def draw_art():
    window = turtle.Screen()
    window.bgcolor("purple")

    brad = turtle.Turtle()
    brad.shape("circle")
    brad.color("yellow")
    brad.speed(1000)
    #brad.forward(200)
   

    for i in range(1,73):
        draw_square(brad)
        brad.right(5)
    for k in range(37,38):
        brad.right(90)
        brad.forward(200)
    window.exitonclick()

draw_art()


