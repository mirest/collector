from django.db import models

from authentication.models import User
from utils.base_model import BaseModel


class House(BaseModel):

    house_name = models.CharField(db_index=True, max_length=255, unique=True)

    rate = models.FloatField(blank=True)

    owner_id = models.ForeignKey(User,unique=False,on_delete='CASCADE',)

    owner_id = models.ForeignKey(User,unique=False,on_delete='CASCADE',)    

    is_occupied = models.BooleanField(default=False)

    start_date = models.DateTimeField(blank=True,null=True)    

    def __str__(self):
        return self.house_name
