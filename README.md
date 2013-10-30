***Operation Manual***

	Setup:


1.	Download the files from GitHub by entering the following command:

    	git clone https://github.com/jorgeorodriguez/ISTA520_midterm.git


2.	Download CCTools 4.0.2 & Installing
	
    	wget http://www.nd.edu/~ccl/software/files/cctools-4.0.2-source.tar.gz

    	cd ~/cctools-4.0.2-source
    	
    	./configure --prefix ~/cctools && make install

3.	Set environment variables by running the following commands:

    	export PATH=~/cctools/bin:${PATH}
    	
    	export PYTHONPATH=~/cctools/lib/python2.4/site-packages:~/cctools/lib/python2.6/site-packages:${PYTHONPATH}




	Get started:


1.	Run the following script to split the files into sections for benchmarking:

    	python splitting_densityGrid.py

2.  	Now we need to take take the IDs from the grav_pos.txt file:
    
    	python split_grav_pos.py


3.	We can now run workqueue to give jobs to workers. This workqueue needs prism.py and grav_per_point.py so make sure they are in the directory

    	python grav_wq.py
    

4.	Next, we send workers to start processing the tasks. This command will submit a worker to lima with a timeout period of 10 seconds, using port number 54601. 
    	The last value will specify how many workers you would like to send for this job

    	torque_submit_workers -d all -t 10 lima.futuregrid.org 54601 1



5.	The grav_wq.py script will generate several output files that will need to be combined into one. For that we can run:

    	merge.output.py


5.	Finally, we can generate a checksum on the final output file to make sure it maintains its integrity:

    	md5sum finalfile.txt
