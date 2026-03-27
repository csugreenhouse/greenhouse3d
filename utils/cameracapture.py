import cv2
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
import time

def get_image_from_camera_parameter(camera_parameters):
    camera_ip = camera_parameters["ip_address"]
    camera_id = camera_parameters["camera_id"]
    camera_url = f"http://{camera_ip}/capture"
    try:
        response = requests.get(camera_url,timeout=10)
        response.raise_for_status()
        image = response.content
        return cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Camera {camera_id}'s ip {camera_url} failed")
        return None
    
def get_images_from_list_of_camera_parameters(camera_parameter_list):
    images = []
    for camera_parameter in camera_parameter_list:
        images.append(get_image_from_camera_parameter(camera_parameter))
    return images

def time_stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def save_image_to_server_directory(camera_id, image):
    save_path = f'testfiles/{time_stamp()}.jpg'
    cv2.imwrite(save_path, image)
    return save_path

default_cam_params = {
    "camera_id": 1,
    "ip_address": "192.168.0.11",
    "width": 1024,
    "height": 768,
    "focal_length_mm": 3.6,
    "sensor_height_mm": 2.2684,
    "sensor_width_mm": 3.590
}

def start_multi_capture(intervalseconds = .1, iterations = 10):
    for iteration in range(iterations):
        try:
            print(f"Capturing {iteration + 1}/{iterations}...")
            img = get_image_from_camera_parameter(default_cam_params)
            
            if img is not None:
                save_path = save_image_to_server_directory(default_cam_params["camera_id"], img)
                print(f"Saved: {save_path}")
            
        except Exception as e:
            print(f"Camera busy or timed out. ({e})")
            
        time.sleep(intervalseconds)

def single_capture():
    print(f"Capturing Single Image...")
    img = get_image_from_camera_parameter(default_cam_params)
            
    if img is not None:
        save_path = save_image_to_server_directory(default_cam_params["camera_id"], img)
        print(f"Saved: {save_path}")


'''#for testing captures:
def main():
    #start_multi_capture()
    single_capture()

main()'''
