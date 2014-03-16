import os


my_nodes = [
    'ec2-23-20-102-155',
    'ec2-54-234-225-146',
    'ec2-23-22-240-206',
    'ec2-184-72-158-99',
    'ec2-54-234-47-227',
    'ec2-107-22-72-56',
    'ec2-50-19-130-44',
    'ec2-67-202-46-157',
    'ec2-54-235-47-234',
    'ec2-107-22-59-142']
    

#my_tests = ['grading_compareprimes.txt', 'grading_nonuniform1.txt', 'grading_nonuniform2.txt', 'grading_nonuniform3.txt', 'grading_burst.txt', 'grading_random.txt']

my_tests = ['grading_nonuniform3.txt', 'grading_burst.txt', 'grading_random.txt']


print "Copying tests to %d instances." % len(my_nodes);
    
for t in my_tests:
    for n in my_nodes:
        os.system("scp -i ../job_queue/mburman_keypair.pem tests/%s ubuntu@%s.compute-1.amazonaws.com:~/tests/" % (t, n) );
