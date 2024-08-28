curl "http://127.0.0.1:8080/sched?sched=none&dev=nvme1c1n1"
curl "http://127.0.0.1:8080/sched?sched=none&dev=nvme0c0n1"
python3 fio_runner.py remote_ns_bread_fread
#ns represents no sharing
