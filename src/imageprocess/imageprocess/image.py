import cv2
import numpy as np
import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from tku_msgs.msg import Camera,ButtonColorForm,HSVValue
from tku_msgs.srv import HSVInfo,SaveHSV
from rclpy.node import Node
import configparser
import os
from tku_msgs.srv import SetString
import time
import json

class ImageSubscriber(Node):

    class HSVColorRange:
        def __init__(self):
            self.hmin = 0
            self.hmax = 0
            self.smin = 0
            self.smax = 0
            self.bmin = 0
            self.bmax = 0

    def __init__(self):
        super().__init__('image_subscriber')
        self.path_manager_client = self.create_client(SetString, 'set_file_path')
        while not self.path_manager_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.get_file_path()
        self.path_manager_client = self.create_client(SetString, '/get_file_path')
        #########################################################################
        self.building_model_subscription = self.create_subscription(
            ButtonColorForm,
            'ColorModelForm_Topic',
            self.building_model_callback,
            10
        )
        self.building_model_subscription  # prevent unused variable warning
        self.hsv_value_subscription = self.create_subscription(
            HSVValue,
            'HSVValue_Topic',
            self.hsv_value_callback,
            10
        )
        self.hsv_value_subscription  # prevent unused variable warning
        #########################################################################
        self.publisher      = self.create_publisher(Image, 'processed_image', 10)
        self.save_hsv_srv   = self.create_service(SaveHSV, '/SaveHSV',      self.save_hsv_callback)
        self.srv            = self.create_service(HSVInfo, '/LoadHSVInfo',  self.adjust_image_callback)
        self.bridge         = CvBridge()
        self.hsvcolorranger = self.HSVColorRange()
        self.colorselectrd  = ""
        self.hsvcolorraberdict   = {}
        self.color_ranges = {}  # Add this line

        self.current_color_label = 0
        self.building_model      = False

    def load_hsv_values(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.file_path + '/ColorModelData.ini')
        except configparser.Error as e:
            self.get_logger().error(f"Failed to read ColorModelData.ini: {e}")
            return
        if not config.sections():
            self.get_logger().info("ColorModelData.ini is empty or does not exist.")
            return

        for color in config.sections():
            hsvrange = self.HSVColorRange()
            try:
                hsvrange.hmin = config.getint(color, 'hmin')
                hsvrange.hmax = config.getint(color, 'hmax')
                hsvrange.smin = config.getint(color, 'smin')
                hsvrange.smax = config.getint(color, 'smax')
                hsvrange.bmin = config.getint(color, 'bmin')
                hsvrange.bmax = config.getint(color, 'bmax')
            except configparser.Error as e:
                self.get_logger().error(f"Failed to read section {color} from ColorModelData.ini: {e}")
                continue
            self.hsvcolorraberdict[color] = {'lower': np.array([hsvrange.hmin, hsvrange.smin, hsvrange.bmin]), 'upper': np.array([hsvrange.hmax, hsvrange.smax, hsvrange.bmax])}
            # self.get_logger().info(f"Loaded HSV values for color {color}: {self.hsvcolorraberdict[color]}")

        # Check if color label 0 is in the dictionary
        if '0' not in self.hsvcolorraberdict:
            self.get_logger().error("Color label 0 not found in hsvcolorraberdict")
            self.hsvcolorraberdict['0'] = {'lower': np.array([0, 0, 0]), 'upper': np.array([0, 0, 0])}  # Add default values for color label 0
            
################## save hsv value to ini file ##################
    def get_file_path(self):
        request = SetString.Request()
        future = self.path_manager_client.call_async(request)
        future.add_done_callback(self.handle_service_response)

    def handle_service_response(self, future):
        if future.result() is not None:
            self.file_path = future.result().data
            self.get_logger().info(f'File path is: {self.file_path}')
            self.load_hsv_values()  # Move the call to load_hsv_values here
        else:
            self.get_logger().info("Failed to get file_path parameter.")

    def save_hsv_callback(self, request, response):
        self.get_logger().info(f"Save status: {request.save}")
        
        if request.save:
            # Load the current color's HSV range from the .ini file
            config = configparser.ConfigParser()
            config.read(self.file_path + '/ColorModelData.ini')

            # Update the hsvcolorraberdict with the current color ranges
            for color, hsvrange in self.color_ranges.items():
                config[str(color)] = {
                    'hmin': hsvrange['lower'][0],
                    'hmax': hsvrange['upper'][0],
                    'smin': hsvrange['lower'][1],
                    'smax': hsvrange['upper'][1],
                    'bmin': hsvrange['lower'][2],
                    'bmax': hsvrange['upper'][2],
                }

            # Save the updated HSV range to the .ini file
            if not os.path.exists(self.file_path):
                self.get_logger().error(f"Path does not exist: {self.file_path}")  # Log the non-existing path
                return response
            try:
                with open(self.file_path + '/ColorModelData.ini', 'w') as configfile:
                    config.write(configfile)
            except PermissionError:
                self.get_logger().error(f"No permission to write to: {self.file_path}")  # Log the permission error
                return response
            response.already = True

            # After saving the parameters, load them again to confirm they have been saved correctly
            self.load_hsv_values()
        else:
            response.already = False
        return response
