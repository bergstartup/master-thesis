#device ip ip_addr_family
#if ipv6 use ip%interface
sudo modprobe nvmet
sudo modprobe nvmet-tcp
cd /sys/kernel/config/nvmet/subsystems
sudo mkdir nvme-test-target
cd nvme-test-target/
echo 1 | sudo tee -a attr_allow_any_host > /dev/null
sudo mkdir namespaces/1
cd namespaces/1

echo -n $1 |sudo tee -a device_path > /dev/null
echo 1|sudo tee -a enable > /dev/null
sudo mkdir /sys/kernel/config/nvmet/ports/1
cd /sys/kernel/config/nvmet/ports/1
echo $2 |sudo tee -a addr_traddr > /dev/null
echo tcp|sudo tee -a addr_trtype > /dev/null
echo 4420|sudo tee -a addr_trsvcid > /dev/null
echo $3 |sudo tee -a addr_adrfam > /dev/null
sudo ln -s /sys/kernel/config/nvmet/subsystems/nvme-test-target/ /sys/kernel/config/nvmet/ports/1/subsystems/nvme-test-target

