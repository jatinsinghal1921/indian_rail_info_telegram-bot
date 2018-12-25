import requests
import json

# Global Varaibles
RailwaysAPI_token = "Your Railways API token"
railways_api_url = "https://api.railwayapi.com/v2/"


# Get PNR Status Info of all the passengers to a same ticket
def pnr_status(pnr_no):
    global railways_api_url
    railways_api_url += "pnr-status/pnr/" + str(pnr_no) + "/apikey/" + RailwaysAPI_token + "/"
    response = requests.get(railways_api_url)
    print("Status Code : " + str(response.status_code))
    
    if response.status_code != 200:
        print("Request Failed")
        return -1
    
    json_output = response.json()
    print(json_output)
    passengers_pnrstatus_list = json_output["passengers"]
    print("Length of pnrStatusList : " + str(len(passengers_pnrstatus_list)))

    output_str = "PNR Details : \n\n"
    for entry in passengers_pnrstatus_list:
        passenger_id = entry["no"]
        current_status = entry["current_status"]
        booking_status = entry["booking_status"]
        output_str += "passenger : " + str(passenger_id) + "\n" + "Current Status : " + current_status + "\n" + "Booking Status : " + booking_status + "\n\n"

    return output_str


# Get Train Availability Info for specific train.
def get_availability_info(train_no,src_stn_code,des_stn_code,date,class_code,quota_code):    
    global railways_api_url
    railways_api_url += "check-seat/train/" + str(train_no) + "/source/" + str(src_stn_code) + "/dest/" + str(des_stn_code) + "/date/" + str(date) + "/pref/" + str(class_code) + "/quota/" + str(quota_code) + "/apikey/" + RailwaysAPI_token + "/"
    response = requests.get(railways_api_url)
    
    print("Status Code : " + str(response.status_code))
    if response.status_code != 200:
        print("Request Failed")
        return -1

    json_output = response.json()
    availability_list = json_output['availability']
    print("Length of Availability list : " + str(len(availability_list)))

    output_str = "Availability Details:\n"
    for entry in availability_list:
        date = entry['date']
        status = entry['status']
        output_str += date + " -----------> " + status + "\n"

    return output_str


def main():
    train_no = 12649
    src_stn_code = "YPR"
    des_stn_code = "KCG"
    date = "24-12-2018"
    class_code = "SL"
    quota_code = "GN"
    
    availability_details = get_availability_info(train_no,src_stn_code,des_stn_code,date,class_code,quota_code)
    print(availability_details)

    # pnr_no = "4561574060"
    # pnr_details = pnr_status(pnr_no)
    # print(pnr_details)

if __name__ == "__main__":
    main()
