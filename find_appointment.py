import requests
import datetime
import time
import logging
import winsound

# change these variables based on requirements
PINCODES = ['400057', '400056', '400055', '400058']
DATE = '07-08-2021'
MIN_AGE_LIMIT = 18
VACCINE = 'COVISHIELD'
QUERY_INTERVAL_MINS = 0.1
FREE = True


# makes GET request and retrives appointsments for a given pincode and date
#
# Arguments
# pincode: string
# date: string in format 'dd-mm-yyyy'
def get_appointments(pincode, date):
    # building request
    URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin'
    HEADERS = {
        'accept': 'application/json', 
        'Accept-Language': 'hi_IN'
    }
    PARAMS = {'pincode': pincode, 'date': date}

    response = requests.get(url = URL, params = PARAMS, headers = HEADERS)
    return response.json()


# filteres the response based on the keys given in filter_dict
# Note: The method has logic which is dependent on the response structure of CoWin API
#
# Arguments
# appointments_json_str: json string 
# filter_dict: dict
#   example: filter_dict = {'min_age_limit': 18, 'vaccine': 'COVAXIN'}
#   keys should match with CoWin response keys
#   data type should also be the same
def filter_appointments(appointments, filter_dict = {}):
    filtered_appointments = appointments['sessions']
    
    # applying all filteres given in dictionary
    for filter_key in filter_dict.keys():
        filtered_appointments = [x for x in filtered_appointments if(x[filter_key] == filter_dict[filter_key])]     

    return filtered_appointments

# Prints required details for each appointment
# Has logic based on json structure - I know its not a good idea, should have a pojo, but a good starting point
def print_appointments(appointments = []):
    if(len(appointments) == 0):
        logging.info("Sorry! No centeres available\n")
        return        
    
    for appointment in appointments:
        if(appointment['fee_type'] != 'Paid'):
            if(appointment['available_capacity'] == 0):
                logging.info("Sorry! center {} has no available slots\n".format(appointment['name']))
            else:
                logging.info("\nCenter Name: {}\nDose 1 Slots Available: {}\nDose 2 Slots Available: {}\nVaccine: {}\nPincode: {}\nDate: {}\n".format(appointment['name'], appointment['available_capacity_dose1'], appointment['available_capacity_dose2'], appointment['vaccine'], appointment['pincode'], appointment['date']))
                winsound.Beep(440, 2000)

def main():
    logging.basicConfig(level=logging.INFO, filename="logs.txt", filemode="a+",
                        format="%(message)s")
                        
    logging.info("Search Query\nPincode: {}\nDate: {}\nMin Age: {}\nVaccine: {}\nQuery Interval: {} Mins\n".format(PINCODES, DATE, MIN_AGE_LIMIT, VACCINE, QUERY_INTERVAL_MINS))
    
    filter_dict = {
    'min_age_limit': MIN_AGE_LIMIT,
    'vaccine': VACCINE
    }

    while(True):
        logging.info("Calling CoWin API")
        logging.info("Time: {}".format(datetime.datetime.now()))
                
        for pincode in PINCODES:
            appointments_json_str = get_appointments(pincode, DATE)
            filtered_appointments = filter_appointments(appointments_json_str, filter_dict)
            print_appointments(filtered_appointments)

        time.sleep(QUERY_INTERVAL_MINS * 60)
          
  
if __name__=="__main__":
    main()
