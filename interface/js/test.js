// Using Object.assign
var obj1 = { a: 1 };
var obj2 = { b: 2 };
var combined = Object.assign({}, obj1, obj2);
console.log(combined); // { a: 1, b: 2 }

// Using spread operator
var obj3 = { a: 1 };
var obj4 = { b: 2 };
var combined2 = { ...obj3, ...obj4 };
console.log(combined2); // { a: 1, b: 2 }

var rclnodejs = require('rclnodejs');

rclnodejs.init().then(() => {
  var node = rclnodejs.createNode('my_node');

  // Replace Topic with Publisher and Subscriber
  var publisher = node.createPublisher('std_msgs/msg/String', 'my_topic');
  var subscriber = node.createSubscription('std_msgs/msg/String', 'my_topic', (msg) => {
    console.log('Received message:', msg.data);
  });

  // Replace Message with standard ROS2 messages
  var msg = {data: 'Hello, ROS2!'};
  publisher.publish(msg);

  // EventEmitter2 is not needed in ROS2
  // Use rclnodejs.spin(node) to handle events
  rclnodejs.spin(node);

  var actionClient = new rclnodejs.ActionClient(
    node,
    'test_msgs/action/Fibonacci',
    'fibonacci'
  );

  var goal = new rclnodejs.Goal(actionClient);
  goal.setOrder(10);

  goal.send();

  goal.on('feedback', (feedback) => {
    console.log('Received feedback:', feedback.sequence);
  });

  goal.on('result', (result) => {
    console.log('Received result:', result.sequence);
  });

  // If timeout specified, emit a 'timeout' event if the action server does not respond
  var timeout = 5000; // 5 seconds
  setTimeout(() => {
    if (!goal.isTerminalState()) {
      console.log('Timeout');
    }
  }, timeout);

}).catch(error => {
  console.error(error);
});

