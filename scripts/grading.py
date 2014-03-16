

CORRECTNESS_PTS = 3
QUESTION_PTS = 10
BIG_QUESTION_PTS = 12

# deduct 75% of points if students allocate maximum resources
NO_ELASTIC_DEDUCTION = .75
SMALL_NO_ELASTIC_DEDUCTION = .5

def perf_eval(actual, low, high):

    if actual < low:
        return 1.0;
    elif actual >= high:
       return 0.0;
    else:
        return 1.0 - (float(actual - low) / (high - low));


def grade_compareprimes(is_correct, trace_jobs, cpu_seconds):

    latency_low_threshold = 2000
    latency_high_threshold = 3000
    cpu_baseline = 125;
    cpu_redline = 165;

    perf_pts = 0.0;
    quick_count = total = 0
    
    for job in trace_jobs:
        if job.descr['work'] == "cmd=lastrequest":
            continue;
        total = total+1;
        latency = 1000 * job.latency.total_seconds();
        perf_pts = perf_pts + perf_eval(latency, latency_low_threshold, latency_high_threshold);
        if latency < latency_low_threshold:
            quick_count = quick_count + 1;
            
    if not is_correct:
        print "Grade: 0 of 13 points";
    else:
        int_perf = int(QUESTION_PTS * min(1.0, perf_pts / total / .9));
        int_cost = int(QUESTION_PTS * min(1.0, (float(max(0.0, cpu_seconds - cpu_baseline)) / (cpu_redline - cpu_baseline)) * SMALL_NO_ELASTIC_DEDUCTION));  
        score = max(0, CORRECTNESS_PTS + int_perf - int_cost);

        print "----------------------------------------------------------------"
        print "Grade: %d of 13 points" % score;
        print "         + 3 points for correctness"
        print "         + %d points for perf" % int_perf;
        print "         - %d points for worker usage" % int_cost;
        print ""
        print "         %.1f%% requests met the %d ms latency requirement" % (100.0 * quick_count / total, latency_low_threshold);
        print "----------------------------------------------------------------"
        
    print ""
    print "Grading Details:"
    print "  Perf:  * Summary: you get full perf points if 90% of your responses have"
    print "           latency under %d ms" % latency_low_threshold;
    print "         * You get one credit per response under %d ms. Partial credit is assigned" % latency_low_threshold;
    print "           with linear falloff to no credit at %d ms latency." % latency_high_threshold;
    print "         * Perf points are: %d * (num_credits / total_requests) / 0.9" % QUESTION_PTS;
    print ""
    print "  Usage: * No resource penalty up to %d CPU-seconds." % cpu_baseline;
    print "         * Linear falloff to minus 50%% points at %d sec" % cpu_redline;
    print ""    


        
def grade_nonuniform1(is_correct, trace_jobs, cpu_seconds):

    latency_low_threshold = 2000;
    latency_high_threshold = 4000;
    cpu_baseline = 150
    cpu_redline = 390;

    perf_pts = 0.0;
    quick_count = total = 0

    for job in trace_jobs:
        if job.descr['work'] == "cmd=lastrequest":
            continue;
        total = total+1;
        latency = 1000 * job.latency.total_seconds();
        perf_pts = perf_pts + perf_eval(latency, latency_low_threshold, latency_high_threshold);
        if latency < latency_low_threshold:
            quick_count = quick_count + 1;
            
    if not is_correct:
        print "Grade: 0 of 15 points";
    else:
        int_perf = int(BIG_QUESTION_PTS * min(1.0, perf_pts / total / .9));
        int_cost = int(BIG_QUESTION_PTS * min(1.0, (float(max(0.0, cpu_seconds - cpu_baseline)) / (cpu_redline - cpu_baseline)) * NO_ELASTIC_DEDUCTION));  
        score = max(0, CORRECTNESS_PTS + int_perf - int_cost);

        print "----------------------------------------------------------------"
        print "Grade: %d of 15 points" % score;
        print "         + 3 points for correctness"
        print "         + %d points for perf" % int_perf;
        print "         - %d points for worker usage" % int_cost;
        print ""
        print "         %.1f%% requests met the %d ms latency requirement" % (100.0 * quick_count / total, latency_low_threshold);
        print "----------------------------------------------------------------"
        
    print ""
    print "Grading Details:"
    print "  Perf:  * Summary: you get full perf points if 90% of your responses have"
    print "           latency under %d ms" % latency_low_threshold;
    print "         * You get one credit per response under %d ms. Partial credit is assigned" % latency_low_threshold;
    print "           with linear falloff to no credit at %d ms latency." % latency_high_threshold;
    print "         * Perf points are: %d * (num_credits / total_requests) / 0.9" % BIG_QUESTION_PTS;
    print ""
    print "  Usage: * No resource penalty up to %d CPU-seconds." % cpu_baseline;
    print "         * Linear falloff to minus 75%% points at %d sec" % cpu_redline;
    print ""    
        
        
