import numpy as np
from random import randint
import time

def snap_rover_state(Rover):
    #check for last state since Rover updated
    Rover.snap = (Rover.pos[0], Rover.pos[1], Rover.yaw, time.time())
    print("snap_rover_state -> Rover.snap: {}".format(Rover.snap))

    return Rover

def update_recorded_movement(Rover):
  # Check if we've sufficiently moved, if we did, update latest recorded position

  if Rover.pos[0] and Rover.pos[1] and Rover.yaw:
    cond1 = np.absolute(Rover.snap[0] - Rover.pos[0]) > 2
    cond2 = np.absolute(Rover.snap[1] - Rover.pos[1]) > 2
    cond3 = np.absolute(Rover.snap[2] - Rover.yaw) % 360 > 2
    Rover.sufficient_movement = cond1 or cond2 or cond3

  if Rover.sufficient_movement:
    print("Rover moved: Update snap positions")
    Rover.snap = (Rover.pos[0], Rover.pos[1], Rover.yaw, Rover.total_time)
    Rover.sufficient_movement = False

  return Rover


def check_if_stuck(Rover):

  stuck_cond1 =  Rover.vel == 0 and np.absolute(Rover.throttle) > 0
  stuck_cond2 = Rover.total_time - Rover.snap[3] > 2 and not Rover.sufficient_movement
  is_stuck = (stuck_cond1 or stuck_cond2) and not Rover.near_sample

  return is_stuck


# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):

    #GC not following left wall, why??
        #yes it did but need more change
    #GC deviate mean angel by 5 degrees
    # 5 able to pass minimal requirement
    #10 is not a bad value
    #11 is ok as able to come near to wall and pick up rock, but sacrifice on fidelity when it comes too close to wall
    #12.5 will hit wall maybe too close

    #after adding "limit_range" routine, can come closer to wall without sacrificing too much on fidelity
    near_wall = 15

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with

    if Rover.nav_angles is not None:
        # rover_mean_angle = np.mean(Rover.nav_angles * 180/np.pi)
        # rover_std_dev = np.std(Rover.nav_angles)

        Rover = snap_rover_state(Rover)

        # Check for Rover.mode status
        if Rover.mode == 'forward':
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + near_wall, -15, 15)
                # Rover.steer = np.mean(Rover.nav_angles * 180/np.pi)+ 0.2*rover_std_dev
                # print("Rover.mode: {}, Rover.steer: {}, rover_mean_angle: {}".format(Rover.mode, Rover.steer, rover_mean_angle))
                # print("Rover.mode: {}, Rover.steer: {}, rover_mean_angle: {}, 0.2*rover_std_dev: {}".format(Rover.mode, Rover.steer, rover_mean_angle, 0.2*rover_std_dev))
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
            #GC
            #While moving, if found rock then stop and pick it up
            #If near a sample, then stop Rover so that it can pick up rock
            if Rover.near_sample == 1:
                print("Near sample and going to pick up sample")
                # Set mode to "stop" and hit the brakes!
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'stop'
                # if Rover.vel == 0:
                #     Rover.picking_up = True
                # return Rover
            #GC in place of check_if_stuck
            # print("Rover.snap: {}; Rover.near_sample: {}".format(Rover.snap, Rover.near_sample))
            # print("Rover.pos: {}; Rover.yaw: {}; time: {}".format(Rover.pos, Rover.yaw, time.time()))
            # if (np.absolute(Rover.snap[0] - Rover.pos[0]) < 2) and \
            #    (np.absolute(Rover.snap[1] - Rover.pos[1]) <2) and \
            #    (np.absolute(Rover.snap[2] - Rover.yaw)%360 < 2) and \
            # #    (Rover.snap[3] - time.time() > 10) and \
            #    (Rover.near_sample != 1):
            #    Rover.mode = 'stuck'
            if check_if_stuck(Rover):
                print("Rover stuck!")
                Rover.mode = 'stuck'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    #GC do same here
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + near_wall, -15, 15)
                    # Rover.steer = np.mean(Rover.nav_angles * 180/np.pi)+ 0.2*rover_std_dev
                    # print("Rover.mode: {}, Rover.steer: {}, rover_mean_angle: {}, 0.2*rover_std_dev: {}".format(Rover.mode, Rover.steer, rover_mean_angle, 0.2*rover_std_dev))
                    Rover.mode = 'forward'
        elif Rover.mode == 'stuck':
            steer = randint(-15,15)  #if in stuck stake, turn randomly hoping to get out of it
            Rover.brake, Rover.throttle, Rover.steer, Rover.mode = 0, 0, steer, 'forward'

    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0



    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True



    return Rover
