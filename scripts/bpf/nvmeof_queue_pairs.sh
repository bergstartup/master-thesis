#!/usr/bin/bpftrace


//kretfunc:blk_mq_map_queues
//{
//	$qmap = (struct blk_mq_queue_map *)args.qmap;
//	printf("CPU :0 = %d\n", $qmap->mq_map[0]);
//    	printf("CPU :1 = %d\n", $qmap->mq_map[1]);
//   	printf("CPU :2 = %d\n", $qmap->mq_map[2]);
//	printf("CPU :3 = %d\n", $qmap->mq_map[3]);
//    	printf("CPU :4 = %d\n", $qmap->mq_map[4]);
//    	printf("CPU :5 = %d\n", $qmap->mq_map[5]);
//    	printf("CPU :6 = %d\n", $qmap->mq_map[6]);
//	printf("CPU :7 = %d\n", $qmap->mq_map[7]);
//    	printf("CPU :8 = %d\n", $qmap->mq_map[8]);
//    	printf("CPU :9 = %d\n", $qmap->mq_map[9]);
//	printf("-----------------\n")
//}

kfunc:nvme_tcp_alloc_queue{
	printf("Queue id : %d is mapped to port ", args.qid);
}

kfunc:nvme_tcp_init_connection{
	$q = (struct nvme_tcp_queue *)args.queue;
	printf("%d\n",$q->sock->sk->__sk_common.skc_num);
}
