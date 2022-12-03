# THIS CODE WILL ONLY WORK UNDER THE FOLLOWING ASSUMPTIONS:
# - you have installed boto3 and tested it according to the lecture training document
# - you configured your AWS CLI with your IAM access key and secret.
# - you created a table called "gifts".
# - you added at least one Item to the gifts table
# - any Items that you request to view in the code have a attribute called "gifts".

import boto3
import sys
import datetime
from botocore.config import Config
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb', config=Config(region_name="us-west-2"))
table = dynamodb.Table('Find_Potty')
print(table.creation_date_time)

while 1:
    print("Enter a number\n1) Show all gifts\n2) Add a new gift")


    select = input()

    if select == "1":

# WARNING: .scan() finds every item in a table, which is an expensive operation
# on a KV database. If you frequently need to find all rows in a table, then a KV
# database might not be the correct storage service for you.
        all_gifts = table.scan()

        all_occasions = set(i['PottyUser'] for i in all_gifts["Items"])
        print("Occasion names: ")
        for o in all_occasions:
            print("\t" + o)


        event_name = input("Enter the name of an occasion: ")
        all_for_event = table.query(KeyConditionExpression=Key("PottyUser").eq(event_name))
        all_givers = set(i["RestroomName"] for i in all_for_event["Items"])
        if len(all_givers) > 0:
            print("Giver names:")
            for g in all_givers:
                print("\t" + g)

            giver = input("Enter the name of a giver:")
            gift = table.get_item(Key={"PottyUser": event_name, "RestroomName": giver})
            if "Item" in gift:
                print(gift["Item"]["gift"])
                exit(0)
            else:
                print("No giver with that name.")
        else:
            print("No occasion with that name.")

    elif select == "2":
        all_gifts = table.scan()
        all_givers = set(i['RestroomName'] for i in all_gifts["Items"])
        giver_list = []
        print("Giver names: ")
        for i in all_givers:
            print("\t" + i)
            giver_list.append(i)
        giver_name = input("Enter the name of the Giver: \t")
        gift_name = input("Enter the name of the gift: \t")
        eventino = input ("Enter the event name: \t")
        table.put_item(Item={"PottyUser" : eventino, "RestroomName" : giver_name, "gift" : gift_name, "date" :  datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        
    else:
        print("not a valid selection")
