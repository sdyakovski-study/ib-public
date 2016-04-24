from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .apps import module_id
from .forms import IndicationsForm
from .models import RateLimits, Indications

#temporary structure
indi = {
	'id':1234,
	'limits': '1000/2000/1000'
}
# Create your views here.
def index(request):
	programs = [
		{'module_id': 32, 'name': 'Hannover'},
		{'module_id': 18, 'name': 'AIX'},
	]
	return render(request, 'rater/index.html', {'programs': programs})

def effdate(request):
	return HttpResponse("Hello, world. You're at the rater effdate.")

def get_bindpkg(request):
	return HttpResponse("Hello, world. You're at the rater get_bindpkg.")

def rater(request, indi_id):
	list_limits = RateLimits.objects.filter(valid_thru__gte=timezone.now().date(),
		valid_from__lte=timezone.now().date(),
		module_id=module_id
	).order_by('id')
	return render(request, 'rater/rater.html', {'list_limits': list_limits, 'module_id': module_id, 'indi': indi})

def rate(request, indi_id):
	try:
		limit = RateLimits.objects.get(valid_thru__gte=timezone.now().date(),
			valid_from__lte=timezone.now().date(),
			id=request.POST['limit_id']
		)
	except KeyError, RateLimits.DoesNotExist:
		return render(request, 'rater/results.html', {
				"error_msg_limits": 'You did not provide a valid limit.', 'module_id': module_id, 'indi': indi
			})
	else:
		indi['limits'] = limit.descr
		return render(request, 'rater/results.html', {'limit': limit, 'module_id': module_id, 'indi': indi})

def indication_details(request, indi_id):
	return HttpResponse("Hello, world. You're at the rater indication_details.")

def indication_email(request, indi_id):
	return HttpResponse("Hello, world. You're at the rater indication_email.")

def indication_view(request, indi_id):
	return HttpResponse("Hello, world. You're at the rater indication_view.")

def appdata(request, indi_id, app_id):
	return HttpResponse("Hello, world. You're at the rater indication application appdata.")

def appdata_verify(request, indi_id, app_id):
	return HttpResponse("Hello, world. You're at the rater indication application appdata_verify.")

def appdata_view(request, indi_id, app_id):
	return HttpResponse("Hello, world. You're at the rater indication application appdata_view.")

def appdata_submit(request, indi_id, app_id):
	return HttpResponse("Hello, world. You're at the rater indication application appdata_submit.")



def indication(request, indi_id, valid_on=timezone.now().date()):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IndicationsForm(request.POST, valid_on=valid_on)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # create a model object by calling form.save
            indi = form.save(commit=False)
            indi.prod_id = 400
            indi.username = 'sdyakovski'
            indi.limits = form.cleaned_data['limits_id'].descr
            indi.deductible = form.cleaned_data['deductible_id'].descr
            indi.risk_experience = form.cleaned_data['risk_experience_id'].descr
            indi.sunset = form.cleaned_data['sunset_id'].descr
            indi.save()
            # redirect to a new URL:
            return HttpResponseRedirect('details/')

    else:
    	if indi_id == '0':
    		form = IndicationsForm(valid_on=valid_on)
    	else:
    		form = IndicationsForm(instance=Indications.objects.get(id=indi_id), valid_on=valid_on)

    return render(request, 'rater/indication.html', {'form': form})

