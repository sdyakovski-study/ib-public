from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



from .apps import module_id
from .models import Indications
import models

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
CLASSCODE_1_EMPTY_LABEL = _('First classcode MUST be given')
CLASSCODE_OTHER_EMPTY_LABEL = _('unused')
COMBOBOX_EMPTY_LABEL = _('Select %s')
REQUIRED_SELECTION = _('Please make a selection')
REQUIRED_FIRST_CLASSCODE = _('You need to select at least the first classification')


'''
def get_queryset(valid_on=None, order_by='id', **kwargs):
	criteria = kwargs.pop('queryset_criteria', {}) 
	if kwargs.pop('with_valids', None):
		if not valid_on:
			valid_on = timezone.now().date()
		criteria['valid_thru__gte'] = valid_on
		criteria['valid_from__lte'] = valid_on
	model = getattr(models, kwargs.pop('model', None)) # ToDo - try-except

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
class IndicationsForm(forms.ModelForm):
	class Meta:
		model = Indications
		exclude = ['id', 'renewal_of', 'territory']

	def __init__(self, *args, **kwargs):
		valid_on = kwargs.pop('valid_on', timezone.now().date())
		super(IndicationsForm, self).__init__(*args, **kwargs)

		# setup the combo boxes
		for field, label in [('limits_id', _('Limits')), ('deductible_id', _('Deductible')),
							 ('risk_experience_id', _('Risk Experience')), ('sunset_id', _('Sunset'))]:
			list_field = self.fields[field]
			list_field.queryset = Indications.get_valid_queryset(field_name=field, valid_on=valid_on).order_by('id')
			list_field.empty_label = ('Select %s') % label
			list_field.error_messages = {'required': REQUIRED_SELECTION}
		classcodes_queryset = Indications.get_valid_queryset(field_name='classcode1_id', valid_on=valid_on).order_by('code')
		for i in range(1,9):
			list_field = self.fields['classcode%d_id'% i]
			list_field.queryset = classcodes_queryset
			list_field.empty_label = (i==1) and _('First classcode MUST be given') or _('unused')
			list_field.label = ''
			list_field.required = (i==1) and True or False
			list_field.error_messages = {'required': (i==1) and _('You need to select at least the first classification') or ''}

		# lables
		self.fields['named'].label = _('Named Insured')
		self.fields['tzipcode'].label = _('Risk Location Zipcode')
		self.fields['limits_id'].label = _('Limits')
		self.fields['deductible_id'].label = _('Deductible (per occurence)')
		self.fields['risk_experience_id'].label = _('Risk Experience')
		self.fields['sunset_id'].label = _('Sunset Provision')
		self.fields['subcost'].label = _('Subcontracted Cost')
		self.fields['service_repair'].label = _('100% service/repair and/or 100% Commercial Risk')
		self.fields['prior_works_buyback'].label = _('Optional Prior Works Buyback - '
			'(If the insured\'s current policy does not exclude Prior Works you can remove the ' 
			'Prior Completed Operations Exclusion from the InterHannover Policy.)')
		self.fields['terrorism'].label = _('Optional Terrorism Coverage')
		self.fields['agg_lim_endmt'].label = _('Per Project Aggregate Limit Endorsement')
		self.fields['absolute_limits_buyback'].label = _('Optional Absolute Limits of '
			'Liability Buyback')
		self.fields['blanket_ai_comp_ops_endmt'].label = _('Optional Blanket Additional Insured ' 
			'with Completed Operations (excluding Residential) Endorsement')

		# help_texts
		self.fields['tzipcode'].help_text = _('The zipcode of the Risk Location is used to '
			'determine the correct territory.')
		self.fields['sales'].help_text = _('Input the total sales/receipts.')
		self.fields['subcost'].help_text = _('Input the total subcontracted cost.')
		self.fields['blanket_ai_comp_ops_endmt'].help_text = _('Note: Subject to underwriter\'s review and approval. '
			'Please contact your underwriter if your need an Endorsement for Residential exposure.')

		# error_messages

		# validators

		# widgets
		self.fields['service_repair'].widget = forms.RadioSelect(choices=BOOL_CHOICES)
		self.fields['prior_works_buyback'].widget = forms.RadioSelect(
			choices=((True, _('Yes, Remove the "Prior Completed Operations Exclusion HGL 1015 0912".')),
					 (False, _('No.')))
		)
		self.fields['terrorism'].widget = forms.RadioSelect(
			choices=((True, _('Yes, add Terrorism coverage.')),
					 (False, _('No, don\'t add Terrorism coverage.')))
		)
		self.fields['agg_lim_endmt'].widget = forms.RadioSelect(
			choices=((True, _('Yes, use Endorsement CG 25 03 for additional $250 (fully earned).')),
					 (False, _('No.')))
		)
		self.fields['absolute_limits_buyback'].widget = forms.RadioSelect(
			choices=((True, _('Yes, Remove the "Absolute Limits of Liability Endorsement HGL 1006 0912".')),
					 (False, _('No.')))
		)
		self.fields['blanket_ai_comp_ops_endmt'].widget = forms.RadioSelect(
			choices=((True, _('Yes, add Endorsement for additional $250 (fully earned).')),
					 (False, _('No.')))
		)
