# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import USZipCodeField

from .apps import module_id


class Carrier(models.Model):
    id = models.AutoField(primary_key=True)
    address_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    admitted = models.NullBooleanField()
    valid_from = models.DateField()
    valid_thru = models.DateField()

    class Meta:
        managed = False
        db_table = 'carrier'
        unique_together = (('id', 'valid_from'),)


class CarrierProgram(models.Model):
    id = models.AutoField(primary_key=True)
    carrier_id = models.IntegerField()
    contact_id = models.IntegerField(blank=True, null=True)
    inspection_company_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=127)
    commission = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    minimum_earned = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    inspection_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    policy_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    broker_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    processing_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    hold_inspection_fee = models.BooleanField()
    hold_policy_fee = models.BooleanField()
    hold_broker_fee = models.BooleanField()
    hold_stamping_fee = models.BooleanField()
    hold_processing_fee = models.BooleanField()
    hold_ciga_fee = models.BooleanField()
    hold_state_tax = models.BooleanField()
    requires_inspection = models.BooleanField()
    multiple_locations_rated = models.NullBooleanField()
    requires_renewal_inspection = models.NullBooleanField()
    reinspection_frequency = models.IntegerField(blank=True, null=True)
    file_digital = models.NullBooleanField()
    requires_rewrite_inspection = models.NullBooleanField()
    max_credit = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    max_debit = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    broker_fee_percent = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    processing_fee_percent = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    policy_fee_percent = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    inspection_fee_percent = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    print_invoice = models.NullBooleanField()
    valid_from = models.DateField()
    valid_thru = models.DateField()
    tax_inspection_fee = models.NullBooleanField()
    tax_policy_fee = models.NullBooleanField()
    tax_broker_fee = models.NullBooleanField()
    tax_processing_fee = models.NullBooleanField()
    tax_other_fee = models.NullBooleanField()
    round_ciga_fee = models.NullBooleanField()
    round_state_tax = models.NullBooleanField()
    round_stamping_fee = models.NullBooleanField()
    state = models.CharField(max_length=2, blank=True, null=True)
    phys_inspection_company_id = models.IntegerField(blank=True, null=True)
    inspection_fee_fixed_is_minimum = models.NullBooleanField()
    inspection_fee_allow_override = models.NullBooleanField()
    round_inspection_fee = models.NullBooleanField()
    policy_fee_fixed_is_minimum = models.NullBooleanField()
    policy_fee_allow_override = models.NullBooleanField()
    round_policy_fee = models.NullBooleanField()
    broker_fee_allow_override = models.NullBooleanField()
    round_broker_fee = models.NullBooleanField()
    processing_fee_fixed_is_minimum = models.NullBooleanField()
    processing_fee_charge_on_ap = models.NullBooleanField()
    processing_fee_charge_min_on_ap = models.NullBooleanField()
    processing_fee_allow_override = models.NullBooleanField()
    round_processing_fee = models.NullBooleanField()
    round_premium = models.NullBooleanField()
    second_inspection_company_id = models.IntegerField(blank=True, null=True)
    second_inspection_company_load = models.IntegerField(blank=True, null=True)
    crn_ahead_days = models.IntegerField(blank=True, null=True)
    nrn_ahead_days = models.IntegerField(blank=True, null=True)
    inspection_received_days = models.IntegerField(blank=True, null=True)
    brokerage_only = models.NullBooleanField()
    brokerage_quoting_allowed = models.NullBooleanField()
    program_expiration = models.DateField(blank=True, null=True)
    enforce_min_earned_on_cancellation = models.NullBooleanField()
    use_manual_policy_number = models.NullBooleanField()
    use_sequential_policy_number = models.NullBooleanField()
    show_order = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrier_program'
        unique_together = (('id', 'valid_from'),)


