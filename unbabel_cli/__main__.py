import os
import sys
import json
import pandas as pd
from argparse import ArgumentParser
from datetime import tzinfo, timedelta, datetime

def moving_avg(input_data,args):
    def mean(j_obj, n):
        sum = 0
        n = min(n, len(j_obj) )
        result = list( 0 for x in j_obj)
        valid_n = list( 1 for x in j_obj)
        for i in range( 0, len(j_obj)):
            count = 0
            for j in range(max(0, i-n+1), i+1):
                if j_obj[j] > 0:
                    count += 1
            if count > 0:
                valid_n[i] = count
        for i in range( 0, n ):
            sum = sum + j_obj[i]
            result[i] = sum / valid_n[i]
        for i in range( n, len(j_obj) ):
            sum = sum - j_obj[i-n] + j_obj[i]
            result[i] = sum / valid_n[i]
        return result

    input_data['timestamp'] = input_data['timestamp'].apply(lambda x: x[:16])
    input_data['timestamp'] = pd.to_datetime(input_data['timestamp'], format='%Y-%m-%d %H:%M')
    start_time = min(input_data['timestamp'])
    end_time = max(input_data['timestamp']) + timedelta(minutes = 1)
    input_data['timestamp'] = input_data['timestamp'] + timedelta(minutes = 1)
    date_range = pd.date_range(start = start_time, end=end_time, freq='min')
    output = pd.DataFrame(date_range, columns={'timestamp'})
    output = pd.merge(output, 	input_data[['timestamp','duration']], how='left', left_on= 'timestamp', right_on= 'timestamp').fillna(0)
    output = output.groupby(by=['timestamp'])['duration'].mean().reset_index()
    output['moving_avg'] = mean(output['duration'], int(args.window_size))
    output.drop(['duration'], axis = 1, inplace = True)
    return output

def main():
    passed_args = ArgumentParser()
    passed_args.add_argument("-i", "--input_file", dest="filename",help="json input file", metavar="FILE")
    passed_args.add_argument("-w", "--window_size", dest="window_size",help="window size for the moving average")
    args = passed_args.parse_args()

    #Reading Json file data
    with open(args.filename, 'r') as f:
        data = [json.loads(line) for line in f]
    input_data = pd.DataFrame(data)

    output_data = moving_avg(input_data,args)

    #print output
    for i in range(len(output_data)):
        #print(output_data['timestamp'][i])
        print('{"date": "'+str(output_data['timestamp'][i])+'", "average_delivery_time":'+ str(output_data['moving_avg'][i])+'}')

if __name__ == '__main__':
    main()