##############################################################
    
    def hsv_value_callback(self, msg):
        self.hmin = int(msg.hmin)
        self.hmax = int(msg.hmax)
        self.smin = int(msg.smin)
        self.smax = int(msg.smax)
        self.vmin = int(msg.vmin)
        self.vmax = int(msg.vmax)
        if self.current_color_label not in self.color_ranges:
            self.color_ranges[self.current_color_label] = {'lower': np.array([0, 0, 0]), 'upper': np.array([0, 0, 0])}
        self.color_ranges[self.current_color_label]['lower'] = np.array([self.hmin, self.smin, self.vmin])
        self.color_ranges[self.current_color_label]['upper'] = np.array([self.hmax, self.smax, self.vmax])
        self.get_logger().info(f"Updated HSV values from message: hmin={self.hmin}, hmax={self.hmax}, smin={self.smin}, smax={self.smax}, vmin={self.vmin}, vmax={self.vmax}")
    
    def building_model_callback(self, msg):
        self.building_model = bool(msg.buildingmodel)

    def camera_param_callback(self, msg):
            self.saturation = msg.saturation
            self.brightness = msg.brightness

    def adjust_image_callback(self, request, response):
        self.colorlabel_str = str(request.colorlabel)
        self.get_logger().info(f"Received request with color label: {self.colorlabel_str}")
        self.get_logger().info(f"Current hsvcolorraberdict: {self.hsvcolorraberdict}")

        if self.colorlabel_str not in self.hsvcolorraberdict:
            self.get_logger().error(f"Color label {self.colorlabel_str} not found in hsvcolorraberdict")
            return response
        # ...
        self.current_color_label = self.colorlabel_str  # Update the current color label
        self.hsvcolorranger = self.hsvcolorraberdict[self.colorlabel_str]
        self.colorselectrd = self.colorlabel_str
        response.hmin = int(self.hsvcolorraberdict[self.colorlabel_str]['lower'][0])
        response.hmax = int(self.hsvcolorraberdict[self.colorlabel_str]['upper'][0])
        response.smin = int(self.hsvcolorraberdict[self.colorlabel_str]['lower'][1])
        response.smax = int(self.hsvcolorraberdict[self.colorlabel_str]['upper'][1])
        response.vmin = int(self.hsvcolorraberdict[self.colorlabel_str]['lower'][2])
        response.vmax = int(self.hsvcolorraberdict[self.colorlabel_str]['upper'][2])

        self.get_logger().info(f"Returning HSV values: hmin={response.hmin}, hmax={response.hmax}, smin={response.smin}, smax={response.smax}, vmin={response.vmin}, vmax={response.vmax}")

        return response

    def image_callback(self,msg):
        bridge = CvBridge()
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except cv_bridge.CvBridgeError as e:
            print(e)

        # Convert the image from BGR to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Create a mask for the chosen color
        color_label = str(self.current_color_label)
        if not self.color_ranges or color_label not in self.color_ranges:
            self.get_logger().error(f"Color label {color_label} not found in color_ranges")
            return
        lower = self.color_ranges[color_label]['lower']
        upper = self.color_ranges[color_label]['upper']
        mask_color = cv2.inRange(hsv, lower, upper)

        # Perform erosion and dilation
        kernel = np.ones((3,3),np.uint8)
        kernel_1 = np.ones((1,1),np.uint8)        
        mask_color = cv2.erode(mask_color, kernel, iterations = 1)
        mask_color = cv2.dilate(mask_color, kernel, iterations = 2)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area and calculate contour information
        min_contour_area = 20  # Minimum contour area to keep
        mask_color_filtered = np.zeros_like(mask_color)
        contour_info = []  # List to hold contour information
        color_mapping = {
            0: [128, 0, 0],  # Orange -> Red in BGR
            1: [128, 128, 0],  # Yellow -> Olive in BGR
            2: [128, 0, 128],  # Blue -> Purple in BGR
            3: [0, 0, 128],  # Green -> Dark Blue in BGR
            4: [255, 0, 255],  # Black -> Magenta in BGR
            5: [255, 255, 0],  # Red1 -> Yellow in BGR
            6: [0, 255, 255],  # White -> Cyan in BGR
            7: [255, 0, 128],  # Other -> Pink in BGR
        }
        new_color = color_mapping[int(self.current_color_label)]
        cv_image[mask_color != 0] = new_color
        image_message = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        self.publisher.publish(image_message)
        
def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()
    # image_subscriber.call_service()
    subscription = image_subscriber.create_subscription(
        Image,
        'image_raw',
        image_subscriber.image_callback,
        10
    )
    subscription  # prevent unused variable warning

    camera_subscription = image_subscriber.create_subscription(
        Camera,
        'camera_parameters',
        image_subscriber.camera_param_callback,
        10
    )
    camera_subscription  # prevent unused variable warning

    rclpy.spin(image_subscriber)

    image_subscriber.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()