import requests
import serial
def light_finder(name):
    API_KEY = "sk-mz046872686c4f29011396"
    url = f"https://perenual.com/api/v2/species-list?key={API_KEY}&q={name}"
    response = requests.get(url).json()
    if not response.get("data"):
        print("plant not found")
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
    
    for condition, range in light_ranges.items():
        if condition in light:
            print(f"{name}: {condition} - boundaries: {range[0]},{range[1]}")
            return range
    print("Light not specified, using default 400-600")
    return (400, 600)
Name = input("enter plant name: ")
light_finder(Name)