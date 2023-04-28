#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#define SERV_TCP_PORT 59002
#define SERV_HOST_ADDR "192.168.125.10"
#define MAXLINE 512

//int written(int fd, char *ptr, int nbytes);
void send_chars (int sockfd, int len, char* sendline);
void read_console(char* line);
char *pname;

int main(int argc, char *argv[])
{
        int sockfd;
        struct sockaddr_in serv_addr;
        pname = argv[0];
        bzero((char *) &serv_addr, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr.s_addr = inet_addr(SERV_HOST_ADDR);
        serv_addr.sin_port = htons(SERV_TCP_PORT);
        if((sockfd = socket(AF_INET, SOCK_STREAM,0)) < 0){
                printf("Client: Can't Open Stream Socket\n");
        }
        printf("Client: Connecting...\n");
        if(connect(sockfd,(struct sockaddr *) &serv_addr, sizeof(serv_addr))<0){
                printf("Client: Can't Connect to the server\n");
        }
        else{
				
                printf("Connected\n");
				char sendline[128];
				read_console(sendline);
                send_chars(sockfd, strlen(sendline), sendline);
        }
        exit(0);
}

void read_console (char* line)
{
    printf("Enter a string: ");
	gets(line);
}

void send_chars (int sockfd, int len, char* sendline)
{
		int nleft, nwritten;
        nleft = len;
        while(nleft > 0) {
                nwritten = write(sockfd, sendline, nleft);
                if(nwritten <= 0) {
						// error - can't send
						printf("strcli:written error on sock\n");
                        return;
                }
                nleft -= nwritten;
                sendline += nwritten;
        }
        printf("wrote %i chars\n", len);
		
        sleep(1);
}

/*
int written(int fd, char *ptr, int nbytes)
{
        int nleft, nwritten;
        nleft = nbytes;
        while(nleft > 0) {
                nwritten = write(fd, ptr, nleft);
                if(nwritten <= 0) {
                        return(nwritten);
                }
                nleft -= nwritten;
                ptr += nwritten;
        }
        return(nbytes - nleft);
} */
