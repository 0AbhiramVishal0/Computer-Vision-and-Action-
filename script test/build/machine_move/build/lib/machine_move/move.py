# move.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import argparse

class Move(Node):
    def __init__(self, args):
        super().__init__('simple_mover')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.move)
        self.linear_vel = args.linear_vel
        self.angular_vel = args.angular_vel

    def move(self):
        msg = Twist()
        msg.linear.x = self.linear_vel
        msg.angular.z = self.angular_vel
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Forward move command')

def main(args=None):
    rclpy.init(args=args)
    parser = argparse.ArgumentParser(description='Machine Control')
    parser.add_argument('--linear_vel', type=float, default=0.01)
    parser.add_argument('--angular_vel', type=float, default=0.0)
    parsed_args, unknown = parser.parse_known_args()
    mover = Move(parsed_args)
    rclpy.spin(mover)
    mover.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

