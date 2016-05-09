from django import forms
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



from .apps import module_id
from .models import Indications, get_gl_territory_by_zipcode
import models

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
CLASSCODE_OTHER_EMPTY_LABEL = _('unused')
REQUIRED_SELECTION = _('Please make a selection')

SALES_MAX_LIMIT = 1500000
PAYROLL_TOTAL_MIN_LIMIT = 25000



'''
def get_queryset(valid_on=None, order_by='id', **kwargs):
	criteria = kwargs.pop('queryset_criteria', {}) 
	if kwargs.pop('with_valids', None):
		if not valid_on:
			valid_on = timezone.now().date()
		criteria['valid_thru__gte'] = valid_on
		criteria['valid_from__lte'] = valid_on
	model = getattr(models, kwargs.pop('model', None))

	return model.objects.filter(**criteria).order_by(order_by)

def get_choices(*args, **kwargs):
	model_objects = get_queryset(*args, **kwargs)
	return [(o.pk, o) for o in model_objects]
		
def validate_gt_0(value):
    if value == '0':
        raise ValidationError(
            _('Please make a selection')
        )
'''

class DivErrorList(ErrorList):
	def as_divs(self):
		if not self: return ''
		return '<div class="errorlist"><strong>%s</strong></div>' % ''.join(['<div class="error">%s</div>' % e for e in self])

	def __unicode__(self):
		return self.as_divs()

	def __str__(self):
		return self.__unicode__()



