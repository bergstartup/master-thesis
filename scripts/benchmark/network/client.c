#include<stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
int main() {
 int sock;
 if((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
 	printf("Socket creation error %d", sock);
	return -1;
 }

 struct sockaddr_in serv_addr;
 serv_addr.sin_family = AF_INET;
 serv_addr.sin_port = htons(9090);

 inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

 if(connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
 	printf("Connection failed\n");
	return -1;
 }

 
}
