from celery import shared_task

from .services import assign_task_to_bot, find_bot_with_least_number_of_tasks


@shared_task
def assign_task_to_bot_with_least_number_of_tasks(task_id: int):
   bot_id = find_bot_with_least_number_of_tasks()
   assign_task_to_bot(task_id, bot_id)
