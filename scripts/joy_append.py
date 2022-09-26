#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy

class JoyAppend(object):
    def __init__(self):
        self.pub = rospy.Publisher("~joy_out", Joy, queue_size=1)
        self.joy_in = rospy.get_param("~joy_in", ["joy_in1","joy_in2"])
        self.msg_in = []
        self.sub = []
        self.last_stamp = rospy.Time.now()
        for topic_name , i in zip(self.joy_in, range(len(self.joy_in))):
            self.sub.append(rospy.Subscriber(topic_name, Joy, self.callback, callback_args=i, queue_size=1))
            self.msg_in.append(None)

    def callback(self, data, index):
        self.msg_in[index] = data
        if all(msg != None for msg in self.msg_in) and self.last_stamp < data.header.stamp:
            self.last_stamp = data.header.stamp
            msg_out = Joy()
            msg_out.header.stamp = data.header.stamp
            for msg in self.msg_in:
                msg_out.axes += msg.axes
                msg_out.buttons += msg.buttons
            self.pub.publish(msg_out)

if __name__ == '__main__':
    rospy.init_node("joy_append")
    n = JoyAppend()
    rospy.spin()
