# stop.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Stop(Node):
    def __init__(self):
        super().__init__('simple_mover')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.stop)

    def stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Stop move command')

def main(args=None):
    rclpy.init(args=args)
    Stoper = Stop()
    rclpy.spin(Stoper)
    mover.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