def grade_nonuniform2(is_correct, trace_jobs, cpu_seconds):

    latency_low_threshold = 2000;
    latency_high_threshold = 4000;
    cpu_baseline = 115
    cpu_redline = 325;

    perf_pts = 0.0;
    quick_count = total = 0;

    for job in trace_jobs:
        if job.descr['work'] == "cmd=lastrequest":
            continue;
        total = total+1;
        latency = 1000 * job.latency.total_seconds();
        perf_pts = perf_pts + perf_eval(latency, latency_low_threshold, latency_high_threshold);
        if latency < latency_low_threshold:
            quick_count = quick_count + 1;
            
    if not is_correct:
        print "Grade: 0 of 13 points";
    else:
        int_perf = int(QUESTION_PTS * min(1.0, perf_pts / total / .9));
        int_cost = int(QUESTION_PTS * min(1.0, (float(max(0.0, cpu_seconds - cpu_baseline)) / (cpu_redline - cpu_baseline)) * NO_ELASTIC_DEDUCTION));  
        score = max(0, CORRECTNESS_PTS + int_perf - int_cost);

        print "----------------------------------------------------------------"
        print "Grade: %d of 13 points" % score;
        print "         + 3 points for correctness"
        print "         + %d points for perf" % int_perf;
        print "         - %d points for worker usage" % int_cost;
        print ""
        print "         %.1f%% requests met the %d ms latency requirement" % (100.0 * quick_count / total, latency_low_threshold);
        print "----------------------------------------------------------------"
                
    print ""
    print "Grading Details:"
    print "  Perf:  * Summary: you get full perf points if 90% of your responses have"
    print "           latency under %d ms" % latency_low_threshold;
    print "         * You get one credit per response under %d ms. Partial credit is assigned" % latency_low_threshold;
    print "           with linear falloff to no credit at %d ms latency." % latency_high_threshold;
    print "         * Perf points are: %d * (num_credits / total_requests) / 0.9" % QUESTION_PTS;
    print ""
    print "  Usage: * No resource penalty up to %d CPU-seconds." % cpu_baseline;
    print "         * Linear falloff to minus 75%% points at %d sec" % cpu_redline;
    print ""    

        
def grade_nonuniform3(is_correct, trace_jobs, cpu_seconds):

    latency_low_threshold = 1700;
    latency_high_threshold = 2500;
    cpu_baseline = 95
    cpu_redline = 250

    perf_pts = 0.0;
    quick_count = total = 0;
    

    for job in trace_jobs:
        if job.descr['work'] == "cmd=lastrequest":
            continue;
        total = total+1;
        latency = 1000 * job.latency.total_seconds();
        perf_pts = perf_pts + perf_eval(latency, latency_low_threshold, latency_high_threshold);
        if latency < latency_low_threshold:
            quick_count = quick_count + 1;

    if not is_correct:
        print "Grade: 0 of 13 points";
    else:
        int_perf = int(QUESTION_PTS * min(1.0, perf_pts / total / .9));
        int_cost = int(QUESTION_PTS * min(1.0, (float(max(0.0, cpu_seconds - cpu_baseline)) / (cpu_redline - cpu_baseline)) * NO_ELASTIC_DEDUCTION));  
        score = max(0, CORRECTNESS_PTS + int_perf - int_cost);

        print "----------------------------------------------------------------"
        print "Grade: %d of 13 points" % score;
        print "         + 3 points for correctness"
        print "         + %d points for perf" % int_perf;
        print "         - %d points for worker usage" % int_cost;
        print ""
        print "         %.1f%% requests met the %d ms latency requirement" % (100.0 * quick_count / total, latency_low_threshold);
        print "----------------------------------------------------------------"
                
    print ""
    print "Grading Details:"
    print "  Perf:  * Summary: you get full perf points if 90% of your responses have"
    print "           latency under %d ms" % latency_low_threshold;
    print "         * You get one credit per response under %d ms. Partial credit is assigned" % latency_low_threshold;
    print "           with linear falloff to no credit at %d ms latency." % latency_high_threshold;
    print "         * Perf points are: %d * (num_credits / total_requests) / 0.9" % QUESTION_PTS;
    print ""
    print "  Usage: * No resource penalty up to %d CPU-seconds." % cpu_baseline;
    print "         * Linear falloff to minus 75%% points at %d sec" % cpu_redline;
    print ""    

                
