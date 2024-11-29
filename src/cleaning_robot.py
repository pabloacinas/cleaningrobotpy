import time

DEPLOYMENT = False  # This variable is to understand whether you are deploying on the actual hardware

try:
    import RPi.GPIO as GPIO
    import board
    import IBS
    DEPLOYMENT = True
except:
    import mock.GPIO as GPIO
    import mock.board as board
    import mock.ibs as IBS


class CleaningRobot:

    RECHARGE_LED_PIN = 12
    CLEANING_SYSTEM_PIN = 13
    INFRARED_PIN = 15

    # Wheel motor pins
    PWMA = 16
    AIN2 = 18
    AIN1 = 22

    # Rotation motor pins
    BIN1 = 29
    BIN2 = 31
    PWMB = 32
    STBY = 33

    N = 'N'
    S = 'S'
    E = 'E'
    W = 'W'

    LEFT = 'l'
    RIGHT = 'r'
    FORWARD = 'f'

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.INFRARED_PIN, GPIO.IN)
        GPIO.setup(self.RECHARGE_LED_PIN, GPIO.OUT)
        GPIO.setup(self.CLEANING_SYSTEM_PIN, GPIO.OUT)

        GPIO.setup(self.PWMA, GPIO.OUT)
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.PWMB, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.STBY, GPIO.OUT)

        ic2 = board.I2C()
        self.ibs = IBS.IBS(ic2)

        self.pos_x = None
        self.pos_y = None
        self.heading = None

        self.recharge_led_on = False
        self.cleaning_system_on = False

    def initialize_robot(self) -> None:
        self.pos_x = 0
        self.pos_y = 0
        self.heading = 'N'

    def robot_status(self) -> str:
        return f'({self.pos_x},{self.pos_y},{self.heading})'

    def execute_command(self, command: str) -> str:
        if self.ibs.get_charge_left() < 10:
            self.cleaning_system_on = False
            self.recharge_led_on = True
            return "!" + self.robot_status()
        if command == 'f': # Move the robot forward
            if self.obstacle_found():
                #if there is an obstacle return the robot status without moving
                return self.robot_status()+ f'({self.pos_x},{self.pos_y+1})'
            else:
                #if there is no obstacle move the robot forward
                self.activate_wheel_motor()
                if self.heading == self.N: # Move the robot forward
                    self.pos_y += 1
                elif self.heading == self.S: # Move the robot backward
                    self.pos_y -= 1
                elif self.heading == self.E: # Move the robot right
                    self.pos_x += 1
                elif self.heading == self.W: # Move the robot left
                    self.pos_x -= 1
        elif command == 'r':
            self.activate_rotation_motor(self.RIGHT) # Rotate the robot right
            if self.heading == self.N: # Change the heading of the robot to the right
                self.heading = self.E
            elif self.heading == self.E:
                self.heading = self.S
            elif self.heading == self.S:
                self.heading = self.W
            elif self.heading == self.W:
                self.heading = self.N
        elif command == 'l':
            self.activate_rotation_motor(self.LEFT) # Rotate the robot left
            if self.heading == self.N: # Change the heading of the robot to the left
                self.heading = self.W
            elif self.heading == self.W:
                self.heading = self.S
            elif self.heading == self.S:
                self.heading = self.E
            elif self.heading == self.E:
                self.heading = self.N
        return self.robot_status()

    def obstacle_found(self) -> bool:
        return GPIO.input(self.INFRARED_PIN) == GPIO.HIGH

    def manage_cleaning_system(self) -> None:
        if self.ibs.get_charge_left() < 0 or self.ibs.get_charge_left() > 100:
            raise CleaningRobotError("Invalid battery charge")
        elif self.ibs.get_charge_left() < 10:
            GPIO.output(self.RECHARGE_LED_PIN, GPIO.HIGH)
            self.recharge_led_on = True
            GPIO.output(self.CLEANING_SYSTEM_PIN, GPIO.LOW)
            self.cleaning_system_on = False
        elif self.ibs.get_charge_left() >= 10:
            GPIO.output(self.RECHARGE_LED_PIN, GPIO.LOW)
            self.recharge_led_on = False
            GPIO.output(self.CLEANING_SYSTEM_PIN, GPIO.HIGH)
            self.cleaning_system_on = True

    def rotate_n_times(self, n):
        for i in range(n):
            self.activate_rotation_motor('r') #Always rotate right
            if self.heading == self.N:
                self.heading = self.E
            elif self.heading == self.E:
                self.heading = self.S
            elif self.heading == self.S:
                self.heading = self.W
            elif self.heading == self.W:
                self.heading = self.N

        if n % 4 == 0: #If it does a full loop it means its multiple of 4
            return f"{self.robot_status()} LOOP"
        else:
            return self.robot_status()

    def activate_wheel_motor(self) -> None:
        """
        Let the robot move forward by activating its wheel motor
        """
        # Drive the motor clockwise
        GPIO.output(self.AIN1, GPIO.HIGH)
        GPIO.output(self.AIN2, GPIO.LOW)
        # Set the motor speed
        GPIO.output(self.PWMA, GPIO.HIGH)
        # Disable STBY
        GPIO.output(self.STBY, GPIO.HIGH)

        if DEPLOYMENT: # Sleep only if you are deploying on the actual hardware
            time.sleep(1) # Wait for the motor to actually move

        # Stop the motor
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)
        GPIO.output(self.PWMA, GPIO.LOW)
        GPIO.output(self.STBY, GPIO.LOW)

    def activate_rotation_motor(self, direction) -> None:
        """
        Let the robot rotate towards a given direction
        :param direction: "l" to turn left, "r" to turn right
        """
        if direction == self.LEFT:
            GPIO.output(self.BIN1, GPIO.HIGH)
            GPIO.output(self.BIN2, GPIO.LOW)
        elif direction == self.RIGHT:
            GPIO.output(self.BIN1, GPIO.LOW)
            GPIO.output(self.BIN2, GPIO.HIGH)

        GPIO.output(self.PWMB, GPIO.HIGH)
        GPIO.output(self.STBY, GPIO.HIGH)

        if DEPLOYMENT:  # Sleep only if you are deploying on the actual hardware
            time.sleep(1)  # Wait for the motor to actually move

        # Stop the motor
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)
        GPIO.output(self.PWMB, GPIO.LOW)
        GPIO.output(self.STBY, GPIO.LOW)

class CleaningRobotError(Exception):
    pass
