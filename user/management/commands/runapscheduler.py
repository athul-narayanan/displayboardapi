from django.core.management.base import BaseCommand
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from user.models import User, UserSchedules
from django.utils import timezone
import requests


def update_nodemcu():
    """
        This job reads the schedules and update the node mcu periodically
    """
    print("this job update message in node mcu")
    # fetch all users who enabled node mcu
    users = User.objects.filter(ping_started=True)
    for user_data in users:
        message = ""
        print(user_data)
        now = timezone.now()
        # find all the current schedules of the user
        current_schedules = UserSchedules.objects.filter(user=user_data,start__lte=now, end__gte=now)
        if len(current_schedules) == 0:
            message = ""
        else:
            message = current_schedules[0].title

        try:
            message = message.replace(" ", "+")
            message = message.ljust(16, "+")
            name = user_data.firstname + "+" + user_data.lastname
            name = name.ljust(16,"+")
            
            # Call node MCU API and update the message
            url = f'http://10.8.4.100/updateMessage?message={message}&name={name}'
            print(url)
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                print("Node MCU updates")
            else:
                print("Failed to update node MCU")
        except Exception:
            print("Failed to update node MCU")

    
def delete_old_job_executions(max_age=604_800):
    """
        Deleted all old jobs on sunday midnight
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # Add the job to update node mcu
        scheduler.add_job(
            update_nodemcu,
            trigger=CronTrigger(second="*/5"),  # Job to update MCU runs in every 5 seconds
            id="update_nodemcu",  # unique id of the update_nodemcu job
            max_instances=1, # Run only one instance
            replace_existing=True,
        )

        # Add the job to remove old cron jobs

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="sun", hour="00", minute="00"
            ), # This job runs on every sunday night and remove the old cron jobs
            id="delete_old_cron_jobs",  # unique id of the update_nodemcu job
            max_instances=1, # Run only one instance
            replace_existing=True,
        )


        try:
            print("Starting the Schedular...")
            scheduler.start()
        except KeyboardInterrupt:
            print("Stopping the schedular...")
            scheduler.shutdown()
            print("Schedular stopped...")

            