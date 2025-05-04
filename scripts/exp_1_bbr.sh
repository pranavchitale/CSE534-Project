# exp settings
declare num_runs=${1:-1}

# iperf params
declare cca=${2:-bbr}
declare iperf_port=${3:-5200}
declare iperf_time=${4:-60}
declare bw=${5:-500M}
#declare window_size

# network setup
declare loss=${6:-2%}
declare rtt=${7:-100ms}
declare buf=${8:-2M}


if [[ ${cca} == "bbr3" ]]; then
	bash config_set_ccabbr3.sh
else
	bash config_set_ccabbr2.sh
fi

# output files
declare resultsfile=/home/client/expt/logs/exp_1_${cca}_${loss}_results

# setup network
if [[ ${loss} == "0%" ]]; then
	sudo tc qdisc add dev ens34 root netem delay ${rtt} limit ${buf}
else
	sudo tc qdisc add dev ens34 root netem loss ${loss} delay ${rtt} limit ${buf}
fi

# initiate iperf experiments
for ((i=1;i<=${num_runs};i++)) do
	python3 ss.py ${iperf_port} ${rtt}_${bw}_${buf}_${loss}_${cca}_${i} & ss_pid=$!
	sudo iperf3 -J --logfile ${resultsfile} -c SERVER_IP -b ${bw} -t ${iperf_time} -i 1 -p ${iperf_port} --get-server-output
	kill $ss_pid

done

sudo tc qdisc del dev ens34 root
