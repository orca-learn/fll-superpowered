from spike import PrimeHub, App, Button, Speaker
from spike import LightMatrix, StatusLight
from spike import ForceSensor, MotionSensor, ColorSensor, DistanceSensor
from spike import Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import equal_to
from math import *

# Robot motors and sensors initialization
hub = PrimeHub()
drive_motor_pair = MotorPair('A', 'B')
drive_motor_left = Motor('A')
drive_motor_right = Motor('B')
front_motor = Motor('C')
back_motor = Motor('D')
color_sensor_left = ColorSensor('E')
color_sensor_right = ColorSensor('F')
motion_sensor = MotionSensor()

# Circumference (in cm) of small SPIKE Prime wheel
wheel_circumference = 17.5

# Min motor power
min_motor_power = 0

# Max motor power
max_motor_power = 100

# Speed at full power in cm/s
speed_at_max_motor_power = 39.123

# Number of steps to accel to max speed and decel to min speed
accel_steps = 10
decel_steps = 10

def move_fast(distance_cm):
    total_degrees = abs(distance_cm) * 360 / wheel_circumference
    drive_motor_left.set_degrees_counted(0)
    drive_motor_right.set_degrees_counted(0)
    motor = drive_motor_left if (distance_cm < 0) else drive_motor_right
    power = 40
    motion_sensor.reset_yaw_angle()
    while motor.get_degrees_counted() < total_degrees:
        correction = 0 - motion_sensor.get_yaw_angle()
        if motor.get_degrees_counted() < total_degrees - 360:
            power += 3
            if power > 100:
                power = 100
        else:
            power -= 10
            if power < 40:
                power = 40
        print (power)
        motor_power = power if (distance_cm > 0) else -power
        drive_motor_pair.start_tank_at_power(
            motor_power + correction, motor_power - correction)
    drive_motor_pair.stop()


def move(distance_cm, power=40):
    total_degrees = abs(distance_cm) * 360 / wheel_circumference
    drive_motor_left.set_degrees_counted(0)
    drive_motor_right.set_degrees_counted(0)
    motor = drive_motor_left if (distance_cm < 0) else drive_motor_right
    motor_power = power if (distance_cm > 0) else -power
    motion_sensor.reset_yaw_angle()
    while motor.get_degrees_counted() < total_degrees:
        correction = 0 - motion_sensor.get_yaw_angle()
        drive_motor_pair.start_tank_at_power(
            motor_power + correction, motor_power - correction)
    drive_motor_pair.stop()


def turn(angle_degrees, speed=10):
    left_speed = speed if (angle_degrees > 0) else -speed
    right_speed = speed if (angle_degrees < 0) else -speed
    drive_motor_pair.start_tank(left_speed, right_speed)
    motion_sensor.reset_yaw_angle()
    while abs(motion_sensor.get_yaw_angle()) < abs(angle_degrees):
        pass
    drive_motor_pair.stop()


def line_squaring():
    left_done = False
    right_done = False
    power = 20
    drive_motor_pair.start_tank_at_power(power, power)
    while not left_done and not right_done:
        if color_sensor_left.get_color() == 'black':
            left_done = True
            drive_motor_left.stop()
        if color_sensor_right.get_color() == 'black':
            right_done = True
            drive_motor_right.stop()


def follow_line(follow_sensor, distance_cm, correction_factor):
    total_degrees = abs(distance_cm) * 360 / wheel_circumference
    drive_motor_right.set_degrees_counted(0)
    power = 40
    while drive_motor_right.get_degrees_counted() < total_degrees:
        error = follow_sensor.get_reflected_light() - 50
        correction = round(error * correction_factor)
        drive_motor_pair.start_tank_at_power(
            power + correction, power - correction)
    drive_motor_pair.stop()


def follow_line_left_sensor(distance_cm):
    correction_factor = 0.3
    follow_line(color_sensor_left, distance_cm, correction_factor)


def follow_line_right_sensor(distance_cm):
    correction_factor = -0.3
    follow_line(color_sensor_right, distance_cm, correction_factor)


def follow_line_to_intersection(follow_sensor, stop_sensor, correction_factor):
    power = 35
    while stop_sensor.get_color() != 'black':
        error = follow_sensor.get_reflected_light() - 50
        correction = round(error * correction_factor)
        drive_motor_pair.start_tank_at_power(
            power + correction, power - correction)
    drive_motor_pair.stop()


def follow_line_to_intersection_left_sensor():
    correction_factor = 0.3
    follow_line_to_intersection(color_sensor_left, color_sensor_right, correction_factor)


def follow_line_to_intersection_right_sensor():
    correction_factor = -0.3
    follow_line_to_intersection(color_sensor_right, color_sensor_left, correction_factor)

def path1():
    # follow path to intersection
    move(23)
    turn(4)
    follow_line_to_intersection_left_sensor()
    turn(20)

    # get 2 energy units
    move(22)

    # lining up with oil rig
    move(-11)
    turn(58)
    follow_line_right_sensor(5)

    # do oil rig
    move(-15, 60)
    move(10)
    move(-12, 60)
    move(10)
    move(-12, 60)

    # get engery unit
    follow_line_right_sensor(31)
    turn(-50)
    move(13)
    move(-14)
    turn(50)

    # get to intersection
    follow_line_left_sensor(40)
    follow_line_to_intersection_left_sensor()

    # back up and turn left
    move(-5)
    turn(-45)
    move(-5)
    turn(-40)

    # push hand
    move(14)
    move(-3)

    # flip car lever
    turn(60,50)
    move(-21)
    turn(10)
    follow_line_left_sensor(10)
    follow_line_to_intersection_left_sensor()
    move(2)
    turn(35)

    # go home
    move_fast(90)

def path2():
    move(45)
    move(-5)
    turn (-45)
    move(41)
    turn (90)
    move(15.5)
    move(-10)
    move(10)
    move(-10)
    move(10)
    move(-10)
    move(10)
    move(-8)
    turn(110)
    move(51,100)

def path3():
    move(45,35)
    move(-50,85)

def path4():
    move(75)
    line_squaring()
    move(3)
    turn (90)
    move(-11,70)
    move(7)
    turn (-90)
    move(97,70)




