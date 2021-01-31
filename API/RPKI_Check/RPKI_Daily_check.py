import json
from urllib.request import urlopen
import time
import datetime
import sys
import logging
import logging.handlers
import csv
import config

#Create logger
my_logger = logging.getLogger('MyLogger')
#We will pass the message as INFO
my_logger.setLevel(logging.INFO)
#Define SyslogHandler
log_ip = (config.server_ip)
handler = logging.handlers.SysLogHandler(address = (log_ip, 514))
my_logger.addHandler(handler)
#end of logger creation
# define file
# local_file_name = "/home/rob/RPKI_Checks/Daily_Checks/RPKI_Daily_checks_" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M')+ ".csv"
local_file_name = "RPKI_Daily_checks_" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M')+ ".csv"
with open(local_file_name, "w", newline='' ) as csv_file:
    writer = csv.writer(csv_file, delimiter=',' )
    writer.writerow(["ASN", "Date", "Prefix", "RPKI_Status"])



def find_invalid():
    try:
        with urlopen("https://rpki-validator.ripe.net/api/bgp/?pageSize=1000&search=AS812&sortBy=prefix&sortDirection=asc") as response:
            source = response.read()
            data =  json.loads(source)
        # print(source)
        # This will print out data in json format
        # print(json.dumps(data, indent=2))

# These 2 lines will print out a count of total RPKI records matching AS812
# totalprefix = (len(data['data']))
# print('Total number of prefixes for AS812 is ' + str(totalprefix)


        for item in data['data']:
            status = item['validity']
            block = item['prefix']
            asnum = item['asn']
            if status == 'INVALID':
                # Empty Array
                tmp=[]
                # create array
                message = ' RPKI_CHECK_FAILED ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S') + ' https://rpki.cloudflare.com/?view=bgp&asn=812&prefix=&validState=Invalid'
                # Appending message to the empty array tmp
                tmp.append(block + ' Prefix Status ')
                tmp.append(status)
                tmp.append(message)
                # Printing the message
                print(tmp)
                # Send data as syslog
                my_logger.info(tmp)
                # print(block, status + ' RPKI Status Failed On ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))
            else:
                check_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')
                with open(local_file_name, "a", newline='' ) as csv_file:
                    writer = csv.writer(csv_file, delimiter=',' )
                    writer.writerow([asnum, check_date, block, status])
                # with open(local_file_name, "a") as myfile:
                #     myfile.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S') + ';')
                #     myfile.write(block + ';')
                #     myfile.write(status + ';')
                #     myfile.write('\n')
    except Exception as e:
        logging.exception(e)

# Main method.
if __name__ == '__main__':
    find_invalid()


