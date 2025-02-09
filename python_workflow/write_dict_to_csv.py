import csv

def write_dict_to_csv(dictionary, output_filename):
    """Write the input dictionary to a csv file"""
    
    with open(output_filename, 'w', newline='') as output_f:
        fieldnames = dictionary.keys()
        writer = csv.DictWriter(output_f, fieldnames = fieldnames)
        writer.writeheader()
        # For reference, data dict format is {key0:[key0data0,key0data1...],key1:[key1data0,key1data1...]}
        # to write the rows of the output csv file, need to grab the i'th value of each key for each row
        for i,row in enumerate(dictionary['Timestamp']):
            temp_dict = {}
            for col in dictionary.keys():    
                temp_dict[col] = dictionary[col][i]
            writer.writerow(temp_dict)