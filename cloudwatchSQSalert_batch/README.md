Instructions
--------------

### Pre-requisite

- Install [boto](http://boto.readthedocs.org/en/latest/getting_started.html#installing-boto)
- Create `boto.cfg` file and set environment variable BOTO_CONFIG to point to it 

    	export BOTO_CONFIG=/Users/dragonaider/Envs/aws_env/xyzpr/cloudwatchalert_batch/boto.cfg

## Script: set_alarm.py

**Description**: Set cloud-watch alarm on all sqs queue with following params: threshold:1000,period: 300, evaluation_periods: 2, alarm_actions: "arn:aws:sns:ap-southeast-1::Cloudwatch_Notification"  .    

**Run**  

	python -u set_alert.py | tee run_log_timestamp.log


## Script: get_sqs_list.py

**Description**  Export csv containing list of aws sqs queues with creation and modified date   
**Run**

	python -u get_sqs_list.py | tee run_log_timestamp.log