def grade_burst(is_correct, trace_jobs, cpu_seconds, finish_time):

    total_time_low = 28000;
    total_time_high = 60000;

    total_time = 1000 * finish_time;
    
    perf_score = 1.0 - min(1.0, max(0.0, float(total_time - total_time_low) / (total_time_high - total_time_low)));
    
    if not is_correct:
        print "Grade: 0 of 13 points";
    else:
        int_score = CORRECTNESS_PTS + int(QUESTION_PTS * perf_score);

        print "----------------------------------------------------------------"
        print "Grade: %d of 13 points" % int_score;
        print "----------------------------------------------------------------"
        
    print ""
    print "Grading Details:"
    print "  Goal:  * Get the burst completed as quickly as possible.  This test"
    print "           measures server throughput"
    print ""
    print "  Perf:  * 10 pts for completion in under %d sec" % (total_time_low / 1000);
    print "         * Linear falloff to 0 pts at %d sec" % (total_time_high / 1000);
    print ""
    print "  Usage: * There is no penality for usage"
    print ""

    
def grade_random(is_correct, trace_jobs, cpu_seconds, avg_latency):

    latency_low_threshold = 1000;
    latency_high_threshold = 2000;

    cpu_baseline = 185;
    cpu_redline = 260;
    
    slowness = max(0.0, avg_latency - latency_low_threshold);
    perf_score = 1.0 - min(1.0, (float(slowness) / (latency_high_threshold - latency_low_threshold)));
    cost_score = min(1.0, (float(max(0.0, (cpu_seconds - cpu_baseline))) / (cpu_redline - cpu_baseline)) * SMALL_NO_ELASTIC_DEDUCTION);
    
    if not is_correct:
        print "Grade: 0 of 13 points";
    else:
        int_perf = int(QUESTION_PTS * perf_score);
        int_cost = int(QUESTION_PTS * cost_score)
        score = max(0, CORRECTNESS_PTS + int_perf - int_cost);

        print "----------------------------------------------------------------"
        print "Grade: %d of 13 points" % score;
        print "         + 3 points for correctness"
        print "         + %d points for perf" % int_perf;
        print "         - %d points for worker usage" % int_cost;
        print "----------------------------------------------------------------"
        
    print ""
    print "Grading Details:"
    print "  Goal:  * Keep average latency low while minimizing server use."
    print ""
    print "  Perf:  * 10 points for avg latency under %d ms." % latency_low_threshold;
    print "         * Linear falloff to 0 pts at %d ms latency." % latency_high_threshold;
    print ""
    print "  Usage: * No resource penalty up to %d CPU-seconds." % cpu_baseline;
    print "         * Linear falloff to minus 50%% points at %d sec" % cpu_redline;
    print ""    

        
def run_grader(name, is_correct, trace_jobs, cpu_seconds, avg_latency, finish_time):

    if name.find("grading_compareprimes.txt") != -1:
        grade_compareprimes(is_correct, trace_jobs, cpu_seconds);
    elif name.find("grading_nonuniform1.txt") != -1:
        grade_nonuniform1(is_correct, trace_jobs, cpu_seconds);
    elif name.find("grading_nonuniform2.txt") != -1:
        grade_nonuniform2(is_correct, trace_jobs, cpu_seconds);
    elif name.find("grading_nonuniform3.txt") != -1:
        grade_nonuniform3(is_correct, trace_jobs, cpu_seconds);
    elif name.find("grading_burst.txt") != -1:
        grade_burst(is_correct, trace_jobs, cpu_seconds, finish_time);
    elif name.find("grading_random.txt") != -1:
        grade_random(is_correct, trace_jobs, cpu_seconds, avg_latency);
    else:
        print "No grading harness for this test"
