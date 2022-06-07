from ast import arg
from turtle import setheading
from global_tello import Ref
from djitellopy import tello
import time
import cv2
import argparse
from threading import Thread
from datetime import datetime


keepRecording = True

def Video_Capture(drone_name):
    frame_read = Ref.myTello.get_frame_read()
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('./drone/'+drone_name+'/'+ datetime.strftime(datetime.now(),"%Y-%m-%d-%H-%M-%S.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))
   
    print('../drone/'+drone_name+ datetime.strftime(datetime.now(),"%Y-%m-%d-%H-%M-%S.mp4"))
    while keepRecording:
        video.write(frame_read.frame)
        # print('../drone/'+drone_name+ datetime.strftime(datetime.now(),"%Y-%m-%d-%H-%M-%S.mp4"))
        time.sleep(1 / 10)
    
    video.release()

def create_path(width, height, interval):
      path = []  # [x축 변위, y축 변위, 시간(사용하지 않음)]
      for i in range(0, height, interval):
          if((i//interval) % 2 == 0): 
              path.append([width, 0, 0.03*width]) # 오른쪽
          else:
              path.append([-width, 0, 0.03*width]) # 왼쪽
          path.append([0, 2*interval, 0.03*interval]) # 앞쪽
      return path


def fly_drone(tello, path, droneId):
    time.sleep(3)
    for d_data in path:
        if d_data[0]:
            if d_data[0]>0:
                tello.move("right",d_data[0])
            elif d_data[0]<0:
                tello.move("left",-d_data[0])
        else:
            tello.move("forward",d_data[1])

def draw_simulation(path):
    import turtle as t
    t.pendown()
    t.setheading(90)
    for d_data in path:
        # print(d_data)
        x,y=t.pos()
        t.goto(x+d_data[0],y+d_data[1])
    t.done()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--interval', type=int)
    parser.add_argument('--drone_id', type=int)
    parser.add_argument('--drone_name', type=str)
    args = parser.parse_args()

    path = create_path(args.width, args.height, args.interval)
    # draw_simulation(path)
    Ref.myTello = tello.Tello()
    Ref.myTello.connect()
    print(Ref.myTello.get_battery())
    Ref.myTello.streamon()
    Ref.myTello.takeoff()
    Ref.myTello.set_speed(15)
    
    # Tello Video Capture feature have to run in background
    # Therefore I use "Thread()" and store tello object in another class variable
    # Now I can access tello object anywhere with Ref class
    recorder = Thread(target=Video_Capture,args=[args.drone_name])
    Ref.recorder = recorder
    recorder.start()

    fly_drone(Ref.myTello, path, args.drone_id)
    
    keepRecording=False
    # Ref.myTello.send_rc_control(0,0,0,0)
    Ref.myTello.streamoff()
    Ref.myTello.land()
    recorder.join()
    del Ref.myTello
