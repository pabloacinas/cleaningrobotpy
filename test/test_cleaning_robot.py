from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot


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

    @patch.object(GPIO, 'output')
    def test_turn_on_led_and_turn_off_cleaning_system_when_battery_below_10(self, mock_output):
        robot=CleaningRobot()
        robot.initialize_robot()
        robot.ibs.get_charge_left.return_value = 9
        robot.manage_cleaning_system()
        mock_output.assert_called_once_with(robot.RECHARGE_LED_PIN, GPIO.HIGH)
        self.assertFalse(robot.cleaning_system_on)




