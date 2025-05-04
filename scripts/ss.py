import sys
import subprocess
import time

port = sys.argv[1]
net_cond = sys.argv[2]
filename = '/home/client/logs/ss_logs_{}.log'.format(net_cond)

while True:
	with open(filename, 'a') as f:
		subprocess.run(['ss', '-tin', 'dst :{}'.format(port)], stdout=f)

	time.sleep(0.1)
