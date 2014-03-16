#
# Kayvon's code to generate Assignment 4 traces
#

import argparse;
import random;

def REQUEST_mostviewed(req_time, m1, d1, m2, d2):
    return "{\"time\": %d, \"work\": \"cmd=mostviewed;start=2013-%d-%d;end=2013-%d-%d\", \"resp\": \"\"}" % (req_time, m1, d1, m2, d2);

def REQUEST_countprimes(req_time, n):
    return "{\"time\": %d, \"work\": \"cmd=countprimes;n=%d\", \"resp\": \"\"}" % (req_time, n);

def REQUEST_compareprimes(req_time, arg1, arg2, arg3, arg4):
    return "{\"time\": %d, \"work\": \"cmd=compareprimes;n1=%d;n2=%d;n3=%d;n4=%d\", \"resp\": \"\"}" % (req_time, arg1, arg2, arg3, arg4);

def REQUEST_418wisdom(req_time, n):
    return "{\"time\": %d, \"work\": \"cmd=418wisdom;x=%d\", \"resp\": \"\"}" % (req_time, n);

def REQUEST_lastrequest(req_time):
    return "{\"time\": %d, \"work\": \"cmd=lastrequest\", \"resp\": \"ack\"}" % req_time;


# make_compare_primes:
#
# The following trace is the compareprimes test. The idea is to
# release a job every second and to expect a response within 1.5 sec.
# This requires parallelism of the request itself to meet this latency
# guarantee.

# grades_compareprimes.txt
def make_compare_primes():
    random.seed(0);
    lasttime = 0;
    for i in range(30):
        arg1 = random.randint(400000, 1000000);
        arg2 = random.randint(400000, 1000000);
        arg3 = random.randint(400000, 1000000);
        arg4 = random.randint(400000, 1000000);

        if arg1 >= arg2:
            arg2 , arg1 = arg1 , arg2
            
        if arg3 >= arg4:
            arg4 , arg3 = arg3 , arg4

        lasttime = 1000 * i;
        print REQUEST_compareprimes(lasttime, arg1, arg2, arg3, arg4);

    return lasttime;

# grades_nonuniform1.txt
def make_rampupdown():
    random.seed(0);
    lasttime = 0;
    step = 2500;
    lastjump = 0;
    for i in range(50):
        current = lasttime + step;

        n = random.randint(0, 100000);
        print REQUEST_418wisdom(current, n);

        if (current - lastjump >= 5000):
            lastjump = current;
            step = step - 300;
            if step < 250:
                step = 250;
            
        lasttime = current;
        
    for i in range(30):
        current = lasttime + step;
        n = random.randint(0, 100000);
        print REQUEST_418wisdom(current, n);

        lasttime = current;
        step = step + 100;
        if step >= 2500:
           step = 2500;
            
    return lasttime;

# grades_nonuniform2.txt
def make_step():
    random.seed(0);
    lasttime = 0
    current = lasttime;

    periods = [2500, 500, 10000, 750, 10000];
    durations = [10, 4, 20, 10, 20]
    for i,dur in enumerate(durations):
        start = current
        end = start + 1000 * dur;
        while current < end:
            n = random.randint(0, 100000);
            print REQUEST_418wisdom(current, n);
            lasttime = current
            current = current + periods[i];
        
    return lasttime;

# grades_nonuniform3.txt
def make_spike_cache():
    random.seed(0);
    duration = 15;
    lasttime = 0;
    current = lasttime;
    repeated = [348394, 679060, 1000010, 234567, 480123, 990600, 230237, 450923, 129000, 609902];
    for i in range(4):
        start = current;
        end = start + 1000 * duration;
        while current < end:
            n = random.randint(700000, 1000000);
            print REQUEST_countprimes(current, n);
            lasttime = current
            current = current + 1500;
        for n in repeated:
            print REQUEST_countprimes(current, n);
            lasttime = current;
            current = current + 25;

    return lasttime;

# grades_burst.txt
def make_burst():
    random.seed(0);
    lasttime = 0;
    current = lasttime;
    step = 300;
    for i in range(10):
        n = random.randint(650000, 750000);
        print REQUEST_countprimes(current, n);
        lasttime = current
        current = current + step;

    for i in range(15):
        n = random.randint(550000, 750000);
        print REQUEST_countprimes(current, n);
        lasttime = current;
        current = current + step;
        step = step - 20;
        if step < 200:
           step = 200;
           
    current = current + 4000;
    for i in range(20):
        print REQUEST_418wisdom(current, random.randint(0,100000));
        lasttime = current
        current = current + 10
        
    for i in range(14):
        month1 = random.randint(1,2);
        month2 = month1 + random.randint(0,3 - month1);
        day1 = random.randint(1,30);
        day2 = random.randint(1,30);
        if month1 == month2:
            day2 = day1 + random.randint(1, 30 - day1);
        print REQUEST_mostviewed(current, month1, day1, month2, day2);
        lasttime = current
        current = current + 10;
    
    return lasttime
    
def make_uniform_random():

    random.seed(0)
    lasttime = 0
    current = lasttime;
    step = 1000;
    step_clamp = 500;

    print REQUEST_countprimes(current, 1000000);
    current = current + 1500;
    
    while current < 60000:
        n = random.randint(0,4);
        if n == 0:
            print REQUEST_418wisdom(current, random.randint(0,4));
        elif n == 1:
            print REQUEST_countprimes(current, random.randint(800000, 1000000));
        elif n == 2:
            print REQUEST_countprimes(current, 1000000);
            print REQUEST_countprimes(current+1, 1000000);
            print REQUEST_countprimes(current+2, 1000000);
            print REQUEST_countprimes(current+3, 1000000);
            print REQUEST_countprimes(current+4, 1000000);
        elif n == 3:
            month1 = 1;
            month2 = 3;
            day1 = random.randint(1,6);
            day2 = day1 + random.randint(10, 30 - day1);
            print REQUEST_mostviewed(current, month1, day1, month2, day2);
        
        elif n == 4:
            arg1 = random.randint(750000, 750005);
            arg2 = random.randint(750000, 750005);
            arg3 = random.randint(750000, 750005);
            arg4 = random.randint(750000, 750005);

            if arg1 >= arg2:
                arg2 , arg1 = arg1 , arg2
            if arg3 >= arg4:
                arg4 , arg3 = arg3 , arg4

            print REQUEST_compareprimes(current, arg1, arg2, arg3, arg4);

        lasttime = current;
        current = current + step;
        step = step - 100;
        if step < step_clamp:
            step = step_clamp;

    return lasttime; 
            
parser = argparse.ArgumentParser(description="Generate Assignment 4 traces")
parser.add_argument('--trace', help='Name of trace')
args = parser.parse_args();

lasttime = 0

if args.trace == "compareprimes":
    lasttime = make_compare_primes();

elif args.trace == "rampupdown":
    lasttime = make_rampupdown();

elif args.trace == "step":
    lasttime = make_step();

elif args.trace == "spikecache":
    lasttime = make_spike_cache();

elif args.trace == "burst":
    lasttime = make_burst();
    
elif args.trace == "random":
    lasttime = make_uniform_random();
    
print REQUEST_lastrequest(lasttime + 500); 
    