class IndicationsForm(forms.ModelForm):
	error_css_class = 'error'
	required_css_class = 'required'

	class Meta:
		model = Indications
		exclude = ['id', 'producer_added_fee', 'renewal_of', 'territory']

	def __init__(self, *args, **kwargs):
		self.valid_on = kwargs.pop('valid_on', timezone.now().date())
		kwargs['error_class']=DivErrorList
		super(IndicationsForm, self).__init__(*args, **kwargs)

		# setup the combo boxes
		for field, label in [('limits', _('Limits')),
							 ('deductible', _('Deductible')),
							 ('risk_experience', _('Risk Experience')),
							 ('sunset', _('Sunset'))]:
			list_field = self.fields[field]
			list_field.queryset = Indications.get_valid_queryset(
									field_name=field,
									valid_on=self.valid_on
								  ).order_by('id')
			list_field.empty_label = ('Select %s') % label
			list_field.error_messages = {'required': REQUIRED_SELECTION}
		classcodes_queryset = Indications.get_valid_queryset(
								field_name='classcode1',
								valid_on=self.valid_on
							  ).order_by('code')
		for i in range(1,9):
			list_field = self.fields['classcode%d' % i]
			list_field.queryset = classcodes_queryset
			list_field.empty_label = ((i==1) and 
				_('First classcode MUST be given') or _('unused'))
			list_field.label = ''
			list_field.required = ((i==1) and True or False)
			list_field.error_messages = {'required': ((i==1) and
				_('You need to select at least the first classification') or '')}

		# lables
		self.fields['named'].label = _('Named Insured')
		self.fields['tzipcode'].label = _('Risk Location Zipcode')
		self.fields['limits'].label = _('Limits')
		self.fields['deductible'].label = _('Deductible (per occurence)')
		self.fields['risk_experience'].label = _('Risk Experience')
		self.fields['sunset'].label = _('Sunset Provision')
		self.fields['subcost'].label = _('Subcontracted Cost')
		self.fields['service_repair'].label = _('100% service/repair and/or '
												'100% Commercial Risk')
		self.fields['worksplit_type_groundup'].label = _('New Construction')
		self.fields['worksplit_type_remodel'].label = _('Remodel')
		self.fields['worksplit_type_service'].label = _('Service & Repair')
		self.fields['worksplit_inst_commercial'].label = _('Commercial')
		self.fields['worksplit_inst_residential'].label = _('Residential')
		self.fields['worksplit_inst_industrial'].label = _('Industrial')
		self.fields['worksplit_inst_institutional'].label = _('Institutional')
		self.fields['number_owners'].label = _('Number of active owners/partners')
		self.fields['number_ft_employees'].label = _('Full Times')
		self.fields['number_pt_employees'].label = _('Part Times')
		self.fields['prior_works_buyback'].label = _('Optional Prior Works '
			'Buyback - (If the insured\'s current policy does not exclude '
			'Prior Works you can remove the Prior Completed Operations ' 
			'Exclusion from the InterHannover Policy.)')
		self.fields['terrorism'].label = _('Optional Terrorism Coverage')
		self.fields['agg_lim_endmt'].label = _('Per Project Aggregate Limit '
											   'Endorsement')
		self.fields['absolute_limits_buyback'].label = _('Optional Absolute '
			'Limits of Liability Buyback')
		self.fields['blanket_ai_comp_ops_endmt'].label = _('Optional Blanket '
			'Additional Insured with Completed Operations (excluding '
			'Residential) Endorsement')

		# help_texts
		self.fields['tzipcode'].help_text = _('The zipcode of the Risk Location '
			'is used to determine the correct territory.')
		self.fields['sales'].help_text = _('Input the total sales/receipts.')
		self.fields['subcost'].help_text = _('Input the total subcontracted '
											 'cost.')
		self.fields['number_owners'].help_text = _('Owners must be included '
			'below at a payroll amount of $25,000 each..')
		self.fields['prior_works_buyback'].help_text = _('If yes, please '
			'provide us with a copy of the insured\'s current declaration page.')
		self.fields['blanket_ai_comp_ops_endmt'].help_text = _('Note: Subject '
			'to underwriter\'s review and approval. Please contact your '
			'underwriter if your need an Endorsement for Residential exposure.')

		# error_messages
		self.fields['named'].error_messages = {'required': _('Please enter the '
															'Insured\'s name')}
		self.fields['tzipcode'].error_messages = {'required': _('You need to '
			'provide the zipcode of the risk location')}

		# validators

		# widgets
		self.fields['service_repair'].widget = forms.RadioSelect(choices=BOOL_CHOICES)
		self.fields['prior_works_buyback'].widget = forms.RadioSelect(
			choices=((True, _('Yes, Remove the "Prior Completed Operations '
							  'Exclusion HGL 1015 0912".')),
					 (False, _('No.')))
		)
		self.fields['terrorism'].widget = forms.RadioSelect(
			choices=((True, _('Yes, add Terrorism coverage.')),
					 (False, _('No, don\'t add Terrorism coverage.')))
		)
		self.fields['agg_lim_endmt'].widget = forms.RadioSelect(
			choices=((True, _('Yes, use Endorsement CG 25 03 for additional '
							  '$250 (fully earned).')),
					 (False, _('No.')))
		)
		self.fields['absolute_limits_buyback'].widget = forms.RadioSelect(
			choices=((True, _('Yes, Remove the "Absolute Limits of Liability '
							  'Endorsement HGL 1006 0912".')),
					 (False, _('No.')))
		)
		self.fields['blanket_ai_comp_ops_endmt'].widget = forms.RadioSelect(
			choices=((True, _('Yes, add Endorsement for additional $250 '
							  '(fully earned).')),
					 (False, _('No.')))
		)

	def clean_sales(self):
		sales = self.cleaned_data['sales']
		if sales > SALES_MAX_LIMIT:
			msg = _('Ineligible risk!!! Sales exceed $1,500,000. Please '
					'contact your underwriter.')
			raise forms.ValidationError(msg, code='sales_to_big')
		return sales

	def clean(self):
		super(IndicationsForm, self).clean()
		# Validate tzipcode - to be an existing zipcode and to be part of 
		# eligible gl_territory
		tzipcode = self.cleaned_data.get('tzipcode')
		if tzipcode:
			try:
				gl_territory_obj = get_gl_territory_by_zipcode(module_id,
										tzipcode,
										valid_on=self.valid_on)
			except ValidationError as e:
				self.add_error('tzipcode', e)
			else:
				self.cleaned_data['territory'] = gl_territory_obj

		# Validate the worksplit_types - they are percentages - must sum up to 100
		worksplit_types = ['worksplit_type_groundup',
						   'worksplit_type_remodel',
						   'worksplit_type_service']
		total_worksplit_types, do_this_validation = 0, True
		for wt in worksplit_types:
			# make sure the field made it so far in the validations
			if not self.cleaned_data.has_key(wt):
				do_this_validation = False
				break
			else:
				total_worksplit_types += self.cleaned_data.get(wt)
		
		if do_this_validation:
			if total_worksplit_types != 100:
				msg = _('These must sum up to 100')
				self.add_error('worksplit_type_groundup', msg)

		# Validate the worksplit_insts - they are percentages - must sum up to 100
		worksplit_insts = ['worksplit_inst_commercial',
						   'worksplit_inst_residential',
						   'worksplit_inst_industrial',
						   'worksplit_inst_institutional']
		total_worksplit_insts, do_this_validation = 0, True
		for wi in worksplit_insts:
			# make sure the field made it so far in the validations
			if not self.cleaned_data.has_key(wi):
				do_this_validation = False
				break
			else:
				total_worksplit_insts += self.cleaned_data.get(wi)
		if do_this_validation:
			if total_worksplit_insts != 100:
				msg = _('These must sum up to 100')
				self.add_error('worksplit_inst_commercial', msg)

		# Check for subcost - if entered to not be more than 50% of sales
		if (self.cleaned_data.has_key('sales') and
			self.cleaned_data.has_key('subcost')):

			sales, subcost = (self.cleaned_data.get('sales'),
							  self.cleaned_data.get('subcost'))
			if float(subcost) > float(sales)*0.5:
				msg = _('Ineligible risk!!! Subcosts exceed 50% of the Sales. '
						'Please contact your underwriter!')
				self.add_error('subcost', msg)

		# Check the classcode payrolls
		for i in range(1,9):
			self.validate_classcode_payroll_pair('classcode%d' % i,
												 'payroll%d' % i)

		# Check for payroll to be at least PAYROLL_TOTAL_MIN_LIMIT
		total_payroll = self.get_total_payroll()
		if total_payroll < PAYROLL_TOTAL_MIN_LIMIT:
			msg = _('The total payroll entered must be at least $25,000!')
			self.add_error('payroll1', msg)

		# Sales can not be below the total payroll
		if self.cleaned_data.has_key('sales'):
			if self.cleaned_data.get('sales') < total_payroll:
				msg = _('Sales can not be below the total payroll!')
				self.add_error('sales', msg)

		# Check if 91342 is there
		has_91342 = False
		for i in range(1,9):
			classcode = self.cleaned_data.get('classcode%d' % i)
			if classcode and classcode.code == '91342':
				has_91342 = True

		# Classcodes 94007 and 95410 are only available if 91342 is selected
		if not has_91342:
			for i in range(1,9):
				classcode = self.cleaned_data.get('classcode%d' % i)
				if classcode and classcode.code in ('94007','95410'):
					msg = _('Classcodes 94007 and 95410 are only available '
							'if 91342 is selected')
					self.add_error('classcode%d' % i, msg)

		# Check if service_repair is selected, but types of work do not support it.
		if self.cleaned_data.get('service_repair'):
		    if (self.cleaned_data.has_key('worksplit_type_groundup') and 
		    	self.cleaned_data.get('worksplit_type_groundup') > 0 and
		    	self.cleaned_data.has_key('worksplit_inst_commercial') and 
		    	self.cleaned_data.get('worksplit_inst_commercial') != 100):

		    	msg = _('Can not select %s - there is New Construction '
		    			'indicated and it is not 100%% '
		    			'Commercial!' % self.fields['service_repair'].label)
		    	self.add_error('service_repair', msg)

		# Check if Blanket AI Completed Operations (excl. Residential) is
		# selected, but 100% Residential work is indicated.
		if (self.cleaned_data.has_key('blanket_ai_comp_ops_endmt') and 
	    	self.cleaned_data.get('blanket_ai_comp_ops_endmt') and
	    	self.cleaned_data.has_key('worksplit_inst_residential') and 
	    	self.cleaned_data.get('worksplit_inst_residential') == 100):

			msg = _('Can not request the Blanket AI Completed Operations '
	    			'(Excl. Residential), because 100% Residential work has '
	    			'been indicated!')
			self.add_error('blanket_ai_comp_ops_endmt', msg)

		# Check if the payroll corresponds to the number of owners
		if self.cleaned_data.has_key('number_owners'):
			number_owners = self.cleaned_data.get('number_owners')
			if total_payroll < number_owners * PAYROLL_TOTAL_MIN_LIMIT:
				msg = _('The total payroll entered must be at least %d times '
                		'$25,000, since %d is the number of '
                		'owners' % (number_owners, number_owners))
				self.add_error('number_owners', msg)

	def validate_classcode_payroll_pair(self, classcode_field, payroll_field):
		if (self.cleaned_data.has_key(classcode_field) and 
			self.cleaned_data.has_key(payroll_field)):

			classcode, payroll = (self.cleaned_data.get(classcode_field),
									 self.cleaned_data.get(payroll_field))
			if classcode and not payroll:
				self.add_error(payroll_field,
							   ValidationError(_('You need to input the '
												 'payroll for this classcode!'),
											   code='incomplete_payroll'))
			if not classcode and payroll:
				self.add_error(classcode_field,
							   ValidationError(_('You need to choose a '
							   					 'classcode if there is a '
							   					 'payroll for it!'),
											   code='incomplete_classcode'))

	def get_total_payroll(self):
		total_payroll = 0
		for i in range(1,9):
			if self.cleaned_data.has_key('payroll%d' % i):
				total_payroll += self.cleaned_data.get('payroll%d' % i)
		return total_payroll




		
		