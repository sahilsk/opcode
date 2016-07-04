from boto.ec2.cloudwatch.alarm import MetricAlarm
import boto.sqs, boto.ec2
import time, sys, traceback
from datetime import datetime

""" Attach alarm to all sqs list

"""
def print_queue(conn, sqs_list):
    num_queues = len(sqs_list);
    current_queue_count = 0;
    success_queue = []
    failed_queues = [];
    
    output_filename = "csv_%d.csv" % time.time()
    f = open( output_filename, "w", 0)
    
    print "Generating list (%s)" % output_filename
    
    head_str =  "Queue Name, Created Timestamp, Last Modified Timestamp"
    f.write( head_str + "\n")
    for q in sqs_list:
        current_queue_count += 1
    	print "------------ {current}/{total}) {queue}".format(total=num_queues, current=current_queue_count, queue=q.name)
    	try:
            print "%s" %(q.name, )
            q_attr = conn.get_queue_attributes(q)
            created_at = datetime.fromtimestamp(float( q_attr['CreatedTimestamp'] ))
            last_mod = datetime.fromtimestamp( float(q_attr['LastModifiedTimestamp'] ) )
            q_str = "%s, %s, %s" %(q.name,  created_at , last_mod)
            f.write(q_str + "\n")
            success_queue.append(q)
            time.sleep(2)
        except:
            failed_queues.append(q);
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60    
            
            
    f.close();      
    print "xxxxxxxxxxxxxxxxx  Finished"
    print "Find output file : %s" % output_filename

    if len(failed_queues) > 0:
        print "################# Failed queue list #########"
        for fq  in failed_queues:
            print fq.name
            
            
""" Calling main

"""
def start_exporting():
   sqs_conn = boto.sqs.connect_to_region( 'ap-southeast-1')
   sqs_queue_list = sqs_conn.get_all_queues()
   num_queues = len(sqs_queue_list)
   print "############## Total queues found: {total} ".format( total=num_queues)
   print_queue(sqs_conn, sqs_queue_list )

if __name__ == "__main__":
    start_exporting()