54# This macro shows an example of running a program on the robot using the Python API (online programming)
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

#Start Task 3 Program:


#initalize the position of the ping pong balls in the coordinate system of the tray (x,y) from lower left:
tray_balls=[[1.5,3.5],[3.5,1.5],[3.5,5.5],[5.5,3.5],[7.5,1.5],[7.5,5.5]]
#default gripper ori
gripper_ori = [0,0,0]

#set the height the gripper shoulds grab the balls at:
pick_height = 0
#set the height the gripper should move to to avoid hitting the other balls while moving
move_height = 0

#In order to find the transform for both the robot base  to pallet 1, and the base to pallet 2, we free drive the robot
#so that the gripper is flush with first the Y edge and then the X edge of the pallet, and record the pose of the robot
#Pallet 1:
source_y_pose = []
source_x_pose = []

#Pallet 2:
dest_y_pose = []
dest_x_pose = []

# From these poses we can caluclate the coordinate transform for both pallets:

source_coords = tray_balls #plugged into transform for pallet 1
source_gripper_ori = gripper_ori #plug into transform for pallet 1
dest_coords = tray_balls #plugged into transform for pallet 2
dest_gripper_ori = gripper_ori #plugged into transform for pallet 2

#initialize all the speeds and forces, this was chosen by experimentation and trading off security of grip with integrity of the ball
force_pong = 0
force_golf = 0
speed_pong = 0
speed_golf = 0


#initialize the gripper as open before starting the cycle:
robot.RunCodeCustom('rq_open_and_wait()',INSTRUCTION_CALL_PROGRAM)

#initialize robot position
robot.MoveJ(home)
robot.MoveJ(xyzrpw_2_pose([0,0,0,0,0,0])) #move robot down to position that moves well linearly to the first ball

#main for loop
for ball in range (0,5):
    #first 3 balls are golf balls, last 3 are ping pong balls, so set appropraite grip parameters
    if(ball<=2):
        robot.RunCodeCustom('rq_set_force(%i)' %force_golf,INSTRUCTION_CALL_PROGRAM)
        robot.RunCodeCustom('rq_set_speed(%i)' %speed_golf,INSTRUCTION_CALL_PROGRAM)
    else:
        robot.RunCodeCustom('rq_set_force(%i)' %force_pong,INSTRUCTION_CALL_PROGRAM)
        robot.RunCodeCustom('rq_set_speed(%i)' %speed_pong,INSTRUCTION_CALL_PROGRAM)

    #move over the ball
    robot.moveL(xzyrpw_2_pose([source_coords[ball][0],source_coords[ball][1],move_height,source_gripper_ori[0],source_gripper_ori[1],source_gripper_ori[2]])
    #descend down to pickup height
    robot.moveL(xzyrpw_2_pose([source_coords[ball][0],source_coords[ball][1],pick_height,source_gripper_ori[0],source_gripper_ori[1],source_gripper_ori[2]])
    #grab the ball
    robot.RunCodeCustom('rq_close_and_wait()',INSTRUCTION_CALL_PROGRAM)
    #check to make sure ball was grabbed before moving
    if(robot.RunCodeCustom('rq_is_object_detected()',INSTRUCTION_CALL_PROGRAM)==1):
        #pick straight up
        robot.moveL(xzyrpw_2_pose([source_coords[ball][0],source_coords[ball][1],move_height,source_gripper_ori[0],source_gripper_ori[1],source_gripper_ori[2]])
        #move to pallet 2
        robot.moveL(xzyrpw_2_pose([dest_coords[ball][0],dest_coords[ball][1],move_height,dest_gripper_ori[0],dest_gripper_ori[1],dest_gripper_ori[2]])
        #set down
        robot.moveL(xzyrpw_2_pose([dest_coords[ball][0],dest_coords[ball][1],pick_height,dest_gripper_ori[0],dest_gripper_ori[1],dest_gripper_ori[2]])
        #release the ball 
        robot.RunCodeCustom('rq_open_and_wait()',INSTRUCTION_CALL_PROGRAM)
        #ascend back to move height for next iteration
        robot.moveL(xzyrpw_2_pose([dest_coords[ball][0],dest_coords[ball][1],move_height,dest_gripper_ori[0],dest_gripper_ori[1],dest_gripper_ori[2]])

    #notify that no ball was found and end program
    else:
        print('Error, no ball detected')
        break

robot.moveJ(home)
       
        
#Task 3 Complete
