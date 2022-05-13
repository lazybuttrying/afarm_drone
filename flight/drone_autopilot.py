import numpy as np
from djitellopy import tello
import datetime
import flight.request_func as request_func

# tello control
tello = tello.Tello()
tello.connect()
print(tello.get_battery())

tello.takeoff() # 이륙
tello.land()    # 착륙


'''
tello.send_rc_control(left_right_velocity (- is left), 
                      forward_backward_velocity (- is back), 
                      up_down_velocity (- is down)
                      yaw_velocity (clockwise))

number is speed 
'''

# algorithm
def cpp_algo_turn(width, grape_height, height, interval, sight_range, init_point, speed):
  print("Do Coverage Path Planning algorithm")

  # parameters
  width, grape_height, height, interval = width, grape_height, height, interval
  sight_range = sight_range
  speed = speed
  init_x = init_point[0]
  init_y = init_point[1] - sight_range

  # how to go to the initial point???

  # traj[0] = move only right side
  # trak[2] = turen left or right
  # traj[3] = x coordinate
  # traj[4] = y coordinate

  idx = 0
  traj = np.zeros((1, 5))
  traj[idx][3] = init_x
  traj[idx][4] = init_y

  count_y = 0
  max_y_range = 2 * sight_range + grape_height
  interval_y_range = interval - 2 * sight_range
  flag = -1

  while 1:
    if ((traj[idx][4] >= (height + 2 * sight_range + init_y)) & (traj[idx][3] >= init_x)):
      break

    if (traj[idx][3] == init_x):
      if (count_y == 0):
        traj = np.append(traj, np.array([[speed, 0, 0, traj[idx][3] + speed, traj[idx][4]]]), axis=0)
        # traj[idx+1][3] = traj[idx][3] + speed ##
        # traj[idx+1][4] = traj[idx][4] ##
        # traj[idx + 1][0] = speed
        # traj[idx + 1][1] = 0
        # traj[idx + 1][2] = 0
      elif (count_y > 0):
        traj = np.append(traj, np.array([[speed, 0, 0, traj[idx][3], traj[idx][4] + speed]]), axis=0)
        # traj[idx+1][3] = traj[idx][3] ##
        # traj[idx+1][4] = traj[idx][4] + speed ##
        # traj[idx+1][0] = speed
        # traj[idx+1][1] = 0
        # traj[idx+1][2] = 0
        count_y = count_y + speed
        if flag == 1:
          traj[idx + 1][2] = 90
          flag = -1
        if (count_y >= max_y_range + interval_y_range):
          count_y = 0
          traj[idx + 1][2] = 90

    elif (traj[idx][3] == init_x + width + sight_range):
      if ((count_y >= 0) & (count_y < max_y_range)):
        traj = np.append(traj, np.array([[speed, 0, 0, traj[idx][3], traj[idx][4] + speed]]), axis=0)
        # traj[idx+1][3] = traj[idx][3] ##
        # traj[idx+1][4] = traj[idx][4] + speed ##
        # traj[idx + 1][0] = speed
        # traj[idx + 1][1] = 0
        # traj[idx + 1][2] = 0
        count_y = count_y + speed
        if (count_y == 0):
          traj[idx + 1][2] = -90

      elif (count_y >= max_y_range):
        flag = 1
        traj = np.append(traj, np.array([[speed, 0, -90, traj[idx][3] - speed, traj[idx][4]]]), axis=0)
        # traj[idx+1][3] = traj[idx][3] - speed ##
        # traj[idx+1][4] = traj[idx][4] ##
        # traj[idx+1][0] = speed
        # traj[idx+1][1] = 0
        # traj[idx+1][2] = -90

    else:
      if (count_y == 0):
        traj = np.append(traj, np.array([[speed, 0, 0, traj[idx][3] + speed, traj[idx][4]]]), axis=0)
        # traj[idx+1][3] = traj[idx][3] + speed ##
        # traj[idx+1][4] = traj[idx][4] ##
        # traj[idx+1][0] = speed
        # traj[idx+1][1] = 0
        # traj[idx+1][2] = 0
      elif (count_y >= max_y_range):
        traj = np.append(traj, np.array([[speed, 0, 0, traj[idx][3] - speed, traj[idx][4]]]), axis=0)
        # traj[idx+1][3] = traj[idx][3] - speed ##
        # traj[idx+1][4] = traj[idx][4] ##
        # traj[idx+1][0] = speed
        # traj[idx+1][1] = 0
        # traj[idx+1][2] = 0

    idx = idx + 1
    print('[' + str(idx) + ']: x:' + str(traj[idx][3]) + ' y:' + str(traj[idx][4]))

  return traj

