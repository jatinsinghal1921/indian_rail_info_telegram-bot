import requests
import json

# Global variables
railways_api_token_day_count = "Your API Token"
railways_api_url_day_count = "http://indianrailapi.com/api/v2/"

railways_api_url_credit_count = "https://api.railwayapi.com/v2/"
railways_api_token_credit_count = "Your API Token"

response_codes_file_obj = open("response_codes.json", "r")
response_codes_dict = json.load(response_codes_file_obj)


class ErrorHandling:
    def __init__(self):
        print("In Error Handler Class")

    # Handling Errors
    def error_handler(self, response):
        print("In Error handler function")
        print(response)
        if response.status_code != 200:
            output_str = "Status Code " + str(
                response.status_code) + "\nThere is an error in serving your Request.\nPlease try again later. "
            print(output_str)
            return output_str

        json_output = response.json()
        output_str = 1
        try:
            response_code = json_output['ResponseCode']
            if str(response_code) != "200":
                output_str = "Response Code " + str(response_code) + "\nThere is an Error in Response"
        except KeyError as e:
            print("There is a key error Exception, Key {} doesn't exists. Instead using 'response_code' as key".format(e))
            response_code = json_output['response_code']
            if str(response_code) != "200":
                output_str = "Response Code " + str(response_code) + "\n" + response_codes_dict[str(response_code)]

        print(output_str)
        return output_str


class RailInfoDayCount(ErrorHandling):
    # Constructor
    def __init__(self):
        print("New Object Created of Rail Info Day Count Class")

    # Train Fare
    def train_fare(self, train_no, src_stn_code, des_stn_code, quota_code):
        global railways_api_url_day_count, railways_api_token_day_count
        request_url = railways_api_url_day_count + "TrainFare/apikey/" + railways_api_token_day_count + "/TrainNumber/" + train_no + "/From/" + src_stn_code + "/To/" + des_stn_code + "/Quota/" + quota_code
        response = requests.get(request_url)

        status = self.error_handler(response)
        if status != 1:
            return status

        json_output = response.json()
        train_fares = json_output["Fares"]
        output_str = ""
        for train_class in train_fares:
            output_str += train_class["Name"] + " --------------> " + train_class["Fare"] + "\n"

        print(output_str)
        return output_str


class RailInfoCreditCount(ErrorHandling):
    def __init__(self):
        print("New Object Created of Rail Info Credit Count")

    # Get PNR Status Info of all the passengers to a same ticket
    def pnr_status(self, pnr_no):
        global railways_api_url_credit_count, railways_api_token_credit_count
        request_url = railways_api_url_credit_count + "pnr-status/pnr/" + pnr_no + "/apikey/" + railways_api_token_credit_count + "/"
        response = requests.get(request_url)

        status = self.error_handler(response)
        if status != 1:
            return status

        json_output = response.json()
        passengers_pnr_status_list = json_output["passengers"]
        passengers_count = len(passengers_pnr_status_list)
        print("Passengers Count : " + str(passengers_count))

        output_str = "PNR Details : \n\n"
        for entry in passengers_pnr_status_list:
            passenger_id = entry["no"]
            current_status = entry["current_status"]
            booking_status = entry["booking_status"]
            output_str += "passenger : " + str(
                passenger_id) + "\n" + "Current Status : " + current_status + "\n" + "Booking Status : " + booking_status + "\n\n"

        print(output_str)
        return output_str

    # Get Seat Availability Info for specific train on specific date.
    def seat_availability_info(self, train_no, src_stn_code, des_stn_code, date, class_code, quota_code):
        global railways_api_url_credit_count, railways_api_token_credit_count
        request_url = railways_api_url_credit_count + "check-seat/train/" + train_no + "/source/" + src_stn_code + "/dest/" + des_stn_code + "/date/" + date + "/pref/" + class_code + "/quota/" + quota_code + "/apikey/" + railways_api_token_credit_count + "/"
        response = requests.get(request_url)

        print("Response has been fetched and it is going to be validated")

        status = self.error_handler(response)
        if status != 1:
            return status

        json_output = response.json()
        availability_list = json_output['availability']
        print("Length of Availability list : " + str(len(availability_list)))

        output_str = "Availability Details:\n"
        for entry in availability_list:
            date = entry['date']
            status = entry['status']
            output_str += date + " -----------> " + status + "\n"

        print(output_str)
        return output_str

    # get the availability of trains
    def train_availability_info(self, src_stn_code, des_stn_code, date):
        global railways_api_url_credit_count, railways_api_token_credit_count
        request_url = railways_api_url_credit_count + "between/source/" + src_stn_code + "/dest/" + des_stn_code + "/date/" + date + "/apikey/" + railways_api_token_credit_count + "/"
        response = requests.get(request_url)

        status = self.error_handler(response)
        if status != 1:
            return status

        json_output = response.json()
        trains_list = json_output["trains"]
        print("NO. of trains : " + str(len(trains_list)))

        trains_info = []
        for train in trains_list:
            l = ""
            l += "Train : " + train["name"] + "(" + train["number"] + ")" + "\n"
            l += "Source Stn : " + train["from_station"]["name"] + "\n"
            l += "Destination Stn : " + train["to_station"]["name"] + "\n"
            l += "Departure Time : " + train["src_departure_time"] + "\n"
            l += "Arrival Time : " + train["dest_arrival_time"] + "\n"
            l += "Total Time : " + train["travel_time"] + "\n"
            trains_info.append(l)

        print(trains_info)
        return trains_info

    # Track Train at run time
    def track_train(self, train_no, date):
        global railways_api_url_credit_count, railways_api_token_credit_count
        request_url = railways_api_url_credit_count + "live/train/" + train_no + "/date/" + date + "/apikey/" + railways_api_token_credit_count + "/"
        response = requests.get(request_url)

        status = self.error_handler(response)
        if status != 1:
            return status

        json_output = response.json()
        output_str = json_output["position"]
        print(output_str)
        return output_str

    # Track Train at run time
    def train_details(self, train_name):
        global railways_api_url_credit_count, railways_api_token_credit_count
        request_url = railways_api_url_credit_count + "name-number/train/" + train_name + "/apikey/" + railways_api_token_credit_count + "/"
        response = requests.get(request_url)

        status = self.error_handler(response)
        if status != 1:
            return status

        json_output = response.json()
        output_str = json_output["train"]["name"] + " -----------> " + json_output["train"]["number"] + "\n" + "Running Details:" + "\n"
        for day in json_output["train"]["days"]:
            output_str += day["code"] + " ------------> " + day["runs"] + "\n"
        print(output_str)
        return output_str


def main():
    train_no = "12723"
    src_stn_code = "hyb"
    des_stn_code = "ndls"
    date = "01-01-2019"
    class_code = "3a"
    quota_code = "gn"
    train_name = "Telangana Express"
    pnr = "1234567890"

    class1_obj1 = RailInfoDayCount()
    # class1_obj1.track_train(train_no, "20190101")
    # class1_obj1.train_fare(train_no, src_stn_code, des_stn_code, quota_code)

    class2_obj1 = RailInfoCreditCount()
    # class2_obj1.seat_availability_info(train_no, src_stn_code, des_stn_code, date, class_code, quota_code)
    class2_obj1.train_availability_info(src_stn_code,des_stn_code,date)
    # class2_obj1.pnr_status(pnr)
    # class2_obj1.track_train(train_no,date)
    # class2_obj1.train_details("AP Sampark Kranti")


if __name__ == "__main__":
    main()
