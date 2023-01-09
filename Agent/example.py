from agent import Agent
from time import sleep

def main():
    agent = Agent()

    # let robot say something
    agent.say('Hi, welcome to the tutorial!')
    sleep(2.0)

    # move robot arm to certain position, with certain velocity (a factor from 0 to 1)
    # the list is in the order of ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "HipRoll"]
    agent.say('I am going to move my arm')
    joint_values = [0.0843689441681,-0.285320520401, 1.18883514404,
                    0.99401974678, 0.147222042084, 0.231631040573]
    vel = 0.5
    agent.take_action(action=joint_values, vel=vel) # this is a non-blocking call
    sleep(3.0) # wait for the robot finishing moving

    # get robot right-hand pose (x, y, z, wx, wy, wz) in the robot base frame
    hand_pose = agent.get_hand_pose()
    print(hand_pose)

    # move robot to home pose
    agent.go_home_pose(blocking=False)
    agent.say("I am going to the home pose while speaking")
    sleep(2.0)

    # collect robot whole-body joint values kinesthetically
    agent.say('Okay, Lets collect some data')
    sleep(1.0)
    agent.say('Ready?')
    sleep(1.0)
    agent.say('Start!')
    agent.set_stiffness(0.0) # set loose the joint stiffness
    total_time_steps = 10
    traj = []
    for step in range(total_time_steps):
        # joint values are in the order of ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "HipRoll"]
        whole_body_joint_values = agent.collect_robot_data_whole_body()
        traj.append(whole_body_joint_values)
        print("[Step {}]: Collected data {}".format(step + 1, whole_body_joint_values))

        sleep(0.5)

    agent.set_stiffness(1.0) # fix the joints so that it will not be able to be moved freely
    agent.say('Great! Data were successfully collected')
    sleep(2.0)

    # move robot to home pose
    agent.go_home_pose(blocking=True)
    agent.say("I am speaking after I finished going home pose")
    sleep(2.0)

    agent.say("That's it for the tutorial! Have fun with the course!")
    agent.stop()

if __name__ == '__main__':
    main()

