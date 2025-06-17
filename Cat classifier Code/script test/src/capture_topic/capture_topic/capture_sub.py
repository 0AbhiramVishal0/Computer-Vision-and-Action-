import sys
import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import torch
import numpy as np
import PIL.Image as PIL_Image
from rclpy.parameter import Parameter
import argparse


class CamCapture(Node):
    def __init__(self,name, save_path, num_max):
        super().__init__(name)
        self.cam_subscription=self.create_subscription(Image, '/depth_cam/rgb/image_raw', self.image_callback, 1)
        self.cv_bridge=CvBridge()
        self.save_path=save_path
        os.makedirs(self.save_path, exist_ok=True)
        self.num_max = num_max
        self.save_id = 0
        
    def image_callback(self,msg):
        image_bgr=self.cv_bridge.imgmsg_to_cv2(msg,"bgr8")
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        cv2.imshow("capture rgb image", image_rgb)
        cv2.imwrite(os.path.join(self.save_path, f'image{self.save_id}.jpg'), image_bgr)
        self.save_id = (self.save_id + 1) % self.num_max
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    parser = argparse.ArgumentParser(description='Save images from ROS2 topic')
    parser.add_argument('--save_path', type=str, default='~/script test/images')
    parser.add_argument('--num_max', type=int, default=1)
    parsed_args, unknown = parser.parse_known_args()
    node = CamCapture("capture_sub", parsed_args.save_path, parsed_args.num_max)
    rclpy.spin(node)
    rclpy.shutdown() 
