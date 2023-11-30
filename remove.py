from django.db.models import Count
from .models import Mymodel

def delete_duplicates():
    duplicates = (
        Mymodel.objects.values('caseid', 'name', 'lon', 'lat', 'datetime')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )

    for duplicate in duplicates:
        # Remove 'count' from the dictionary
        duplicate.pop('count')
        duplicate_ids = (
            CaseMountain.objects.filter(**duplicate)
            .values_list('id', flat=True)
        )
        # Keep the first one, delete the rest
        CaseMountain.objects.filter(id__in=duplicate_ids[1:]).delete()
