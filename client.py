from timeit import default_timer as timer 
from dateutil import parser 
import threading 
import datetime 
import socket 
import time 
import argparse
from clock import Clock

counter =[0,0,0]
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d", "--drift_rate", type=float, default=1, help="Drift rate of the slave clock [Optional: Defaults to 1]")

args = arg_parser.parse_args()

slave_clock = Clock(drift_rate = args.drift_rate)

def startSendingTime(slave_client, server_address): 

	while True: 
		slave_client.sendto(str(slave_clock.getTime()).encode(), server_address) 
        #counter[0] += counter[0]  
		# print("\n Time sent successfully") 
		time.sleep(5)

def updateSlaveClock(synchronized_time):

    print("Slave node time before receiving the message:\t" + str(slave_clock.getTime()))
    print("Counter",counter)
    slave_clock.setTime(synchronized_time)
    print("Slave node time after receiving the message:\t" + str(synchronized_time) + "\n\n")
    print("Counter", counter)
def startReceivingTime(slave_client): 

    while True: 
		# receive data from the server 
        receivedTime, address = slave_client.recvfrom(1024)
        synchronized_time = parser.parse(receivedTime) 
        updateSlaveClock(synchronized_time)
        counter[0] = counter[0]+1
        # print("Synchronized time at the client is: " + str(synchronized_time), end = "\n\n") 


def initiateSlaveNode(master_port = 8080): 

    slave_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		 
		
	# define the master node address
    server_address = ('127.0.0.1', 8080)

    print("Slave node started...", end="\n\n")

	# start sending time to server 
    # print("Starting to receive time from server\n") 
    send_t_thread = threading.Thread(target = startSendingTime, args = (slave_client, server_address, )) 
    send_t_thread.start() 


	# start recieving synchronized from server 
    # print("Starting to recieving " + "synchronized time from server\n") 
    receive_t_thread = threading.Thread(target = startReceivingTime, args = (slave_client, )) 
    receive_t_thread.start() 


# Driver function 
if __name__ == '__main__': 

	# initialize the Slave / Client 
	initiateSlaveNode(master_port = 8080) 
