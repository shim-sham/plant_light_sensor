import requests
import serial
import time
def light_finder(name):
    API_KEY = "sk-mz046872686c4f29011396"
    url = f"https://perenual.com/api/v2/species-list?key={API_KEY}&q={name}"
    response = requests.get(url).json()
    if not response.get("data"):
        print("plant not found, using default range (200,600)")
        return (200, 600)
    
    plant = response["data"][0]
    id = plant["id"]
    x= f"https://perenual.com/api/v2/species/details/{id}?key={API_KEY}"
    print(x)
    plant_details = requests.get(x)
    if plant_details.status_code == 200:
        plant_details = plant_details.json()
        light = plant_details.get("sunlight",[])
        print(light)
    else:
        print("error getting the request back")
        print(plant_details.status_code)
        return(400,600)

    light_ranges = {
        "full shade": (50, 200),
        "part shade": (200, 400),
        "part sun/part shade": (400, 600),
        "full sun": (600, 1000)
    }
    
    for condition, (min_val, max_val) in light_ranges.items():
        if condition in light:
            print(f"{name}: {condition} ({min_val}-{max_val} lux)")
            return (min_val, max_val)
    print("Light not specified, using default 400-600")
    return (400, 600)
if __name__ == "__main__":
    plant_name = input("Enter plant name: ")
    min_light, max_light = light_finder(plant_name)
    
    try:
        arduino = serial.Serial('/dev/cu.usbserial-0001', 9600, timeout=1)
        time.sleep(2) 
        arduino.write(f"{min_light},{max_light}\n".encode())
        print(f"Sent to Arduino: {min_light}-{max_light} lux")
        arduino.close()
    except Exception as e:
        print(f"Serial error: {e}. Check port name and connections.")