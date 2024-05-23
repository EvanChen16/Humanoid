import rclpy
from rclpy.node import Node
from tku_msgs.srv import SetString
import os
import argparse

class PathManager(Node):

    def __init__(self):
        super().__init__('path_manager')
        self.declare_parameter("file_path", "")  # Declare a new parameter
        self.service = self.create_service(SetString, 'set_file_path', self.handle_request)
        print(f'Initial file path: {self.get_parameter("file_path").value}')
        # self.get_path_service = self.create_service(SetString, 'get_file_path', self.handle_get_path_request)

    def handle_request(self, request, response):
        if request.data:
            # If the request data is not empty, set the file path
            self.set_file_path(request.data)
            response.data = 'File path set to: %s' % self.get_parameter("file_path").value
        else:
            # If the request data is empty, get the file path
            response.data = self.get_parameter("file_path").value
        return response

    def set_file_path(self, new_path):
        base_path = "/home/iclab/Desktop/ros2/src/strategy/"
        file_path = os.path.join(base_path, new_path, "Parameter")  # Remove the file name from the path
        print(f'File path set to: {file_path}')
        self.set_parameters([rclpy.parameter.Parameter("file_path", rclpy.parameter.Parameter.Type.STRING, file_path)])  # Update the parameter

def main(args=None):
    # Parse command line argument for the path
    parser = argparse.ArgumentParser(description='Set the path for the file.')
    parser.add_argument('path', type=str, help='The path to set.')
    args, unknown = parser.parse_known_args(args)

    # Initialize ROS
    rclpy.init(args=unknown)
    path_manager = PathManager()

    # Set the file path
    path_manager.set_file_path(args.path)

    rclpy.spin(path_manager)
    path_manager.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()