from config import ENDPOINTS
import requests
import json, os
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

OUTPUT_DIR = "/workspaces/few-and-far/donation_output"

def fill_supporters(supporter_donations):
    """
    Fetchs supporters from the API and fill the supporter_donations dictionary with their details.
    Must be called before get_donations().
    """

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
                "created_at": supporter.get("created_at"),
                "donations": [],
                "total_donated": 0
            }

        #check for more pages
        if supporters["has_more"]:
            page+=1
        else:
            break

    print("Got supporters.")
    return supporter_donations

def get_donations(supporter_donations):
    """
    Fetches donations from the API and fills the supporter_donations dictionary with their donations.
    """
    
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

    #create graph of statistics
    graphs(supporter_donations, top_10_supporters)

    return 0

def graphs(supporter_donations, top_10_supporters):
    #Bar chart of top 10 supporters
    names = [supporter["name"] for _, supporter in top_10_supporters]
    donation_amounts = [supporter["total_donated"] for _, supporter in top_10_supporters]

    plt.figure(figsize=(20, 10))
    plt.bar(names, donation_amounts, color="royalblue")

    plt.xlabel("Supporters")
    plt.ylabel("Total Donations (£)")
    plt.title("Top 10 Supporters by Donation Amount")
    plt.xticks(rotation=75, ha="right") 
    plt.savefig(os.path.join(OUTPUT_DIR,"top_10_supporters.png"))

    # Line Chart of Cumulative donations
    all_donations = []
    for supporter in supporter_donations.values():
        for donation in supporter["donations"]:
            all_donations.append(donation)

    all_donations.sort(key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"))
    amounts = []
    sum = 0
    dates = []

    for donation in all_donations:
        sum += donation["amount"]
        amounts.append(sum)
        dates.append(datetime.strptime(donation["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"))

    plt.figure(figsize=(20, 10))
    plt.plot(dates, amounts, marker="o", linestyle="-", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Total Donations Receivef (£)")
    plt.title("Cumulative Donation Amount Over Time")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.savefig(os.path.join(OUTPUT_DIR, "all_donations.png"))

    # Pie chart of donations per supporter
    plt.figure(figsize=(10, 10))
    plt.pie(donation_amounts, labels=names, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.title("Donations per Supporter")
    plt.savefig(os.path.join(OUTPUT_DIR,"supporter_donations.png"))


def print_donations(supporter_donations):
    #print to terminal
    for supporter_id, supporter in supporter_donations.items():
        print(f"\n{supporter['name']} : Total Donated: £{supporter['total_donated']}")

        for donation in supporter["donations"]:
            print(f".... Donation ID: {donation['id']}, Amount: £{donation['amount']}, Date: {datetime.strptime(donation["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%d/%m/%Y %H:%M')}")


def main():
    """
    Menu to navigate application
    """
    supporter_donations = defaultdict(dict)

    print("--- SUPPORTER DONATIONS ---")
    while True:

        print("\nPress 1 to create a new export")
        print("Press 2 to view an existing export")
        print("Press 3 to view statistics")
        print("Press 0 to exit")

        choice = input("Enter your choice: ")
        match choice:
            case "1":
                #initilaise dictionary
                supporter_donations = fill_supporters(supporter_donations)
                supporter_donations = get_donations(supporter_donations)

                #display donations
                print_donations(supporter_donations)

                #json dump
                with open("donation_output/donation_export.json", "w") as file:
                    json.dump(supporter_donations, file, indent=4)  

            case "2":
                with open("donation_output/donation_export.json", "r") as file:
                    supporter_donations = json.load(file)

                if supporter_donations is not None:
                    print_donations(supporter_donations)
                else:
                    print("You have no existing export.")

            case "3":
                if supporter_donations is not None:
                    stats(supporter_donations)
                    print("\nGraphs have been generated and saved to the output directory /donation_output")
                else:
                    print("You have no existing export.")                       

            case "0":
                return 0
            
            case _:
                print("Not an option. Please try again.")
            
#--- Main -----
if __name__ == "__main__":
    #check if the API is available
    url = ENDPOINTS.get_supporters()
    response = requests.get(url)
    if response.status_code != 200:
        print(f"API Unavailable: {response.status_code}")
        exit()
    else:
        main()

    








