import paho.mqtt.client as mqtt  
import time  
import random  
import json  
import threading  
from datetime import datetime  
  
# Define the MQTT broker details  
broker = "34.168.60.218"  # Replace with your broker's IP address  
port = 1883  # Use 1883 for non-TLS connections  
  
# Define 50 unique locations (fictional rice field villages in Indonesia)  
locations = [  
    "lamongan", "bojonegoro", "jember", "probolinggo", "tuban",  
    "nganjuk", "kediri", "blitar", "malang", "pasuruan",  
    "sidoarjo", "mojokerto", "surabaya", "bangkalan", "pamekasan",  
    "sampang", "sumenep", "lumajang", "banyuwangi", "situbondo",  
    "bondowoso", "jember", "tulungagung", "trenggalek", "ngawi",  
    "magetan", "karanganyar", "wonogiri", "klaten", "sukoharjo",  
    "boyolali", "salatiga", "semarang", "kendal", "batang",  
    "tegal", "brebes", "cirebon", "indramayu", "majalengka",  
    "sumedang", "purwakarta", "karawang", "bekasi", "bogor",  
    "depok", "jakarta", "tangerang", "banten", "cilegon"  
]  
  
# Function to generate random data  
def generate_random_data(category):  
    if category == "soil_monitoring":  
        data = {  
            "timestamp": datetime.now().isoformat(),  # Add timestamp  
            "soil_moisture_levels": round(random.uniform(0, 100), 2),  
            "nutrient_levels": {  
                "N": round(random.uniform(0, 200), 2),  
                "P": round(random.uniform(0, 200), 2),  
                "K": round(random.uniform(0, 200), 2)  
            },  
            "soil_ph_levels": round(random.uniform(4.0, 8.0), 2),  
            "soil_temperature": round(random.uniform(0, 40), 2) 
        }  
        return data  
    elif category == "weather_data":  
        data = {  
            "timestamp": datetime.now().isoformat(),  # Add timestamp  
            "air_temperature": round(random.uniform(-10, 40), 2),  
            "humidity": round(random.uniform(0, 100), 2),  
            "rainfall_amount": round(random.uniform(0, 200), 2),  
            "wind_speed": round(random.uniform(0, 20), 2),  
            "wind_direction": random.randint(0, 360),  
            "solar_radiation": round(random.uniform(0, 1000), 2)
        }  
        return data  
    elif category == "water_management":  
        data = {  
            "timestamp": datetime.now().isoformat(),  # Add timestamp  
            "water_levels_in_irrigation_canals": round(random.uniform(0, 5), 2),  
            "water_quality": {  
                "pH": round(random.uniform(0, 14), 2),  
                "salinity": round(random.uniform(0, 35), 2),  
                "contaminants": round(random.uniform(0, 100), 2)  
            }  
        }  
        return data  
  
# Callback when the client connects to the broker  
def on_connect(client, userdata, flags, rc):  
    print(f"Client {userdata} connected with result code {rc}")  
  
# Function to create and run an MQTT client for a specific location and ID  
def run_client(location, client_id):  
    client = mqtt.Client(userdata=client_id)  
    client.on_connect = on_connect  
  
    # Connect to the broker  
    client.connect(broker, port, 60)  
    client.loop_start()  # Start the loop to process network traffic  
  
    # Publish messages for different categories continuously  
    categories = ["soil_monitoring", "weather_data", "water_management"]  
    try:  
        while True:  # Infinite loop  
            for category in categories:  
                data = generate_random_data(category)  
                topic = f"{location}/{client_id}/{category}/data"  
                message = json.dumps(data, indent=2)  # Convert data to JSON format  
                client.publish(topic, message)  
                # Print only the timestamp and the topic  
                print(f"{data['timestamp']} - {topic}")  
                time.sleep(1)  # Wait for 1 second between publishes  
    except KeyboardInterrupt:  
        print(f"Client {client_id} interrupted and will stop publishing.")  
    finally:  
        client.loop_stop()  # Stop the loop  
        client.disconnect()  # Disconnect from the broker  
        print(f"Client {client_id} has finished publishing.")  
  
# Create and start multiple client threads for each location  
threads = []  
for i in range(50):  
    location = locations[i]  
    client_id = random.randint(1,10)  # Unique client ID starting from 1  
    thread = threading.Thread(target=run_client, args=(location, client_id))  
    threads.append(thread)  
    thread.start()  
  
# Wait for all threads to complete (they won't unless interrupted)  
for thread in threads:  
    thread.join()  
  
print("All clients have finished publishing.")  
