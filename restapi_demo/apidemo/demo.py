from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
print(current_site.domain)