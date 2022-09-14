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


def move(distance_cm):
    total_degrees = abs(distance_cm) * 360 / wheel_circumference
    drive_motor_left.set_degrees_counted(0)
    drive_motor_right.set_degrees_counted(0)
    motor = drive_motor_left if (distance_cm < 0) else drive_motor_right
    power = 50
    motor_power = power if (distance_cm > 0) else -power
    motion_sensor.reset_yaw_angle()
    while motor.get_degrees_counted() < total_degrees:
        correction = 0 - motion_sensor.get_yaw_angle()
        drive_motor_pair.start_tank_at_power(
            motor_power + correction, motor_power - correction)
    drive_motor_pair.stop()


def turn(angle_degrees):
    speed = 3
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
    speed = 20
    drive_motor_pair.start_tank(-speed, speed)
    while not left_done and not right_done:
        if color_sensor_left.get_color() == 'black':
            left_done = True
            drive_motor_left.stop()
        if color_sensor_right.get_color() == 'black':
            right_done = True
            drive_motor_right.stop()


def follow_line(follow_sensor, distance_cm):
    total_degrees = abs(distance_cm) * 360 / wheel_circumference
    drive_motor_left.set_degrees_counted(0)
    drive_motor_right.set_degrees_counted(0)
    motor_power = 40
    while drive_motor_left.get_degrees_counted() < total_degrees:
        error = follow_sensor.get_reflected_light() - 50
        correction = round(error * 0.3)
        drive_motor_pair.start_tank_at_power(
            motor_power - correction, motor_power + correction)
    drive_motor_pair.stop()


def follow_line_left_sensor(distance_cm):
    follow_line(color_sensor_left, distance_cm)


def follow_line_right_sensor(distance_cm):
    follow_line(color_sensor_right, distance_cm)


def follow_line_to_intersection(follow_sensor, stop_sensor):
    drive_motor_left.set_degrees_counted(0)
    drive_motor_right.set_degrees_counted(0)
    motor_power = 40
    while stop_sensor.get_color() != 'black':
        error = follow_sensor.get_reflected_light() - 50
        correction = round(error * 0.3)
        drive_motor_pair.start_tank_at_power(
            motor_power - correction, motor_power + correction)
    drive_motor_pair.stop()


def follow_line_to_intersection_left_sensor():
    follow_line_to_intersection(color_sensor_left, color_sensor_right)


def follow_line_to_intersection_right_sensor():
    follow_line_to_intersection(color_sensor_right, color_sensor_left)
