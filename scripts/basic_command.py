#!/usr/bin/env python
import rospy, time, threading
from sensor_msgs.msg import Joy
from pynput.keyboard import Key, Listener
from mavros_msgs.srv import *
from mavros_msgs.msg import OverrideRCIn


def setMode(mode):
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        isModeChanged = flightModeService(custom_mode=mode)  # return true or false
    except rospy.ServiceException, e:
        print "service set_mode call failed: %s. " + mode + " Mode could not be set. Check that GPS is enabled" % e

def arming(value):
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(value)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s" % e

def takeoff(alt=5):
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
        req = mavros_msgs.srv.CommandTOLRequest()
        req.min_pitch = 0
        req.yaw = 0
        req.latitude = 0    # 47.397742
        req.longitude = 0   # 8.5455932
        req.altitude = alt
        takeoffService(req)
    except rospy.ServiceException, e:
        print "Service takeoff call failed: %s" % e

def land(alt=5):
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        req = mavros_msgs.srv.CommandTOLRequest()
        req.min_pitch = 0
        req.yaw = 0
        req.latitude = 0  # 47.397742
        req.longitude = 0  # 8.5455932
        req.altitude = alt
        landService(req)
    except rospy.ServiceException, e:
        print "Service land call failed: %s" % e

def callback(data):
    cmd.channels[0] = -data.axes[0] * 200 + 1500
    cmd.channels[1] = -data.axes[1] * 200 + 1500
    cmd.channels[2] = data.axes[3] * 200 + 1500
    cmd.channels[3] = -data.axes[2] * 200 + 1500
    cmd.channels[4] = 1500
    cmd.channels[5] = 1500
    cmd.channels[6] = 1500
    cmd.channels[7] = 1500

    if data.buttons[0]:
        print "ARMING"
        arming(True)
    elif data.buttons[1]:
        print "DISARMING"
        arming(False)
    elif data.buttons[2]:
        print "TAKEOFF"
        takeoff(5)
    elif data.buttons[3]:
        print "LAND"
        land()
    elif data.buttons[4]:
        mode = "RTL"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[5]:
        mode = "BRAKE"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[6]:
        mode = "LOITER"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[7]:
        mode = "GUIDED"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[8]:
        mode = "ALT_HOLD"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[9]:
        mode = "CIRCLE"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[10]:
        mode = "AUTO"
        print "Mode " + mode
        setMode(mode)
    elif data.buttons[11]:
        mode = "ACRO"
        print "Mode " + mode
        setMode(mode)

rospy.init_node("DRONE_CTRL")
cmd_vel_pub = rospy.Publisher("/mavros/rc/override", OverrideRCIn, queue_size=10)
rospy.Subscriber("/joy", Joy, callback)
cmd = OverrideRCIn()

while not rospy.is_shutdown():
    cmd_vel_pub.publish(cmd)
    time.sleep(0.01)