class CarrierProgramTaxes(models.Model):
    id = models.AutoField(primary_key=True)
    carrier_program_id = models.IntegerField()
    stamping_fee = models.DecimalField(max_digits=20, decimal_places=3)
    ciga_fee = models.DecimalField(max_digits=20, decimal_places=3)
    state_tax = models.DecimalField(max_digits=20, decimal_places=3)
    valid_from = models.DateField()
    valid_thru = models.DateField()
    hold_stamping_fee = models.NullBooleanField()
    round_stamping_fee = models.NullBooleanField()
    hold_ciga_fee = models.NullBooleanField()
    round_ciga_fee = models.NullBooleanField()
    hold_state_tax = models.NullBooleanField()
    round_state_tax = models.NullBooleanField()
    flat_stamping_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    flat_state_tax = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    flat_ciga_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    apply_stamping_fee_on_ap = models.NullBooleanField()
    apply_stamping_fee_on_rp = models.NullBooleanField()
    apply_state_tax_on_ap = models.NullBooleanField()
    apply_state_tax_on_rp = models.NullBooleanField()
    apply_ciga_fee_on_ap = models.NullBooleanField()
    apply_ciga_fee_on_rp = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'carrier_program_taxes'
        unique_together = (('id', 'valid_from'),)


class Coverage(models.Model):
    id = models.AutoField(primary_key=True)
    program_id = models.IntegerField()
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=25, blank=True, null=True)
    descr = models.CharField(max_length=255, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=20, decimal_places=3)
    module_id = models.IntegerField()
    coverage_type = models.CharField(max_length=1)
    is_addable = models.NullBooleanField()
    is_prorateable = models.NullBooleanField()
    valid_from = models.DateField()
    valid_thru = models.DateField()

    class Meta:
        managed = False
        db_table = 'coverage'
        unique_together = (('id', 'valid_from'),)


class CpBrokerFee(models.Model):
    id = models.AutoField(primary_key=True)
    program_id = models.IntegerField()
    broker_fee = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    premium_min = models.DecimalField(max_digits=20, decimal_places=3)
    premium_max = models.DecimalField(max_digits=20, decimal_places=3)
    valid_from = models.DateField()
    valid_thru = models.DateField()

    class Meta:
        managed = False
        db_table = 'cp_broker_fee'
        unique_together = (('id', 'valid_from'),)


