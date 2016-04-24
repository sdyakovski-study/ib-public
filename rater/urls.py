""" rater app urls

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from . import views

app_name = 'rater'

application_patterns = [
    url(r'^(?P<app_id>[0-9]+)/', include([
        # ex: /rater/indication/1234/application/6789/ or /rater/indication/1234/application/0/
        url(r'^$', views.appdata, name='appdata'),
        # ex: /rater/indication/1234/application/6789/verify
        url(r'^verify/$', views.appdata_verify, name='appdata_verify'),
        # ex: /rater/indication/1234/application/6789/view
        url(r'^view/$', views.appdata_view, name='appdata_view'),
        # ex: /rater/indication/1234/application/6789/subimt
        url(r'^subimt/$', views.appdata_submit, name='appdata_submit'),
    ])),
]

indication_patterns = [
    url(r'^(?P<indi_id>[0-9]+)/', include([
        # ex: /rater/indication/1234/ or /rater/indication/0/
        url(r'^$', views.indication, name='indication'),
        # ex: /rater/indication/1234/ or /rater/indication/0/
        url(r'^rater/$', views.rater, name='rater'),
        # ex: /rater/indication/1234/rate or /rater/indication/0/rate
        url(r'^rate/$', views.rate, name='rate'),
        # ex: /rater/indication/1234/details
        url(r'^details/$', views.indication_details, name='indication_details'),
        # ex: /rater/indication/1234/email
        url(r'^email/$', views.indication_email, name='indication_email'),
        # ex: /rater/indication/1234/view
        url(r'^view/$', views.indication_view, name='indication_view'), 
        # ex: /rater/indication/1234/application
        url(r'^application/', include(application_patterns)), 

    ]))
]
urlpatterns = [
	# ex: /rater/
    url(r'^$', views.index, name='index'),
    # ex: /rater/effdate/
    url(r'^effdate/$', views.effdate, name='effdate'),
    # ex: /rater/getbindpkg
    url(r'^getbindpkg/$', views.get_bindpkg, name='get_bindpkg'),
    # ex: /rater/indication/
    url(r'^indication/', include(indication_patterns)),
]