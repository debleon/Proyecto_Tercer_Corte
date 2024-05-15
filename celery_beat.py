from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'gestion_de_nomina'

    def ready(self):
        self.setup_periodic_tasks()

    def setup_periodic_tasks(self):
        schedule, created = CrontabSchedule.objects.get_or_create(hour=18, minute=0)
        
        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Pagar Nóminas Diarias',
            task='gestion_de_nomina.tasks.pagar_nominas',
            defaults={'args': json.dumps([])}
        )
