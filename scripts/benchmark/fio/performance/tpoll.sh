curl "http://172.16.137.2:8080/poll?poll=0"
python3 fio_runner.py remote_perf_tpoll0
curl "http://172.16.137.2:8080/poll?poll=50"
python3 fio_runner.py remote_perf_tpoll50
curl "http://172.16.137.2:8080/poll?poll=100"
python3 fio_runner.py remote_perf_tpoll100
