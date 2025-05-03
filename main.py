from config import ENDPOINTS
import requests
import json, os
from collections import defaultdict
from datetime import datetime

#base data has 500 supporters on 1 page, and has_more is false
def fill_supporters(supporter_donations):

    #given data has one page but this might not always be the case
    page = 1
    while True: 

        url = ENDPOINTS.get_supporters(page=page)
        response = requests.get(url)

        #check success
        if response.status_code != 200:
            print(f"Error fetching supporters: {response.status_code}")
            break

        supporters = response.json()

        #add people to list of supporters
        for supporter in supporters["data"]:
            supporter_id = supporter["id"]

            supporter_donations[supporter_id] = {
                "name": supporter.get("name", "Name?"),
                "postcode": supporter.get("postcode", "Postcode?"),
                "created_at": supporter.get("created_at"),
                "donations": [],
                "total_donated": 0
            }

        #check for more pages
        if supporters["has_more"]:
            page+=1
        else:
            break

    return supporter_donations

def get_donations(supporter_donations):

    print("Fetching donations ...", end="")
    page = 1
    while True: 
        
        print(".", end="")
        url = ENDPOINTS.get_donations(page=page)
        response = requests.get(url)

        #check success
        if response.status_code != 200:
            print(f"Error fetching donations: {response.status_code}")
            break

        donations = response.json()

        #add donations
        for donation in donations["data"]:
            supporter_id = donation["supporter_id"]

            supporter_donations[supporter_id]["donations"].append({
                "id": donation.get("id"),
                "amount": round(donation.get("amount") / 100, 2),
                "created_at": donation.get("created_at")
            })
            supporter_donations[supporter_id]["total_donated"] += round(donation.get("amount") / 100, 2)
             
        #check for more pages
        if donations["has_more"]:
            page+=1
        else:
            break

    #process one page at a time to avoid expiry
    print("Done.\n")
    return supporter_donations

def save():
    #insert into csv or json format so you can view the result
    return 0

def view_save():
    #if someone has saved then do x
    return 0

def stats(supporter_donations):
    #Total Donated
    total_donated = sum(supporter["total_donated"] for supporter in supporter_donations.values())
    print(f"\nLifetime Total Donated: £{total_donated}")

    average_donation = total_donated / len(supporter_donations)
    print(f"\nAverage Donation Amount: £{average_donation}")

    #Top 10 Supporters
    top_10_supporters = sorted(supporter_donations.items(), key=lambda x: x[1]['total_donated'], reverse=True)[:10]
    print("\nTop 10 Supporters:")
    for supporter_id, supporter in top_10_supporters:
        print(f".... {supporter['name']} : Total Donated: £{supporter['total_donated']}")

    #10 Biggest Donations
    biggest_donations = []
    for supporter in supporter_donations.values():
        for donation in supporter["donations"]:
            biggest_donations.append(donation)
    biggest_donations = sorted(biggest_donations, key=lambda x: x['amount'], reverse=True)[:10]
    print("\n10 Biggest Donations:")
    for donation in biggest_donations:
        print(f".... Donation ID: {donation['id']}, Amount: £{donation['amount']}, Date: {donation['created_at']}")

    #Smallest Donation
    smallest_donation = min(biggest_donations, key=lambda x: x['amount'])
    print(f"\nSmallest Donation: {smallest_donation['id']}, Amount: £{smallest_donation['amount']}, Date: {smallest_donation['created_at']}")

    #Oldest Supporter
    oldest_supporter = min(supporter_donations.items(), key=lambda x: x[1]['created_at'])
    print(f"\nOldest Supporter: {oldest_supporter[1]['name']} : Created At: {oldest_supporter[1]['created_at']}")

    return 0

def print_donations(supporter_donations):
    #print to terminal
    for supporter_id, supporter in supporter_donations.items():
        print(f"\n{supporter['name']} : Total Donated: £{supporter['total_donated']}")

        for donation in supporter["donations"]:
            print(f".... Donation ID: {donation['id']}, Amount: £{donation['amount']}, Date: {datetime.strptime(donation["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%d/%m/%Y %H:%M')}")

def main():
    print("--- SUPPORTER DONATIONS ---")
    while True:

        print("\nPress 1 to create a new export")
        print("Press 2 to view an existing export")
        print("Press 3 to view statistics")
        print("Press 4 to view graphs")
        print("Press 5 to exit")

        choice = input("Enter your choice: ")
        match choice:
            case "1":
                #initilaise dictionary
                supporter_donations = defaultdict(dict)
                supporter_donations = fill_supporters(supporter_donations)
                supporter_donations = get_donations(supporter_donations)

                #display donations
                print_donations(supporter_donations)

                #json dump
                with open("donation_export.json", "w") as file:
                    json.dump(supporter_donations, file, indent=4)  

            case "2":
                with open("donation_export.json", "r") as file:
                    supporter_donations = json.load(file)

                if supporter_donations:
                    print_donations(supporter_donations)
                else:
                    print("You have no existing export.")

            case "3":
                if supporter_donations:
                    stats(supporter_donations)
                else:
                    print("You have no existing export.")                       

            case "4":
                if supporter_donations:
                    print("Graphs not implemented yet.")
                else:
                    print("You have no existing export.")

            case "5":
                return 0
            
            case _:
                print("Not an option. Please try again.")
            
#--- Main -----

#check if the API is available
url = ENDPOINTS.get_supporters()
response = requests.get(url)
if response.status_code != 200:
    print(f"API Unavailable: {response.status_code}")
    exit()
else:
    main()

#statistics -----
#Liftime Total Donated 
#Average Donation Amount
#Average Donation Amount per Supporter
#Top 10 Supporters
#10 Biggest Donations
#Oldest Supporter

#Graphs -----
#Pie chart of donations
#Bar chart of donations
#Line chart of donations over time

    








