from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError
from django.utils import timezone

from .apps import module_id
from .forms import IndicationsForm
from .models import RateLimits, Indications, get_hangl_rates


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
			indi.date_effective = valid_on
			indi.territory = form.cleaned_data['territory']
			indi.territory_descr = str(form.cleaned_data['territory'])
			indi.limits_descr = str(form.cleaned_data['limits'])
			indi.deductible_descr = str(form.cleaned_data['deductible'])
			indi.risk_experience_descr = str(form.cleaned_data['risk_experience'])
			indi.sunset_descr = str(form.cleaned_data['sunset'])
			indi.classcode1_descr = str(form.cleaned_data['classcode1'])
			if form.cleaned_data['classcode2']:
				indi.classcode2_descr = str(form.cleaned_data['classcode2'])
			if form.cleaned_data['classcode3']:
				indi.classcode3_descr = str(form.cleaned_data['classcode3'])
			if form.cleaned_data['classcode4']:
				indi.classcode4_descr = str(form.cleaned_data['classcode4'])
			if form.cleaned_data['classcode5']:
				indi.classcode5_descr = str(form.cleaned_data['classcode5'])
			if form.cleaned_data['classcode6']:
				indi.classcode6_descr = str(form.cleaned_data['classcode6'])
			if form.cleaned_data['classcode7']:
				indi.classcode7_descr = str(form.cleaned_data['classcode7'])
			if form.cleaned_data['classcode8']:
				indi.classcode8_descr = str(form.cleaned_data['classcode8'])

			#calculate the combined rate_factor over all the parameters
			deduct_factor = float(form.cleaned_data['deductible'].rate_factor)
			riskex_factor = float(form.cleaned_data['risk_experience'].factor)
			sunset_factor = float(form.cleaned_data['sunset'].factor)
			serrep_factor = form.cleaned_data['service_repair'] and 0.75 or 1.0
			pw_bb_factor = form.cleaned_data['prior_works_buyback'] and 1.25 or 1.0
			al_bb_factor = form.cleaned_data['absolute_limits_buyback'] and 1.10 or 1.0
			#all_factors = deduct_factor * sunset_factor * riskex_factor * serrep_factor * pw_bb_factor * al_bb_factor

			premium=0.0
			min_premium=0.00

			# Get the classcode baserate and finalrate
			try:
				rates = get_hangl_rates(classcode=indi.classcode1, territory=indi.territory, limits=indi.limits, valid_on=valid_on)
			except ValidationError as e:
				raise Http404(e)
			baserate = float(rates.rate1)
			print 'rates.rate1 %s' % baserate
			finalrate = baserate * deduct_factor * sunset_factor * riskex_factor * serrep_factor * pw_bb_factor * al_bb_factor
			print 'finalrate %s' % finalrate
			# let's do the math
			premium = float(indi.payroll1/1000) * finalrate
			print 'premium %s' % premium
			indi.premium = premium


			"""
			# first classcode
			cc1=getClasscodeData(classcode=indi['classcode1'],territory=territory['code'],limit=result['limit'],rateseffective=valid_on, payroll=indi.payroll1)
			result['premium1']=calculate_premium(cc1, deduct_factor, sunset_factor, riskex_factor, serrep_factor, pw_bb_factor, al_bb_factor)
			premium=result['premium1']

			min_premium = getMinimumPremium(result['limit'],result['sunset'])
			"""
			indi.save()
			# redirect to a new URL:
			return render(request, 'rater/results.html', {'indi': indi})

	else:
		if indi_id == '0':
			form = IndicationsForm(valid_on=valid_on)
		else:
			form = IndicationsForm(instance=Indications.objects.get(id=indi_id), valid_on=valid_on)

	return render(request, 'rater/indication.html', {'form': form, 'indi_id': indi_id})




