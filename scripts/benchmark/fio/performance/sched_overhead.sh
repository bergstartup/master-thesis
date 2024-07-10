#Change the target I/O scheduler to none
curl "http://172.16.137.2:8080/sched?sched=none&dev=nvme4n1"

#Change local scheduler to none
curl "http://localhost:8080/sched?sched=none&dev=nvme4c4n1"
python3 fio_runner.py remote_lhead_intra_none
python3 fio_runner.py remote_lhead_inter_nopin_none
python3 fio_runner.py remote_lhead_inter_none
python3 fio_runner.py remote_thead_none


#Change local scheduler to kyber
curl "http://localhost:8080/sched?sched=kyber&dev=nvme4c4n1"
python3 fio_runner.py remote_lhead_intra_none
python3 fio_runner.py remote_lhead_intra_ikyber
python3 fio_runner.py remote_lhead_inter_nopin_ikyber
python3 fio_runner.py remote_lhead_inter_ikyber
python3 fio_runner.py remote_thead_ikyber



#Change the target I/O scheduler to kyber
curl "http://172.16.137.2:8080/sched?sched=kyber&dev=nvme4n1"

#Change local scheduler to none
curl "http://localhost:8080/sched?sched=none&dev=nvme4c4n1"
python3 fio_runner.py remote_lhead_intra_tkyber
python3 fio_runner.py remote_lhead_inter_nopin_tkyber
python3 fio_runner.py remote_lhead_inter_tkyber
python3 fio_runner.py remote_thead_tkyber

#Change local scheduler to kyber
curl "http://localhost:8080/sched?sched=kyber&dev=nvme4c4n1"
python3 fio_runner.py remote_lhead_intra_itkyber
python3 fio_runner.py remote_lhead_inter_nopin_itkyber
python3 fio_runner.py remote_lhead_inter_itkyber
python3 fio_runner.py remote_thead_itkyber
