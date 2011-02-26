#!/usr/bin/env python
import rospy, time
from mavros_msgs.msg import OverrideRCIn
from sensor_msgs.msg import Joy
cmd = OverrideRCIn()
def callback(data):

    cmd.channels[0] = -data.axes[0] * 200 + 1500
    cmd.channels[1] = -data.axes[1] * 200 + 1500
    cmd.channels[2] = data.axes[3] * 200 + 1500
    cmd.channels[3] = -data.axes[2] * 200 + 1500
    cmd.channels[4] = 1500
    cmd.channels[5] = 1500
    cmd.channels[6] = 1500
    cmd.channels[7] = 1500

rospy.init_node("JOYSTICK")
cmd_vel_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10)
rospy.Subscriber("joy", Joy, callback)
while 1:
    cmd_vel_pub.publish(cmd)
    time.sleep(0.01)