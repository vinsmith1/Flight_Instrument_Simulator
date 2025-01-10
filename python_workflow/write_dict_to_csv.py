import csv

def write_dict_to_csv(dictionary, output_csv_filename):
    """ Write the input dictionary to a csv file
    :param frames: dictionary to write to csv
    :param csv_filename: filename of the csv file to write
    :param write_outputframes_log: boolean to write the output frames log
    """
    with open(output_csv_filename, 'w', newline='') as output_f:
        fieldnames = dictionary.keys()
        writer = csv.DictWriter(output_f, fieldnames = fieldnames)
        writer.writeheader()
        # For reference, data dict format is {key0:[key0data0,key0data1...],key1:[key1data0,key1data1...]}
        # to write the rows of the output csv file, need to grab the i'th value of each key for each row
        for i,row in enumerate(dictionary['Timestamp']):
            tempDict = {}
            for col in dictionary.keys():    
                tempDict[col] = dictionary[col][i]
            writer.writerow(tempDict)