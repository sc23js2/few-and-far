from config import ENDPOINTS
import requests
from collections import defaultdict

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
                "name": supporter.get("name", "No Name"),
                "email": supporter.get("email", "No Email"),
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

    print("Fetching donations ...")
    page = 1
    while True: 
        
        print(".")
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
                "amount": donation.get("amount") / 100,
                "created_at": donation.get("created_at")
            })
            supporter_donations[supporter_id]["total_donated"] += (donation.get("amount") / 100)
             
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
        
supporter_donations = defaultdict(dict)
supporter_donations = fill_supporters(supporter_donations)
supporter_donations = get_donations(supporter_donations)

for supporter_id, supporter in supporter_donations.items():
    print(f"{supporter['name']} : Total Donated: £{supporter['total_donated']}")

    for donation in supporter["donations"]:
        print(f".... Donation ID: {donation['id']}, Amount: £{donation['amount']}, Date: {donation['created_at']}")


    








