import os
import re
import pandas as pd
import argparse


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Convert logs to CSV for a given sender.')
    ## -f is the file path
    argparser.add_argument('-f', '--file', type=str, required=True, help='Path to the log file')
    ## -s is the sender
    argparser.add_argument('-s', '--sender', type=str, required=True, help='Sender to filter logs. Format is ip:port')
    args = argparser.parse_args()

    with open(args.file) as f:
        lines = f.readlines()

    i=0
    conn_hist = []
    while i < len(lines):
        line = lines[i]
        if args.sender in line:
            info = lines[i+1].strip().replace('send ', 'send:').replace('delivery_rate ', 'delivery_rate:').replace('pacing_rate ', 'pacing_rate:')
            conn_hist.append(dict(re.findall(r'(\w+):([\w.]+)', info)))
            i+=2
        else:
            i+=1
    
    out_file = re.findall(r'([\w%]+)\.log', args.file)[0]
    out_file = out_file + '_' + args.sender.replace(':', '_') + '.csv'
    cwd = os.getcwd()

    pd.DataFrame(conn_hist).to_csv(os.path.join(cwd,out_file), index=False)