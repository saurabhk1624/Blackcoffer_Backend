from django.db import models
from enum import IntEnum

class StatusNum(IntEnum):
    DELETE=0
    INSERT=1
    UPDATE=2


class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=StatusNum.INSERT)

    class Meta:
        abstract = True




class DropDown(BaseModel):
    pid=models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,related_name="dropdown_parent",)
    value=models.CharField(max_length=300)



class AnalyticsData(BaseModel):
    start_year=models.IntegerField(null=True)
    end_year=models.IntegerField(null=True)
    intensity=models.IntegerField(null=True)
    sector=models.ForeignKey(DropDown,on_delete=models.SET_NULL,null=True,related_name="sector_dropdown")
    topic=models.ForeignKey(DropDown,on_delete=models.SET_NULL,null=True,related_name="topic_dropdown")
    insight=models.TextField(null=True)
    url=models.URLField(max_length=500,null=True)
    region=models.ForeignKey(DropDown,on_delete=models.SET_NULL,null=True,related_name="region_dropdown")
    added=models.DateTimeField(null=True)
    published=models.DateTimeField(null=True)
    country=models.ForeignKey(DropDown,on_delete=models.SET_NULL,null=True,related_name="country_dropdown")
    relevance=models.IntegerField(null=True)
    pestle=models.ForeignKey(DropDown,on_delete=models.SET_NULL,null=True,related_name="pestle_dropdown")
    source=models.ForeignKey(DropDown,on_delete=models.SET_NULL,null=True,related_name="source_dropdown")
    title=models.TextField(null=True)
    likelihood=models.IntegerField(null=True)

