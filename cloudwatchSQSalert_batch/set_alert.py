from boto.ec2.cloudwatch.alarm import MetricAlarm
import boto.sqs, boto.ec2
import time, sys, traceback, copy



""" Create or update alarm on given queue

"""
def attach_cloudwatch_alert(queue_name):
    cloudwatch_conn = boto.ec2.cloudwatch.connect_to_region('ap-southeast-1')
    topicarnToSendNotification = "arn:aws:sns:ap-southeast-1::Cloudwatch_Notification"
    metric_name_str = "ApproximateNumberOfMessagesVisible"

    alarmName = queue_name + "-" + metric_name_str
    print "\t Setting alarm with name '%s'"% alarmName
    queueLenAlarm = MetricAlarm(
				    name= alarmName,
				    description= alarmName,
					connection = cloudwatch_conn,
					namespace = 'AWS/SQS',
					dimensions= dict(QueueName = queue_name),
					metric = metric_name_str,
					comparison = '>=',
					threshold = 1000,
				    period = 300,
				    evaluation_periods = 2,
				    alarm_actions= [topicarnToSendNotification],
				    statistic="Maximum"
					);
    cloudwatch_conn.create_alarm( queueLenAlarm);
    print "\t Alarm set successfully : %s" % queueLenAlarm.name


""" Attach alarm to all sqs list

"""

def attach_alarms(sqs_list):
    num_queues = len(sqs_list);
    current_queue_count = 0;
    success_queue = []
    failed_queues = [];

    for q in sqs_list:
        current_queue_count += 1
    	print "------------ {current}/{total}) Attaching alert to {queue}".format(total=num_queues, current=current_queue_count, queue=q.name)
    	try:
            attach_cloudwatch_alert(q.name)
            success_queue.append(q)
            time.sleep(2)
        except:
            failed_queues.append(q);
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60

    print "Xxxxxxxxxxxxxxxxx  Finished creating  alarms"
    print "\t Successful alarms: %d" % len(success_queue)
    print "\t Failed Alarms: %d" % len(failed_queues)

    if len(failed_queues) > 0:
        print "################# Failed queue list #########"
        for fq  in failed_queues:
            print fq.name


""" Entrypoint function to create alarms

"""

def start_main():
    sqs_queue_list = boto.sqs.connect_to_region( 'ap-southeast-1').get_all_queues();
    num_queues = len(sqs_queue_list)
    print "############## Total queues found: {total} ".format( total=num_queues)
    print "It's going to create %d alarms. You have 10 seconds to stop it." % num_queues
    time.sleep(10)

    attach_alarms(sqs_queue_list );


if __name__ == "__main__":
    start_main()
