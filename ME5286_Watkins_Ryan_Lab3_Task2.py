# This macro shows an example of running a program on the robot using the Python API (online programming)
# More information about the RoboDK API appears here:
# https://robodk.com/doc/en/RoboDK-API.html
from robolink import *    # API to communicate with RoboDK
from robodk import *      # robodk robotics toolbox
# Any interaction with RoboDK must be done through RDK:
RDK = Robolink()
# Select a robot (a popup is displayed if more than one robot is available)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception('No robot selected or available')
RUN_ON_ROBOT = False
# Important: by default, the run mode is RUNMODE_SIMULATE
# If the program is generated offline manually the runmode will be RUNMODE_MAKE_ROBOTPROG,
# Therefore, we should not run the program on the robot
if RDK.RunMode() != RUNMODE_SIMULATE:
    RUN_ON_ROBOT = False
if RUN_ON_ROBOT:

    # Connect to the robot using default IP
    success = robot.Connect() # Try to connect once
    status, status_msg = robot.ConnectedState()
    if status != ROBOTCOM_READY:
        # Stop if the connection did not succeed
        print(status_msg)
        raise Exception("Failed to connect: " + status_msg)
    # This will set to run the API programs on the robot and the simulator (online programming)
    RDK.setRunMode(RUNMODE_RUN_ROBOT)

# Get the current joint position of the robot
# (updates the position on the robot simulator)
joints_ref = robot.Joints()
# get the current position of the TCP with respect to the reference frame:
# (4x4 matrix representing position and orientation)
target_ref = robot.Pose()
pos_ref = target_ref.Pos()
# It is important to provide the reference frame and the tool frames when generating programs offline
# It is important to update the TCP on the robot mostly when using the driver
robot.setPoseFrame(robot.PoseFrame())
robot.setPoseTool(robot.PoseTool())
#robot.setZoneData(10) # Set the rounding parameter (Also known as: CNT, APO/C_DIS, ZoneData, Blending radius, cornering, ...)
robot.setSpeed(200) # Set linear speed in mm/s

# Setting Pose 1, Pose 2, and Pose 3 from the Lab Manual
# We enter our xyzrpw (X, Y, Z, RX, RY, RZ) into the function xyzrpw_2_pose()
# to convert out position and euler angles to a 4x4 pose matrix
# Start at the home position
home = [0, -90, 0, -90, 0, 0]

#Start Task 2 Program:

#since we are free driving to the position of the load cell, we don't have to move the robot pose at all, we will manually
#enter in the orientation ("RX:0","RY:3.146","RZ:0")

#initialize all the speeds and forces
forces = [0,1,50,100,127,128,150,200,255]
speeds = [25,50,75,105,150,200,250]

#initialize the gripper as open before starting the cycle:
robot.RunCodeCustom('rq_open_and_wait()',INSTRUCTION_CALL_PROGRAM)

#main for loop
for force in range (0,8):
    #Set force for next 7 iter
    robot.RunCodeCustom('rq_set_force(%i)' %forces[force],INSTRUCTION_CALL_PROGRAM)
    for speed in range (0,6):
        #Set speed for iter
        robot.RunCodeCustom('rq_set_speed(%i)' %speeds[speed],INSTRUCTION_CALL_PROGRAM)
        #Grasp
        robot.RunCodeCustom('rq_close_and_wait()',INSTRUCTION_CALL_PROGRAM)
        #Wait 2 seconds
        robot.RunCodeCustom('sleep(2)',INSTRUCTION_CALL_PROGRAM)
        #Fully open to be ready for next speed
        robot.RunCodeCustom('rq_open_and_wait()',INSTRUCTION_CALL_PROGRAM)
        
#Task 2 Complete
