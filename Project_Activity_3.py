import urllib.parse
import requests
from tabulate import tabulate
from colorama import init, Fore, Back, Style
from termcolor import colored


main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "wU6GmujkIUcBEXlWP6KpF64chWWxSxjc"

while True:
     print(colored("MAPQUEST API", 'cyan'))
     
     orig = input(colored("Starting Location: ", 'magenta'))
     if orig == "quit" or orig == "q":
          break
     dest = input(colored("Destination: ", 'magenta'))
     if dest == "quit" or dest == "q":
          break
     measurement = input(colored("Choose measurement (km) or (miles): ", 'magenta'))
     if measurement == "quit" or measurement == "q":
          break
     roundtrip = input(colored("Roundtrip? (yes) or (no): ", 'magenta'))
     if roundtrip == "quit" or roundtrip == "q":
          break
          
     url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
     print(colored("URL: " + (url), 'blue', 'on_yellow'))
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
          print(colored("API Status: " + str(json_status) + " = A successful route call.\n", 'green'))
          print(colored(tabulate(table) + "\n", 'red', 'on_cyan'))
          for each in json_data["route"]["legs"][0]["maneuvers"]:
               print(colored((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"), 'yellow'))
               print("====================")
     elif json_status == 402:
          print("**********************************************")
          print(colored("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.", 'on_red'))
          print("**********************************************\n")
     elif json_status == 611:
          print("**********************************************")
          print(colored("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.", 'on_red'))
          print("**********************************************\n")
     else:
          print("********************************************************************")
          print("For Staus Code: " + str(json_status) + "; Refer to:")
          print(colored("https://developer.mapquest.com/documentation/directions-api/status-codes", 'on_red'))
          print("********************************************************************\n")
