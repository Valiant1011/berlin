import multiprocessing
import os
import signal
import sys
import time
from interface import *

sys.path.append('../')

def main():
	print('[ BERLIN ] : Welcome!')
	####################################################################
	# Create variables/lists that will be shared between processes
	data_changed_flags = multiprocessing.Array('i', 30)
	# This queue will be polled from bitsoj_core for handling tasks like 
	# database updates or data transmission
	task_queue = multiprocessing.Queue(maxsize = 1000)   
	
	# Initialize GUI handler
	try:
		init_gui(data_changed_flags, task_queue)
	except Exception as error:
		print("[ CRITICAL ] GUI could not be loaded! Restart Server." + str(error))
			
	print('[ BERLIN ] : Bella Ciao!')

if __name__ == '__main__':
	# If this file is run natively, and not imported
	main()