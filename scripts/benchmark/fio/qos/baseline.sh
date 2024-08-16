DEVICE=nvme1n1
curl "http://127.0.0.1:8080/sched?sched=none&dev=${DEVICE}"
python3 fio_runner.py local_baseline_bread_fread
