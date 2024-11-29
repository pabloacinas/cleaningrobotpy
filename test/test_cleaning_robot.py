from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot
from src.cleaning_robot import CleaningRobotError


class TestCleaningRobot(TestCase):

    def test_initialize_robot(self):
        robot=CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(robot.pos_x, 0)
        self.assertEqual(robot.pos_y, 0)
        self.assertEqual(robot.heading, 'N')

    def test_robot_status(self):
        robot=CleaningRobot()
        robot.initialize_robot()
        status=robot.robot_status()
        self.assertEqual(status, '(0,0,N)')

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_turn_on_led_and_turn_off_cleaning_system_when_battery_below_10(self, mock_output: Mock, mock_ibs: Mock):
        mock_ibs.return_value = 9
        robot=CleaningRobot()
        robot.manage_cleaning_system()
        mock_output.assert_has_calls([call(robot.RECHARGE_LED_PIN, GPIO.HIGH), call(robot.CLEANING_SYSTEM_PIN, GPIO.LOW)])
        self.assertTrue(robot.recharge_led_on)
        self.assertFalse(robot.cleaning_system_on)

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_turn_off_led_and_turn_on_cleaning_system_when_battery_above_10(self, mock_output: Mock, mock_ibs: Mock):
        mock_ibs.return_value = 10
        robot=CleaningRobot()
        robot.manage_cleaning_system()
        mock_output.assert_has_calls([call(robot.RECHARGE_LED_PIN, GPIO.LOW), call(robot.CLEANING_SYSTEM_PIN, GPIO.HIGH)])
        self.assertFalse(robot.recharge_led_on)
        self.assertTrue(robot.cleaning_system_on)

    @patch.object(IBS, 'get_charge_left')
    @patch.object(GPIO, 'output')
    def test_invalid_battery_charge(self, mock_output: Mock, mock_ibs: Mock):
        mock_ibs.return_value = -1
        robot=CleaningRobot()
        self.assertRaises(CleaningRobotError, robot.manage_cleaning_system)

    def test_execute_command_forward(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.execute_command('f')
        self.assertEqual(robot.robot_status(), "(0,1,N)")

    def test_execute_command_right(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.execute_command('r')
        self.assertEqual(robot.robot_status(), "(0,0,E)")

    def test_execute_command_left(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.execute_command('l')
        self.assertEqual(robot.robot_status(), "(0,0,W)")

    @patch.object(GPIO, 'input')  # infrared sensor
    def test_obstacle_found(self, mock_input: Mock):
        mock_input.return_value = True
        robot = CleaningRobot()
        self.assertTrue(robot.obstacle_found())

    @patch.object(GPIO, 'input') #infrared sensor
    def test_execute_command_forward_with_obstacle(self, mock_input: Mock):
        mock_input.return_value = True
        robot = CleaningRobot()
        robot.initialize_robot()
        result=robot.execute_command('f')
        self.assertEqual(result, "(0,0,N)(0,1)") #if robot detects an obstacle, it should not move

    @patch.object(GPIO, 'input') #infrared sensor
    def test_execute_command_forward_without_obstacle(self, mock_input: Mock):
        mock_input.return_value = False
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.execute_command('f')
        self.assertEqual(robot.robot_status(), "(0,1,N)")

    @patch.object(IBS, 'get_charge_left')
    def test_execute_command_low_battery(self, mock_ibs: Mock):
        mock_ibs.return_value = 9
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command('f')
        self.assertEqual(result, "!(0,0,N)")








