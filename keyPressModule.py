from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()


me.flip("l")
tello.move_forward(100)

tello.land()