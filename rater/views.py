from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .apps import module_id
from .forms import IndicationsForm
from .models import RateLimits, Indications, get_rates


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
			indi.territory_id = form.cleaned_data['territory_id']
			indi.territory = str(form.cleaned_data['territory_id'])
			indi.limits = str(form.cleaned_data['limits_id'])
			indi.deductible = str(form.cleaned_data['deductible_id'])
			indi.risk_experience = str(form.cleaned_data['risk_experience_id'])
			indi.sunset = str(form.cleaned_data['sunset_id'])
			indi.classcode1 = str(form.cleaned_data['classcode1_id'])
			if form.cleaned_data['classcode2_id']:
				indi.classcode2 = str(form.cleaned_data['classcode2_id'])
			if form.cleaned_data['classcode3_id']:
				indi.classcode3 = str(form.cleaned_data['classcode3_id'])
			if form.cleaned_data['classcode4_id']:
				indi.classcode4 = str(form.cleaned_data['classcode4_id'])
			if form.cleaned_data['classcode5_id']:
				indi.classcode5 = str(form.cleaned_data['classcode5_id'])
			if form.cleaned_data['classcode6_id']:
				indi.classcode6 = str(form.cleaned_data['classcode6_id'])
			if form.cleaned_data['classcode7_id']:
				indi.classcode7 = str(form.cleaned_data['classcode7_id'])
			if form.cleaned_data['classcode8_id']:
				indi.classcode8 = str(form.cleaned_data['classcode8_id'])

			#calculate the combined rate_factor over all the parameters
			deduct_factor = form.cleaned_data['deductible_id'].rate_factor
			sunset_factor = form.cleaned_data['sunset_id'].factor
			riskex_factor = form.cleaned_data['risk_experience_id'].factor
			serrep_factor = form.cleaned_data['service_repair'] and 0.75 or 1.0
			pw_bb_factor = form.cleaned_data['prior_works_buyback'] and 1.25 or 1.0
			al_bb_factor = form.cleaned_data['absolute_limits_buyback'] and 1.10 or 1.0
			#all_factors = deduct_factor * sunset_factor * riskex_factor * serrep_factor * pw_bb_factor * al_bb_factor

			premium=0.0
			min_premium=0.00

			print 'indi.limits_id.id %s' % indi.limits_id.id

			try:
				rates = get_rates(valid_on=valid_on, classcode=indi.classcode1_id.code, territory=int(indi.territory_id.code), limit1=indi.limits_id.id)
			except DoesNotExist:
				raise ValidationError(_('The rates are not setup for a risk with classcode %(classcode)s, '
										'territory %(territory)s and limits %(limit)s. Please contact us.'), 
									  code='nonexistent', 
									  params={'classcode': indi.classcode1_id.code,
							  				  'territory': int(indi.territory_id.code),
							  				  'limit': indi.limits_id})

			"""
			# first classcode
			cc1=getClasscodeData(classcode=indi['classcode1'],territory=territory['code'],limit=result['limit'],rateseffective=valid_on, payroll=indi.payroll1)
			result['premium1']=calculate_premium(cc1, deduct_factor, sunset_factor, riskex_factor, serrep_factor, pw_bb_factor, al_bb_factor)
			premium=result['premium1']

			min_premium = getMinimumPremium(result['limit'],result['sunset'])
			"""
			indi.save()
			# redirect to a new URL:
			return HttpResponseRedirect('details/')

	else:
		if indi_id == '0':
			form = IndicationsForm(valid_on=valid_on)
		else:
			form = IndicationsForm(instance=Indications.objects.get(id=indi_id), valid_on=valid_on)

	return render(request, 'rater/indication.html', {'form': form})




