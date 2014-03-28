#!/usr/bin/env python2.7

import os;

import urllib2, urllib, sys, os, argparse
try:
  from poster.streaminghttp import register_openers
  from poster.encode import multipart_encode
except ImportError:
  print "First install the poster module as follows"
  print "mkdir -p $HOME/local/lib/python2.6/site-packages"
  print "export PYTHONPATH=$HOME/local/lib/python2.6/site-packages:$PYTHONPATH"
  print "easy_install --prefix=$HOME/local poster"
  sys.exit()

try:
  from awsserver import *
except ImportError:
  print "Please add /afs/cs/academic/class/15418-s14/assignments"
  print "to your PYTHONPATH"
  sys.exit()

parser = argparse.ArgumentParser(description="Launch on amazon")
parser.add_argument("--qsub", help="Max number of workers your program will require")
parser.add_argument("--logs", help="Get log files for a job")
parser.add_argument("--last", help="Get log files for the last job", action='store_true')
parser.add_argument('--test', default='hello418.txt', help='The test to run on your job')
parser.add_argument('--qstat', help='Get batch queue info', action='store_true')
args = parser.parse_args()

if not os.path.exists('scoreboard_token'):
  print "Go to http://dolores.sp.cs.cmu.edu/15418_spr13/index.php/scoreboard/token and generate a scoreboard token"
  sys.exit()

f = open('scoreboard_token', 'r')
user = f.read()
f.close

#UPLOAD_SERVER = 'http://107.20.226.209:8889/upload'
#JOB_QUEUE = 'http://107.20.226.209:8888/jobs'

def unzip_logs(job_id):
  cmd = "tar -xvf job-%s-logs.tar.gz" % job_id;
  print cmd
  os.system(cmd);
  
def post(data, path):
  datagen, headers = multipart_encode(data)
  req=urllib2.Request(path, datagen, headers)
  page=urllib2.urlopen(req).read()

  if data['type'] == 'LOGS':
    fo = open('job-' + data['job_id'] + '-logs.tar.gz', "w+")
    fo.write(page)
  else:
    return page

def qsub(num_nodes, job_id):
  register_openers()
  data = {
    'job_id': job_id,
    'type': "QSUB",
    'num_nodes': num_nodes,
    'test': args.test
  }
  print "Queuing test: %s" % args.test;
  return post(data, JOB_QUEUE)

def qstat():
  print "Queue Stats"
  register_openers()
  data = {
    'type': "QSTAT",
  }
  return post(data, JOB_QUEUE)

def upload_master():
  register_openers()
  os.chdir('./src')
  os.system('tar cvzf upload.tgz myserver')
  data = {
    'user': user,
    'file': open('upload.tgz', 'rb'),
    'type': 'UPLOAD'
  }
  os.chdir('..')
  return post(data, UPLOAD_SERVER)

def get_logs(job_id):
  register_openers()
  print "Getting logs for job: " + job_id
  data = {
    'user': user,
    'job_id': job_id,
    'type': 'LOGS'
  }
  post(data, UPLOAD_SERVER)

def poll_logs(job_id):
  register_openers()
  data = {
    'user': user,
    'job_id': job_id,
    'type': 'POLL_LOGS'
  }
  return post(data, JOB_QUEUE)

def retrieve_logs(job_id):
  ret = poll_logs(job_id)
  if ret == 'Job complete':
    print "Downloading logs from AWS..."
    get_logs(job_id)
    print "Unzipping to local directory..."
    unzip_logs(job_id);
  else:
    print ret

def verify_test(name):
  
  # only allow these tests to be specified
  known_tests = ['hello418.txt', 'uniform1.txt', 'uniform2.txt', 'uniform3.txt', 'uniform4.txt',
                 'nonuniform1.txt', 'nonuniform2.txt',
                 'grading_compareprimes.txt', 'grading_nonuniform1.txt', 'grading_nonuniform2.txt', 'grading_nonuniform3.txt',
                 'grading_burst.txt', 'grading_random.txt'];

  for t in known_tests:
    if t == name:
      return True;

  print "Error: unknown test (%s), aborting..." % name;
  return False;
    
if __name__ == '__main__':
  if args.qsub:
    if not verify_test(args.test):
      sys.exit()
    print "Uploading src/myserver directory to AWS..."
    job_id =  upload_master()
    if 'error' in job_id:
      print job_id
      sys.exit()
    print qsub(args.qsub, job_id)

    f = open(".lastjob", "w")
    f.write("%s" % job_id)
    f.close()
    
  elif args.logs:
    retrieve_logs(args.logs);
      
  elif args.last:
    if os.path.exists(".lastjob"):
      f = open(".lastjob", "r");
      job_name = f.readline()
      retrieve_logs(job_name);
      f.close();
    else:
      print "No last job information found (missing file: .lastjob)";
      
  elif args.qstat:
    print qstat()
  else:
    print "For usage help, type: python launch_amazon.py --help"
