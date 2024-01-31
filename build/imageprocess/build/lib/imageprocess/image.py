import cv2
import numpy as np
import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from tku_msgs.msg import Camera,ButtonColorForm,HSVValue
from tku_msgs.srv import HSVInfo
from rclpy.node import Node

def nothing(x):
    pass

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.color_ranges = {
            0: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Orange
            1: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Yellow
            2: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Blue
            3: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Green
            4: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Black
            5: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Red
            6: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # White
            7: {'lower': np.array([0, 0, 0]), 'upper': np.array([180, 255, 255])},  # Other
        }
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
        self.publisher = self.create_publisher(Image, 'processed_image', 10)
        self.srv = self.create_service(HSVInfo, '/LoadHSVInfo', self.adjust_image_callback)
        self.bridge = CvBridge()
        self.saturation = 0
        self.brightness = 0
        self.current_color_label = 0
        self.building_model = False
        
    def hsv_value_callback(self, msg):
        hmin = int(msg.hmin / 2)  # Convert from 0-360 to 0-180
        hmax = int(msg.hmax / 2)
        smin = int(msg.smin * 2.55)  # Convert from 0-100 to 0-255
        smax = int(msg.smax * 2.55)
        vmin = int(msg.vmin * 2.55)  # Convert from 0-100 to 0-255
        vmax = int(msg.vmax * 2.55)
        self.color_ranges[self.current_color_label]['lower'] = np.array([hmin, smin, vmin])
        self.color_ranges[self.current_color_label]['upper'] = np.array([hmax, smax, vmax])
    def building_model_callback(self, msg):
        self.building_model = bool(msg.buildingmodel)

    def camera_param_callback(self, msg):
            self.saturation = msg.saturation
            self.brightness = msg.brightness

    def adjust_image_callback(self, request, response):
        self.current_color_label = request.colorlabel
        color_range = self.color_ranges[request.colorlabel]
        response.hmin = color_range['lower'][0].item()
        response.hmax = color_range['upper'][0].item()
        response.smin = color_range['lower'][1].item()
        response.smax = color_range['upper'][1].item()
        response.vmin = color_range['lower'][2].item()
        response.vmax = color_range['upper'][2].item()
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
        lower = self.color_ranges[self.current_color_label]['lower']
        upper = self.color_ranges[self.current_color_label]['upper']
        mask_color = cv2.inRange(hsv, lower, upper)

        # Display the result
        res_color = cv2.bitwise_and(cv_image, cv_image, mask=mask_color)
        image_message = self.bridge.cv2_to_imgmsg(res_color, encoding="bgr8")
        self.publisher.publish(image_message)

def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()

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