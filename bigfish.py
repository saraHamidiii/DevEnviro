

import boto3
import sys
import datetime
from botocore.config import Config
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb', config=Config(region_name="us-west-2"))
table = dynamodb.Table('Find_Potty')
print(table.creation_date_time)

while 1:
    print("Enter a number\n1) Show all 'Find Potty' users\n2) Add a new 'Find Potty user'")


    select = input()

    if select == "1":


        bname = table.scan()

        allUsers = set(i['PottyUser'] for i in bname["Items"])
        print("User\'s names: ")
        for o in allUsers:
            print("\t" + o)


        userName = input("Enter the name of a user: ")
        allUserNames = table.query(KeyConditionExpression=Key("PottyUser").eq(userName))
        allBlocations = set(i["RestroomName"] for i in allUserNames["Items"])
        if len(allBlocations) > 0:
            print("User\'s names:")
            for g in allBlocations:
                print("\t" + g)

            location = input("Restroom Locations they have visited:")
            bathName = table.get_item(Key={"PottyUser": userName, "RestroomName": location})
            if "Item" in bathName:
                print(bathName["Item"]["bathName"])
                exit(0)
            else:
                print("No bathroom locations with that name.")
        else:
            print("No users with that name.")

    elif select == "2":
        bname = table.scan()
        allBlocations = set(i['RestroomName'] for i in bname["Items"])
        location_list = []
        print("Restroom Locations: ")
        for i in allBlocations:
            print("\t" + i)
            location_list.append(i)
        loc_name = input("Enter the name of the restroom location: \t")
        bath_name = input("Enter the name of the bathroom: \t")
        uName = input ("Enter the user\'s name: \t")
        table.put_item(Item={"PottyUser" : uName, "RestroomName" : loc_name, "bathName" : bath_name, "date" :  datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        
    else:
        print("not a valid selection")
