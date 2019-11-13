import MelfaCmd
from time import sleep
from TCPClient import TCPClient
from typing import *


class MelfaRobot(object):
    """
    Class representing the physical robots with its unique routines, properties and actions.
    """

    def __init__(self, tcp_client, number_axes: int = 6):
        """
        Initialises the robot.
        :param tcp_client: Communication object for TCP/IP-protocol
        :param number_axes: Number of robot axes, declared by 'J[n]', n>=1
        """
        if not hasattr(tcp_client, 'send') or not hasattr(tcp_client, 'receive'):
            raise TypeError('TCP-client does not implement required methods.')
        if not number_axes > 0:
            raise TypeError('Illegal number of axes.')

        self.tcp: TCPClient = tcp_client
        self.joints: Iterable[AnyStr] = set(['J' + str(i) for i in range(1, number_axes + 1)])
        self.servo: bool = False
        self.com_ctrl: bool = False

    # Administration functions
    def start(self, safe_return: bool = True) -> None:
        """
        Starts the robot and initialises it.
        :param safe_return: Flag, whether the robot should return to its safe position
        :return: None
        """
        # Communication & Control on
        self.change_communication_state(True)
        # Servos on
        self.change_servo_state(True)
        # Safe position
        if safe_return:
            self.go_safe_pos()

    def shutdown(self, safe_return: bool = True) -> None:
        """
        Safely shuts down the robot.
        :param safe_return: Flag, whether the robot should return to its safe position
        :return: None
        """
        # Safe position
        if safe_return:
            self.go_safe_pos()
        # Servos off
        self.change_servo_state(False)
        # Communication & Control off
        self.change_communication_state(False)

    def maintenance(self):
        # Communication & Control on
        self.change_communication_state(True)

    # Utility functions
    def change_communication_state(self, activate: bool) -> None:
        """
        Obtain/release communication and control.
        :param activate: Boolean
        :return: None
        """
        if activate:
            # Open communication and obtain control
            self.tcp.send(MelfaCmd.COM_OPEN)
            self.tcp.receive()
            self.tcp.send(MelfaCmd.CNTL_ON)
            self.tcp.receive()
        else:
            # Open communication and obtain control
            self.tcp.send(MelfaCmd.CNTL_OFF)
            self.tcp.receive()
            self.tcp.send(MelfaCmd.COM_CLOSE)
            self.tcp.receive()

        self.com_ctrl = activate

    def change_servo_state(self, activate: bool) -> None:
        """
        Switch the servos on/off.
        :param activate: Boolean
        :return: None
        """
        if activate:
            self.tcp.send(MelfaCmd.SRV_ON)
            self.tcp.receive()
        else:
            self.tcp.send(MelfaCmd.SRV_OFF)
            self.tcp.receive()

        # Wait for servos to finish
        sleep(MelfaCmd.SERVO_INIT_SEC)
        self.servo = activate

    def reset_speed_factors(self):
        pass

    # Movement functions
    def go_safe_pos(self):
        pass

    def linear_move_poll(self):
        pass

    def circular_move_poll(self, is_clockwise):
        pass
