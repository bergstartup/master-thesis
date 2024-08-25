DEVICE=nvme0c0n1
curl "http://127.0.0.1:8080/sched?sched=mq-deadline&dev=${DEVICE}"
python3 fio_runner.py remote_pollprio_nice5_bread_fread
python3 fio_runner.py remote_pollprio_nice10_bread_fread
python3 fio_runner.py remote_pollprio_nice15_bread_fread
python3 fio_runner.py remote_pollprio_nice19_bread_fread
