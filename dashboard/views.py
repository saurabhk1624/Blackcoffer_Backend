import json
from django.http import JsonResponse
from django.shortcuts import render
from dashboard.functions import format_date,valid_year,valid_integer,Round
from dashboard.models import AnalyticsData, DropDown, StatusNum
from django.db.models import Count, Q,Avg,F,CharField
from django.db.models.functions import Cast


def import_data(request):
    with open("jsondata.json", "r") as file:
        data = json.load(file)
        sheet = data.get("data")
        if sheet is None:
            return JsonResponse(
                {"msg": "Invalid request type!"}, status=400
            )
        for i in sheet:
            sector=i.get('sector').strip().upper()
            topic=i.get('topic').strip().upper()
            region=i.get('region').strip().upper()
            country=i.get('country').strip().upper()
            pestle=i.get('pestle').strip()
            source=i.get('source').strip()
            intensity=valid_integer(i.get('intensity'))
            likelihood=valid_integer(i.get('likelihood'))
            relevance=valid_integer(i.get('relevance'))
            sector_parent=DropDown.objects.filter(value='SECTOR').exclude(status=StatusNum.DELETE).first()
            if sector_parent is None:
                sector_parent=DropDown.objects.create(value='SECTOR')
            topic_parent=DropDown.objects.filter(value='TOPIC').exclude(status=StatusNum.DELETE).first()
            if topic_parent is None:
                topic_parent=DropDown.objects.create(value='TOPIC')
            region_parent=DropDown.objects.filter(value='REGION').exclude(status=StatusNum.DELETE).first()
            if region_parent is None:
                region_parent=DropDown.objects.create(value='REGION')
            country_parent=DropDown.objects.filter(value='COUNTRY').exclude(status=StatusNum.DELETE).first()
            if country_parent is None:
                country_parent=DropDown.objects.create(value='COUNTRY')
            pestle_parent=DropDown.objects.filter(value='PESTLE').exclude(status=StatusNum.DELETE).first()    
            if pestle_parent is None:
                pestle_parent=DropDown.objects.create(value='PESTLE')
            source_parent=DropDown.objects.filter(value='SOURCE').exclude(status=StatusNum.DELETE).first()    
            if source_parent is None:
                source_parent=DropDown.objects.create(value='SOURCE')
            published=format_date(i.get('published').strip()) if i.get('published').strip() is not None else None
            added=format_date(i.get('added').strip()) if i.get('added').strip() is not None else None
            print(published,added,"test")
            start_year=valid_year(i.get('start_year'))
            end_year=valid_year(i.get('end_year'))
            sector_value=DropDown.objects.filter(value=sector,pid__value='SECTOR').exclude(status=StatusNum.DELETE).first()
            if sector_value is None:
                sector_value=DropDown.objects.create(value=sector,pid=sector_parent)
            topic_value=DropDown.objects.filter(value=topic,pid__value='TOPIC').exclude(status=StatusNum.DELETE).first()
            if topic_value is None:
                topic_value=DropDown.objects.create(value=topic,pid=topic_parent)
            region_value=DropDown.objects.filter(value=region,pid__value='REGION').exclude(status=StatusNum.DELETE).first()
            if region_value is None:
                region_value=DropDown.objects.create(value=region,pid=region_parent)
            country_value=DropDown.objects.filter(value=country,pid__value='COUNTRY').exclude(status=StatusNum.DELETE).first()
            if country_value is None:
                country_value=DropDown.objects.create(value=country,pid=country_parent)
            pestle_value=DropDown.objects.filter(value=pestle,pid__value='PESTLE').exclude(status=StatusNum.DELETE).first()
            if pestle_value is None:
                pestle_value=DropDown.objects.create(value=pestle,pid=pestle_parent)
            source_value=DropDown.objects.filter(value=source,pid__value='SOURCE').exclude(status=StatusNum.DELETE).first()
            if source_value is None:
                source_value=DropDown.objects.create(value=source,pid=source_parent)
            AnalyticsData.objects.create(start_year=start_year,end_year=end_year,intensity=intensity,sector=sector_value,topic=topic_value,insight=i.get('insight'),url=i.get('url'),region=region_value,added=added,published=published,country=country_value,relevance=relevance,pestle=pestle_value,source=source_value,title=i.get('title'),likelihood=likelihood)
        
        return JsonResponse({'msg':'Data Imported Successfully'},status=200)


def dashboard_statistics(request):
    if request.method=='GET':
        request_type=request.GET.get('request_type')
        if request_type is None:
            return JsonResponse({'msg':'Invalid Format'},status=400)
        status=200
        if request_type=='country_statistics':
            data = list(
                    AnalyticsData.objects
                    .exclude(status=StatusNum.DELETE)
                    .exclude(Q(country__value__isnull=True) | Q(country__value=''))
                    .values("country__value")
                    .annotate(count=Count("country"))
                    .order_by("-count")[:5]
                )
        elif request_type=='sector_statistics':
            data = list(
                    AnalyticsData.objects
                    .exclude(status=StatusNum.DELETE)
                    .exclude(Q(sector__value__isnull=True) | Q(sector__value=''))
                    .values("sector__value")
                    .annotate(count=Count("sector"))
                    .order_by("-count")[:7]
                )
        elif request_type=='region_statistics':
            data = list(
                    AnalyticsData.objects
                    .exclude(status=StatusNum.DELETE)
                    .exclude(Q(region__value__isnull=True) | Q(region__value=''))
                    .values("region__value")
                    .annotate(count=Count("region"))
                    .order_by("-count")[:7]
                )
        elif request_type=='average_statistics':
            data = (
                    AnalyticsData.objects
                    .exclude(status=StatusNum.DELETE)
                    .aggregate(
                        total_data=Count("*"),
                        avg_likelihood=Round(Avg("likelihood", filter=~Q(likelihood__isnull=True)),2),
                        avg_relevance=Round(Avg("relevance", filter=~Q(relevance__isnull=True)),2),
                        avg_intensity=Round(Avg("intensity", filter=~Q(intensity__isnull=True)),2)
                        )
                    )
        elif request_type=='overall_data':
           data = list(
                AnalyticsData.objects
                .exclude(status=StatusNum.DELETE)
                .annotate(
                    added_date=Cast(F("added"), CharField()),
                    published_date=Cast(F("published"), CharField())
                )
                .values(
                    'start_year', 'end_year', 'intensity', 'sector__value', 'topic__value',
                    'insight', 'url', 'region__value', 'added_date', 'published_date',
                    'country__value', 'relevance', 'pestle__value', 'source__value',
                    'title', 'likelihood'
                )
            )
        else:
            data="Invalid return type"
            status=400
        return JsonResponse({'msg':data},status=status)
