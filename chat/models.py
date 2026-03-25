from django.db import models

class ChatLog(models.Model):
    chat_log_id = models.AutoField(primary_key=True, db_column='CHAT_LOG_ID')
    user_id     = models.IntegerField(db_column='USER_ID')
    context     = models.TextField(db_column='CONTEXT')

    class Meta:
        db_table = 'CHAT_LOG'
        managed = False
