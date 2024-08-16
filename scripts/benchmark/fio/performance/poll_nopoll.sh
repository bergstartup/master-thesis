sudo nvme disconnect -d /dev/nvme4
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev4 10 0
sudo python3 fio_runner.py remote_perf_npoll
sudo nvme disconnect -d /dev/nvme4
../../../setup/nvmeof_tcp_initiator_setup.sh thesis.dev4 10 10
sudo python3 fio_runner.py remote_perf_poll
