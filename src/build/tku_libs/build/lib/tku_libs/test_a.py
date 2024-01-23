import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from tku_msgs.msg import ButtonColorForm
class Tool(Node):

    def __init__(self):
        # self.node = rclpy.create_node('TKU_tool')
        super().__init__('TKU_tool')
        # self.initParameterPath()
        # self.publisher_ = self.create_publisher(ButtonColorForm,'topic',10)
        # self.i = 0
        # msg = ButtonColorForm()
        # msg.buildingmodel = self.i
        # self.publisher_.publish(msg)
        # self.i += 1
        # self.get_logger().info('publish: "%d"' %msg.buildingmodel)
        self.subscription = self.create_subscription(
            ButtonColorForm,
            'topic',
            self.callback,
            10)
        self.subscription
    # def time(self):
       
    def callback(self, msg):
        # msg = ButtonColorForm()
        # msg.buildingmodel = self.i
        # self.i = 1
        # self.publisher_.publish(msg)
        # self.get_logger().info('publish: "%d"' %msg.buildingmodel)
        self.get_logger().info('i heard: "%d" '%msg.buildingmodel)
#     def initParameterPath(self):
#         # Implement your parameter path initialization logic here
#         pass

#     def getPackagePath(self, package_name):
#         # Implement your getPackagePath logic here
#         pass

#     def readvalue(self, title, mode):
#         # Implement your readvalue logic here
#         pass

#     def Delay(self, timedelay):
#         # Implement your Delay logic here
#         pass

def main(args=None):
    rclpy.init(args=args)
    tool = Tool()
    # Add your main logic here
    rclpy.spin(tool)
    tool.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    # pass
