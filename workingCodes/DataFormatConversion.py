import os
import datetime


def epochToISO(ts):

    iso_timestamp = datetime.datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return iso_timestamp


def convert_line_F2_to_F1(line):
    lineItems = line.strip().split(',')
    timestamp = lineItems[0]
    mac_address = lineItems[1]
    sensor_type = lineItems[4]
    sensor_value = ','.join(lineItems[6:])
    format1_line = f"{epochToISO(int(timestamp))},raw/{sensor_type.lower()}/{mac_address},{timestamp},{sensor_value}"
    return format1_line
      
def convert_line_F1_to_F2(line):
    lineItems = line.strip().split(',')
    timestamp = lineItems[2]
    sensorsInfo = lineItems[1].split('/')
    mac_address = sensorsInfo[2]
    collector_type = sensorsInfo[1]
    sensor_value = ','.join(lineItems[3:])
    if collector_type == 'vac':
        sensor_type = 'VAC'
    elif collector_type == 'ps':
        sensor_type = 'PS'
    else:
        sensor_type = 'ST'
    format2_line = f"{timestamp},{mac_address},{sensor_type},1,{collector_type},1,{sensor_value}"
    return format2_line
     

def convertDataFormat(conversiontype, inputFile, outputFile):
    with open(inputFile, 'r') as file:
        inputdataLines = file.readlines()
        outputdataLines = [conversiontype(line) for line in inputdataLines]
    with open(outputFile, 'w') as file:
        for line in outputdataLines:
            file.write(line + '\n')


input_directory = 'D:/MachinesenseProjects/Format2Data'
output_directory = 'D:/MachinesenseProjects/formatconvertedRAW'
    

for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):  # Adjust the file extension as needed
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.csv")
        convertDataFormat(convert_line_F2_to_F1, input_file, output_file)