class FiZipcodes(models.Model):
    zipcodeid = models.AutoField(primary_key=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    code_type = models.CharField(max_length=1, blank=True, null=True)
    gl_territory = models.CharField(max_length=3, blank=True, null=True)
    territory_bop = models.CharField(max_length=3, blank=True, null=True)
    protection_class = models.CharField(max_length=2, blank=True, null=True)
    territory_bop_liab_terrorism = models.SmallIntegerField(blank=True, null=True)
    territory_bop_prop_terrorism = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fi_zipcodes'

    def __unicode__(self):
        return '%s, %s, %s, %s, %s, %s' % (self.zipcode, self.city,	self.county, self.state,
        	self.gl_territory, self.territory_bop)

    def __str__(self):
        return self.__unicode__()

class IbModules(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ib_modules'

class IntegerRangeField(models.IntegerField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, **kwargs)

    def formfield(self, **kwargs):
        # Passing localize=True in order to force the FormField in the ModelForm to have widget=TextInput.
        # Without it, the FormField uses NumberInput and accepts Real numbers. They throw a
        # Validation Error here, but it is inconsistent with the other validation errors that occur
        # on Form Validation level and use the validators and error_messages defined there.
        # Alternatively, I will have to define the widget here (presentation in the Model?!?),
        # and also import forms.TextInput widget - bad.
        defaults = {'min_value': self.min_value, 'max_value': self.max_value, 'localize': True}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class PositiveDecimalField(models.DecimalField):
    def __init__(self, min_value=None, **kwargs):
        self.min_value = min_value
        models.DecimalField.__init__(self, **kwargs)

    def formfield(self, **kwargs):
        # Passing localize=True in order to force the FormField in the ModelForm to have widget=TextInput.
        # Without it, the FormField uses NumberInput and accepts Real numbers. They throw a
        # Validation Error here, but it is inconsistent with the other validation errors that occur
        # on Form Validation level and use the validators and error_messages defined there.
        # Alternatively, I will have to define the widget here (presentation in the Model?!?),
        # and also import forms.TextInput widget - bad.
        defaults = {'min_value': self.min_value, 'localize': True}
        defaults.update(kwargs)
        return super(PositiveDecimalField, self).formfield(**defaults)


class WIthValidsForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['on_delete'] = models.DO_NOTHING
        kwargs['related_name'] = '+'
        super(WIthValidsForeignKey, self).__init__(*args, **kwargs)

    def get_queryset_settings(self):
        return {
            'model': self.rel.to.__name__,
            'with_valids': True,
            'queryset_criteria': self.get_limit_choices_to(),
        }


class Indications(models.Model):
    # blank=False, null=False,  are there by default. I include blank and null only where they are True
    valid_on = timezone.now().date()
    id = models.AutoField(primary_key=True)
    prod_id = models.IntegerField(editable=False)
    username = models.CharField(max_length=32, editable=False)
    # the next one is being handled on the database level.
    #date_indicated = models.DateTimeField(blank=True, null=True, editable=False)
    printed = models.NullBooleanField(default=False, editable=False)
    date_effective = models.DateField(editable=False)

    named = models.CharField(max_length=255)
    dba = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True, default='CA')
    zipcode = USZipCodeField(max_length=10, blank=True, null=True)

    premium = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
    min_premium = models.BooleanField(editable=False)
    producer_added_fee = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    renewal_of = models.CharField(max_length=32, blank=True, null=True, editable=False)

    tzipcode = USZipCodeField(max_length=10,)
    territory = WIthValidsForeignKey('RateTerritories',
        db_column='territory_id',
        limit_choices_to={'module_id': module_id}
    )
    territory_descr = models.CharField(max_length=255, editable=False)
    limits = WIthValidsForeignKey('RateLimits',
        db_column='limits_id',
        limit_choices_to={'module_id': module_id}
    )
    limits_descr = models.CharField(max_length=255, editable=False)
    deductible = WIthValidsForeignKey('RateDeductibles',
        db_column='deductible_id',
        limit_choices_to={'module_id': module_id}
    )
    deductible_descr = models.CharField(max_length=255, editable=False)
    risk_experience = WIthValidsForeignKey('RateFactors',
        db_column='risk_experience_id',
        limit_choices_to={'module_id': module_id, 'parameter_set': 'risk_experience'}
    )
    risk_experience_descr = models.CharField(max_length=255, editable=False)
    sunset = WIthValidsForeignKey('RateFactors',
        db_column='sunset_id',
        limit_choices_to={'module_id': module_id, 'parameter_set': 'sunset'}
    )
    sunset_descr = models.CharField(max_length=255, editable=False)

    sales = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    subcost = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)

    service_repair = models.BooleanField(default=False)

    worksplit_type_groundup = IntegerRangeField(min_value=0, max_value=100, default=0)
    worksplit_type_remodel = IntegerRangeField(min_value=0, max_value=100, default=0)
    worksplit_type_service = IntegerRangeField(min_value=0, max_value=100, default=0)
    worksplit_inst_commercial = IntegerRangeField(min_value=0, max_value=100, default=0)
    worksplit_inst_residential = IntegerRangeField(min_value=0, max_value=100, default=0)
    worksplit_inst_industrial = IntegerRangeField(min_value=0, max_value=100, default=0)
    worksplit_inst_institutional = IntegerRangeField(min_value=0, max_value=100, default=0)

    number_owners = IntegerRangeField(min_value=0, default=0)
    number_ft_employees = IntegerRangeField(min_value=0, default=0)
    number_pt_employees = IntegerRangeField(min_value=0, default=0)

    classcode1 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode1_id',
        limit_choices_to={'module_id': module_id})
    classcode1_descr = models.CharField(max_length=255, editable=False)
    payroll1 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode2 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode2_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode2_descr = models.CharField(max_length=255, editable=False)
    payroll2 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode3 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode3_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode3_descr = models.CharField(max_length=255, editable=False)
    payroll3 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode4 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode4_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode4_descr = models.CharField(max_length=255, editable=False)
    payroll4 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode5 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode5_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode5_descr = models.CharField(max_length=255, editable=False)
    payroll5 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode6 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode6_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode6_descr = models.CharField(max_length=255, editable=False)
    payroll6 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode7 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode7_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode7_descr = models.CharField(max_length=255, editable=False)
    payroll7 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)
    classcode8 = WIthValidsForeignKey('RateClasscodes',
        db_column='classcode8_id',
        limit_choices_to={'module_id': module_id},
        default=0
    )
    classcode8_descr = models.CharField(max_length=255, editable=False)
    payroll8 = PositiveDecimalField(min_value=0, max_digits=20, decimal_places=2, default=0)

    prior_works_buyback = models.BooleanField(default=False)
    terrorism = models.BooleanField(default=False)
    agg_lim_endmt = models.BooleanField(default=False)
    absolute_limits_buyback = models.BooleanField(default=False)
    blanket_ai_comp_ops_endmt = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'indications_hangl'

    @classmethod
    def get_valid_queryset(cls, field_name, valid_on):
        criteria = {'valid_thru__gte': valid_on, 'valid_from__lte': valid_on}
        field = cls._meta.get_field(field_name)
        criteria.update(field.get_limit_choices_to())
        return field.rel.to.objects.filter(**criteria)


