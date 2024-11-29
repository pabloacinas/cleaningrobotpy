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








