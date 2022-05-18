# Afarm Drone

It based on Tello Python api : https://github.com/damiafuentes/DJITelloPy

If you want to use drone to fly real, just refer to tello api code

GUI is based on PyQT5

If you want to look ui closely, Use 'Qt Designer' desktop app.

## Install & Run
- Qt Designer : https://build-system.fman.io/qt-designer-download 
```bash
# Install
pip install -r requirements.txt

# Run
python3 main.py
```
## Architecture

![Architecture](https://user-images.githubusercontent.com/79500842/169015425-b1350af8-9f8b-49a8-9069-85909a30088f.png)


## UI
### LoginWindow.py
- When login finished, Get flight info from database and Store in flight_info folder
<img src="https://user-images.githubusercontent.com/79500842/168304960-1de15774-bdc4-4089-8030-8fed0276ed3e.png" width="300" height="300" alt="login">

### SendVideoWindow.py
- Tello have to connect PC and tello by UDP
- If you want to fly tello, Disconnect internet then connect to tello
- In wireless network (Wi-Fi) setting, you can see tello bla bla. Just click it
- It will draw the path by python turtle module. After turtle move, Close the turtle window then tello will fly
- Video will save after flight. Therefore If the flight failed, video will be cracked
<img src="https://user-images.githubusercontent.com/79500842/168304954-459d495e-9f2c-42f6-992b-cb799c3de589.png" width="300" height="300" alt="fly">

- Select tello then select video.
- Video is located in /drone/{drone_name}/, file name is date of flight
<img src="https://user-images.githubusercontent.com/79500842/168304962-49cbe870-c71a-41d0-91ea-e75e41bdc6f7.png" width="300" height="300" alt="send video">

## Directory
```
├── flight
│   ├── // files to fly tello
├── flight_info // save 'flight info json file' and 'mp4 video' of each drone
│   ├── tello1
│   └── tello2
├── resource // logo & background image
└── ui // .ui file for PyQT5
└── LoginWindow.py
└── SendVideoWindow.py
└── main.py 
```

## Example of Flight Info JSON 
```json
{
  "flight": {"init_x": 1, "init_y": 1, "width": 100, "height": 70, "interval": 10, "sight_range": 1, "grape_height": 100}, 
  "id": 3, 
  "zone": 1, 
  "product_name": "tello2", 
  "start_time": "2022-03-19T13:30:00"
}
```