class LineCoverage(models.Model):
    id = models.AutoField(primary_key=True)
    program_line_id = models.IntegerField()
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=5, blank=True, null=True)
    descr = models.CharField(max_length=255, blank=True, null=True)
    applies_to = models.CharField(max_length=1)
    credit_limit = models.DecimalField(max_digits=20, decimal_places=2)
    coverage_type = models.CharField(max_length=1)
    is_addable = models.NullBooleanField()
    is_prorateable = models.NullBooleanField()
    valid_from = models.DateField()
    valid_thru = models.DateField()

    class Meta:
        managed = False
        db_table = 'line_coverage'
        unique_together = (('id', 'valid_from'),)

    def __unicode__(self):
        return self.descr

    def __str__(self):
        return self.__unicode__()


class RateClasscodes(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    code = models.CharField(max_length=20)
    descr = models.CharField(max_length=254)
    valid_from = models.DateField()
    valid_thru = models.DateField()
    explanation = models.TextField(blank=True, null=True)
    iso_increase_premises = models.CharField(max_length=1, blank=True, null=True)
    iso_increase_products = models.CharField(max_length=1, blank=True, null=True)
    surcharge_factor = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    descr2 = models.CharField(max_length=255, blank=True, null=True)
    rate_group = models.IntegerField(blank=True, null=True)
    all_risk_grade = models.CharField(max_length=1, blank=True, null=True)
    alcohol_on_premises = models.NullBooleanField()
    liq_liab_eligible = models.NullBooleanField()
    enforce_central_burglar_alarm = models.NullBooleanField()
    bailees_eligible = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'rate_classcodes'
        unique_together = (('id', 'valid_from'),)

    def __unicode__(self):
        return '%s: %s' % (self.code, self.descr)

    def __str__(self):
        return self.__unicode__()


class RateDeductibles(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField(null=False)
    descr = models.CharField(max_length=127)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    rate_factor = models.DecimalField(max_digits=20, decimal_places=3)
    valid_from = models.DateField()
    valid_thru = models.DateField()
    line_coverage_id = models.IntegerField(default=0, null=False)

    class Meta:
        managed = False
        db_table = 'rate_deductibles'
        unique_together = (('id', 'valid_from'),)

    def __unicode__(self):
        return self.descr

    def __str__(self):
        return self.__unicode__()


class RateFactors(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    parameter_set = models.CharField(max_length=127)
    descr = models.CharField(max_length=127)
    is_default = models.NullBooleanField()
    factor = models.DecimalField(max_digits=20, decimal_places=3)
    valid_from = models.DateField()
    valid_thru = models.DateField()
    explanation = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rate_factors'
        unique_together = (('id', 'valid_from'),)

    def __unicode__(self):
        return self.descr

    def __str__(self):
        return self.__unicode__()


class RateIsoIncreasedLimits(models.Model):
    id = models.AutoField(primary_key=True)
    tableid = models.CharField(max_length=1)
    aggregate_limit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    occurrence_limit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    rate_factor = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    products_limit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rate_iso_increased_limits'


class RateLimits(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField(null=False)
    descr = models.CharField(max_length=127)
    limit1 = models.DecimalField(max_digits=20, decimal_places=2)
    limit1_descr = models.CharField(max_length=64, blank=True, null=True)
    limit2 = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    limit2_descr = models.CharField(max_length=64, blank=True, null=True)
    limit3 = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    limit3_descr = models.CharField(max_length=64, blank=True, null=True)
    limit4 = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    limit4_descr = models.CharField(max_length=64, blank=True, null=True)
    limit5 = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    limit5_descr = models.CharField(max_length=64, blank=True, null=True)
    limit6 = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    limit6_descr = models.CharField(max_length=64, blank=True, null=True)
    rate_value = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    rate_factor = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    valid_from = models.DateField()
    valid_thru = models.DateField()
    descr2 = models.CharField(max_length=255, blank=True, null=True)
    minimum_premium = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    line_coverage_id = models.IntegerField(default=0, null=False)
    is_default = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'rate_limits'
        unique_together = (('id', 'valid_from'),)

    def __unicode__(self):
        return self.descr

    def __str__(self):
        return self.__unicode__()


class RateRanges(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    line_coverage_id = models.IntegerField()
    lower = models.DecimalField(max_digits=20, decimal_places=2)
    upper = models.DecimalField(max_digits=20, decimal_places=2)
    descr = models.CharField(max_length=127)
    valid_from = models.DateField()
    valid_thru = models.DateField()

    class Meta:
        managed = False
        db_table = 'rate_ranges'
        unique_together = (('id', 'valid_from'),)


class RateTerritories(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    descr = models.CharField(max_length=127)
    code = models.CharField(max_length=20)
    is_default = models.NullBooleanField()
    valid_from = models.DateField()
    valid_thru = models.DateField()
    explanation = models.TextField(blank=True, null=True)
    surcharge_factor = models.DecimalField(max_digits=10, decimal_places=3)
    eligible = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'rate_territories'
        unique_together = (('id', 'valid_from'),)

    def __unicode__(self):
        return self.descr

    def __str__(self):
        return self.__unicode__()


class Rates(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    classcode = models.CharField(max_length=64, blank=True, null=True)
    territory = models.IntegerField(blank=True, null=True)
    limit1 = models.IntegerField(blank=True, null=True)
    deductible1 = models.IntegerField(blank=True, null=True)
    group1 = models.IntegerField(blank=True, null=True)
    group2 = models.IntegerField(blank=True, null=True)
    group3 = models.IntegerField(blank=True, null=True)
    rate1 = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    rate2 = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    rate3 = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    minimum_rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    valid_from = models.DateField()
    valid_thru = models.DateField()
    line_coverage_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rates'
        unique_together = (('id', 'valid_from'),)

def get_gl_territory_by_zipcode(module_id, zipcode, valid_on=timezone.now().date()):
	try:
		zipcode_obj = FiZipcodes.objects.get(zipcode=zipcode)
	except FiZipcodes.DoesNotExist:
		raise ValidationError(_('The zipcode %(value)s you provided can\'t be mapped. '
								'Are you sure it\'s a valid Zipcode? If yes, please contact us.'),
			code='nonexistent', params={'value': zipcode}
		)
	else:
		gl_territory_code = int(zipcode_obj.gl_territory)
		kwargs = {'module_id': module_id, 'code': gl_territory_code,
				  'valid_from__lte': valid_on, 'valid_thru__gte': valid_on}
		if gl_territory_code==10:
			kwargs['descr__icontains'] = zipcode_obj.county
		territory_obj = RateTerritories.objects.filter(**kwargs)

		if not territory_obj or not territory_obj[0].eligible:
			raise ValidationError(_('Ineligible risk!!! The zipcode %(value)s falls into '
									'\'%(territory)s\'  which is not an eligible Territory under this program!'),
				code='ineligible', params={'value': zipcode, 'territory': territory_obj[0]}
			)
		return territory_obj[0]

def get_hangl_rates(classcode, territory, limits, valid_on=timezone.now().date()):
	print 'classcode.code %s' % classcode.code
	print 'int(territory.code) %s' % int(territory.code)
	print 'limits.id %s' % limits.id
	criteria = {'classcode': classcode.code, 'territory': int(territory.code), 'limit1': limits.id}
	try:
		rates = get_rates(valid_on=valid_on, **criteria)
	except Rates.DoesNotExist:
		raise ValidationError(_('The rates are not setup for a risk with classcode %(classcode)s, '
								'territory %(territory)s and limits %(limit)s. Please contact us.'), 
							  code='nonexistent', 
							  params={'classcode': classcode.code,
					  				  'territory': str(territory),
					  				  'limit': str(limits)
					  				 })
	else:
		return rates

def get_rates(valid_on=timezone.now().date(), **kwargs):
	criteria = {'valid_thru__gte': valid_on, 'valid_from__lte': valid_on}
	criteria.update(kwargs)
	return Rates.objects.get(**criteria)