def cpp_algo(self, width, grape_height, height, interval, sight_range, init_point, speed):
  print("Do Coverage Path Planning algorithm")

  # parameters
  self.width, self.grape_height, self.height, self.interval = width, grape_height, height, interval
  self.sight_range = sight_range
  self.speed = speed
  init_x = init_point(1)
  init_y = init_point(2) - sight_range

  # how to go to the initial point???
  '''
    traj[0] = move right or left side
    traj[1] = move forward or backward
    traj[3] = x coordinate
    traj[4] = y coordinate
  '''

  idx = 0
  traj = [][5]
  traj[idx][3] = self.init_x
  traj[idx][4] = self.init_y ##append

  count_y = 0
  max_y_range = 2 * sight_range + grape_height
  interval_y_range = interval - 2 * sight_range

  while 1:
    if ((traj[idx][1] == height + 2 * sight_range + init_y) & (traj[idx][0] == init_x)):
      break

    if (traj[idx][3] == init_x):
      if (count_y == 0):
        traj[idx + 1][3] = traj[idx][3] + speed  ##
        traj[idx + 1][4] = traj[idx][4]  ##

        traj[idx + 1][0] = speed
        traj[idx + 1][1] = 0
        traj[idx+1][2] = 0
      elif (count_y > 0):
        traj[idx + 1][3] = traj[idx][3]  ##
        traj[idx + 1][4] = traj[idx][4] + speed  ##

        traj[idx + 1][0] = 0
        traj[idx + 1][1] = speed
        traj[idx + 1][2] = 0
        count_y = count_y + speed
        if (count_y >= max_y_range + interval_y_range):
          count_y = 0

    elif (traj[idx][3] == init_x + width + sight_range):
      if ((count_y >= 0) & (count_y < max_y_range)):
        traj[idx + 1][3] = traj[idx][3]  ##
        traj[idx + 1][4] = traj[idx][4] + speed  ##

        traj[idx + 1][0] = 0
        traj[idx + 1][1] = speed
        traj[idx + 1][2] = 0
        count_y = count_y + speed
      elif (count_y >= max_y_range):
        traj[idx + 1][3] = traj[idx][3] - speed  ##
        traj[idx + 1][4] = traj[idx][4]  ##

        traj[idx + 1][0] = -speed
        traj[idx + 1][1] = 0
        traj[idx + 1][2] = 0

    else:
      if (count_y == 0):
        traj[idx + 1][3] = traj[idx][3] + speed  ##
        traj[idx + 1][4] = traj[idx][4]  ##

        traj[idx + 1][0] = speed
        traj[idx + 1][1] = 0
        traj[idx + 1][2] = 0
      elif (count_y >= max_y_range):
        traj[idx + 1][3] = traj[idx][3] - speed  ##
        traj[idx + 1][4] = traj[idx][4]  ##

        traj[idx + 1][0] = -speed
        traj[idx + 1][1] = 0
        traj[idx + 1][2] = 0

    idx = idx + 1

  return traj


def fly_drone(traj_list, charge_x, charge_y, index, drone_id):
  # global index ##
  traj = traj_list
  '''
  tello.connect()  # UDP 소켓 열어서 하는 방법도 고안해야..
  tello.takeoff()
  tello.send_rc_control(0, 0, 0, 100, 0)  # z = 1m
  tello.streamon()
  '''
  # go to last location
  # basically, last location is initial point
  # index = last_traj_idx

  if index != 0:
    dist_x = traj[index][3] - charge_x
    dist_y = traj[index][4] - charge_y
    tello.send_rc_control(dist_x, dist_y, 0, 0)

  last_req = 0
  for i in range(index, len(traj)):
    print("fly idx:", i)

    if (tello.get_battery() < 10):
      # 마지막 위치 저장 후
      index = i
      # index = last_traj_idx
      # 충전하러 감
      dist_x = charge_x - traj[i][3]
      dist_y = charge_y - traj[i][4]
      tello.send_rc_control(dist_x, dist_y, 0, 0)
      flag = -1
      return flag  # or break

    else:
      tello.send_rc_control(traj[i][0], traj[i][1], 0, traj[i][2])
      request_func.load_img()
      # or clockwise로 처리하는 방법

    now = datetime.datetime.now()
    if (now - last_req) > 1000:
      is_fly, start_time, end_time = request_func.req_droneControl(drone_id)
      last_req = datetime.datetime.now()
      if (last_req > end_time):
        break


  # 충전하러 감
  dist_x = charge_x - traj[i][3]
  dist_y = charge_y - traj[i][4]
  # tello.send_rc_control(dist_x, dist_y, 0, 0)
  flag = 0
  index = 0
  return flag
