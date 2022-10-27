import urllib.parse
import requests
from tabulate import tabulate

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "wU6GmujkIUcBEXlWP6KpF64chWWxSxjc"

while True:
     print("\nWelcome to MAPQUEST API!")
     
     orig = input("\nStarting Location: ")
     if orig == "quit" or orig == "q":
          break
     dest = input("Destination: ")
     if dest == "quit" or dest == "q":
          break
     measurement = input("Choose measurement (km) or (miles): ")
     if measurement == "quit" or measurement == "q":
          break
     roundtrip = input("Roundtrip? (yes) or (no): ")
     if roundtrip == "quit" or roundtrip == "q":
          break
          
     url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
     print("URL: " + (url))
     json_data = requests.get(url).json()
     json_status = json_data["info"]["statuscode"]
     trip = (json_data["route"]["formattedTime"])
     
     kilometers = str("{:.2f}".format((json_data["route"]["distance"])*1.61))
     miles = str("{:.2f}".format((json_data["route"]["distance"])))
     
     rountrip_km = float(kilometers)*2
     rountrip_miles = float(miles)*2
     
     if roundtrip == "yes" and measurement == "km":
          table = [['Origin', 'Destination', 'Trip Duration', 'Distance', 'Roundtrip Distance'], [orig, dest, trip, kilometers + " km", str(rountrip_km) + " km"]]
     elif roundtrip == "yes" and measurement == "miles":
          table = [['Origin', 'Destination', 'Trip Duration', 'Distance', 'Roundtrip Distance'], [orig, dest, trip, miles + " miles", str(rountrip_miles) + " miles"]]
     elif roundtrip == "no" and measurement == "km":
          table = [['Origin', 'Destination', 'Trip Duration', 'Distance',], [orig, dest, trip, kilometers + " km"]]
     else:
          table = [['Origin', 'Destination', 'Trip Duration', 'Distance',], [orig, dest, trip, miles + " miles"]]
     
     if json_status == 0:
          print("API Status: " + str(json_status) + " = A successful route call.\n")
          print(tabulate(table) + "\n")
          for each in json_data["route"]["legs"][0]["maneuvers"]:
               print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
               print("=============================================")
     elif json_status == 402:
          print("**********************************************")
          print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
          print("**********************************************\n")
     elif json_status == 611:
          print("**********************************************")
          print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
          print("**********************************************\n")
     else:
          print("************************************************************************")
          print("For Staus Code: " + str(json_status) + "; Refer to:")
          print("https://developer.mapquest.com/documentation/directions-api/status-codes")
          print("************************************************************************\n")