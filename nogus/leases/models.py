"""

"""



from datetime import date, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib import admin



# 1. Property Valuation Model
class PropertyValuation(models.Model):
    appraisal_value = models.FloatField(validators=[MinValueValidator(0)], default=0)
    valuation_date = models.DateField()
    VALUATION_METHOD_CHOICES = [('market', 'Market Value'), ('income', 'Income Approach'), ('cost', 'Cost Approach')]
    valuation_method = models.CharField(max_length=50, choices=VALUATION_METHOD_CHOICES, default='market')

    def __str__(self):
        return f'Appraisal Value: {self.appraisal_value}, Valuation Method: {self.valuation_method}'

# 2. Property Improvement Model
class PropertyImprovement(models.Model):
    description = models.TextField()
    cost = models.FloatField(validators=[MinValueValidator(0)], default=0)
    completion_date = models.DateField()

    def __str__(self):
        return f'Description: {self.description}, Cost: {self.cost}'


# 3. Property Management Model
class PropertyManagement(models.Model):
    company_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    management_fee_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)


    def __str__(self):
        return f'Company Name: {self.company_name}, Management Fee: {self.management_fee_percentage}%'

class DebtFinancing(models.Model):
    interest_rate = models.FloatField(validators=[MinValueValidator(0)], default=0)
    amortization_period_years = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=30)
    term_years = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(7)], default=7)
    max_loan_to_value = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(70)], default=70)
    min_debt_service_coverage_ratio = models.FloatField(validators=[MinValueValidator(1.2)], default=1.2)
    closing_fees_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=1.0)
    prepayment_penalty_period_years = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], default=4)

    def __str__(self):
        return f'Interest Rate: {self.interest_rate}, Amortization Period: {self.amortization_period_years} years'

class PropertySale(models.Model):
    going_out_cap_rate = models.FloatField(validators=[MinValueValidator(0)], default=5.5)
    sale_fees = models.FloatField(validators=[MinValueValidator(0)], default=200000)
    sale_date = models.DateField()

    def __str__(self):
        return f'Going Out Cap Rate: {self.going_out_cap_rate}, Sale Fees: {self.sale_fees}'


class PropertyAcquisition(models.Model):
    purchase_price_per_unit = models.FloatField(validators=[MinValueValidator(0)], default=0)
    closing_costs = models.FloatField(validators=[MinValueValidator(0)], default=0)
    acquisition_date = models.DateField()
    # Additional fields can be added here as needed

    def __str__(self):
        return f'Purchase Price per Unit: {self.purchase_price_per_unit}, Closing Costs: {self.closing_costs}'


class AreaMeasure(models.Model):
    building_total = models.FloatField(validators=[MinValueValidator(0)], default=0)
    office_total = models.FloatField(validators=[MinValueValidator(0)], default=0)
    retail_total = models.FloatField(validators=[MinValueValidator(0)], default=0)
    industrial_total = models.FloatField(validators=[MinValueValidator(0)], default=0)
    storage_total = models.FloatField(validators=[MinValueValidator(0)], default=0)
    alternate_building_total = models.FloatField(validators=[MinValueValidator(0)], default=0)

class MarketLeasingProfile(models.Model):
    market_rent = models.FloatField(validators=[MinValueValidator(0)], default=0)
    area_to_lease = models.FloatField(validators=[MinValueValidator(0)], default=0)
    average_lease_area = models.FloatField(validators=[MinValueValidator(0)], default=0)
    market_rent_units = models.FloatField(validators=[MinValueValidator(0)], default=0) # New field
    unit_rollover_fields = models.FloatField(validators=[MinValueValidator(0)], default=0) # New field
    absorption_assumptions = models.FloatField(validators=[MinValueValidator(0)], default=0) # New field

    def calculate_market_lease(self, lease):
        return self.market_rent * lease.leased_area

    def __str__(self):
        return f'Market Rent: {self.market_rent}, Area to Lease: {self.area_to_lease}'


class LocationDetail(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.zip_code}, {self.country}'

class BuildingAreaEntry(models.Model):
    date = models.DateField(default=date.today)
    month = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(11)])
    amount = models.FloatField(validators=[MinValueValidator(0)], default=0)


class LeaseFinancialDetail(models.Model):
    ANNUAL_RENT_ESCALATION_CHOICES = [
    ('fixed', 'Fixed Percentage'),
    ('cpi', 'Consumer Price Index'),
    # Add other choices here
    ]
    AREA_TYPE_CHOICES = [('standard', 'Standard Area'), ('alternate', 'Alternate Area')] # New choices
    RECOVERY_ALLOCATION_CHOICES = [('fixed', 'Fixed Percentage'), ('pro_rata', 'Pro-Rata Rentable Area')] # New choices

    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES, default='standard') # New field
    recovery_allocation_method = models.CharField(max_length=50, choices=RECOVERY_ALLOCATION_CHOICES, default='fixed') # New field
    initial_rent_method = models.CharField(max_length=50, choices=[('fixed', 'Fixed Amount'), ('per_sqft', 'Per Square Foot')], default='fixed')
    initial_rent_fixed_amount = models.FloatField(validators=[MinValueValidator(0)], default=0, blank=True, null=True)
    initial_rent_per_sqft = models.FloatField(validators=[MinValueValidator(0)], default=0, blank=True, null=True)
    annual_rent_escalation_method = models.CharField(max_length=50, choices=ANNUAL_RENT_ESCALATION_CHOICES, default='fixed')
    CAM_charges = models.FloatField(validators=[MinValueValidator(0)], default=0)
    real_estate_taxes_pass_through = models.BooleanField(default=False)
    utilities_pass_through = models.BooleanField(default=False)
    tenant_improvement_allowances = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def calculate_initial_rent(self):
        if self.initial_rent_fixed:
            return self.initial_rent_fixed
        elif self.leased_area and self.price_per_square_foot:
            return self.leased_area * self.price_per_square_foot
        else:
            return 0

    def __str__(self):
        return f'Initial Rent: {self.initial_rent}, CAM Charges: {self.CAM_charges}'

    class Meta:
        verbose_name_plural = "Lease Financial Details"

class LeaseEscalationMethod(models.Model):
    CPI_CHOICES = [
        ('lease_year', 'Lease Year'),
        ('calendar_year', 'Calendar Year'),
        ('mid_lease', 'At Mid Lease'),
        # Add other CPI choices here
    ]
    REVIEW_CHOICES = [
        ('sales_review', '% of Sales Review'),
        ('partial_ratchet_higher', 'Partial Ratchet Higher'),
        ('partial_ratchet_lower', 'Partial Ratchet Lower'),
        # Add other review choices here
    ]
    CPI_method = models.CharField(max_length=50, choices=CPI_CHOICES, default='default')
    review_option = models.CharField(max_length=50, choices=REVIEW_CHOICES, default='default')

    def calculate_escalation(self, lease, month):
        # Logic to calculate escalation based on the chosen methodology
        if self.CPI_method == 'lease_year':
            # Example logic for Lease Year CPI method
            return lease.initial_rent * (1 + month * 0.01)
        # Add logic for other methods
        return lease.initial_rent

class rental_unit(models.Model):
    """
    This class is used to store the rental unit details
    This includes functional fields like area, type, etc.
    """
    UNIT_TYPE_CHOICES = [
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('condo', 'Condominium'),
    ('townhouse', 'Townhouse'),
    # Add other unit types here
]

    unit_type = models.CharField(max_length=50, choices=UNIT_TYPE_CHOICES)


class RealEstateProperty(models.Model):
    name = models.CharField(max_length=200)
    location_details = models.OneToOneField(LocationDetail, on_delete=models.CASCADE, null=True, blank=True)
    area_measures = models.OneToOneField(AreaMeasure, on_delete=models.CASCADE, null=True, blank=True) # New field
    total_area = models.FloatField(validators=[MinValueValidator(0)], default=0)
    real_estate_taxes = models.FloatField(validators=[MinValueValidator(0)], default=0)
    leased_area = models.FloatField(validators=[MinValueValidator(0)], default=0)
    operating_expenses = models.FloatField(validators=[MinValueValidator(0)], default=0)
    management_fee_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    utilities = models.FloatField(validators=[MinValueValidator(0)], default=0)
    capital_costs = models.FloatField(validators=[MinValueValidator(0)], default=0)
    debt_service = models.FloatField(validators=[MinValueValidator(0)], default=0)
    vacancy_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    debt_financing = models.OneToOneField(DebtFinancing, on_delete=models.SET_NULL, null=True, blank=True)
    property_sale = models.OneToOneField(PropertySale, on_delete=models.SET_NULL, null=True, blank=True)
    
    def calculate_cash_flow_after_debt_service(self):
        return self.calculate_net_operating_income() - self.debt_service - self.capital_costs

    def calculate_net_operating_income(self):
        gross_income = sum(lease.calculate_monthly_cashflow() for lease in self.leases.all())
        operating_expenses_with_management = self.operating_expenses + (self.management_fee_percentage / 100) * gross_income
        return gross_income - operating_expenses_with_management - self.real_estate_taxes - self.utilities

  
    class Meta:
        verbose_name_plural = "Real Estate Properties"

    def __str__(self):
        return self.name
    
class Lease(models.Model):

    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('retail', 'Retail'),
        # Add other property types here
    ]

    real_estate_property = models.ForeignKey(RealEstateProperty, related_name='leases', on_delete=models.CASCADE)
    tenant_name = models.CharField(max_length=200)
    lease_start_date = models.DateField(default=date.today)
    lease_end_date = models.DateField(default=date.today() + timedelta(days=365))
    leased_area = models.FloatField(validators=[MinValueValidator(0)], default=0)
    renewal_probability = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    rent_free_period = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    financial_details = models.OneToOneField(LeaseFinancialDetail, on_delete=models.CASCADE, null=True, blank=True)
    external_id = models.CharField(max_length=38, blank=True, null=True)
    entity_id = models.CharField(max_length=38, blank=True, null=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='residential')
    building_area = models.FloatField(validators=[MinValueValidator(0)], default=0)
    analysis_begin_date = models.DateField(default=date.today)
    length_of_analysis_years = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=1)
    length_of_analysis_months = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(11)], default=1)
    use_actuals = models.BooleanField(default=False)
    actual_values_end_date = models.DateField(blank=True, null=True)
    use_prior_budget = models.BooleanField(default=False)
    budget_period_end_date = models.DateField(blank=True, null=True)
    use_inflation_begin_date = models.BooleanField(default=False)
    miscellaneous_revenue_inflation_begin_date = models.DateField(blank=True, null=True)
    operating_expense_inflation_begin_date = models.DateField(blank=True, null=True)
    capital_expense_inflation_begin_date = models.DateField(blank=True, null=True)
    property_valuation = models.OneToOneField(PropertyValuation, on_delete=models.SET_NULL, null=True, blank=True)
    property_improvement = models.OneToOneField(PropertyImprovement, on_delete=models.SET_NULL, null=True, blank=True)
    property_management = models.OneToOneField(PropertyManagement, on_delete=models.SET_NULL, null=True, blank=True)


    
    EXPIRATION_CHOICES = [
        ('market', 'Market'),
        ('reabsorb', 'Reabsorb'),
        ('renew', 'Renew'),
        ('vacate', 'Vacate'),
        ('option', 'Option'),
    ]
    expiration_option = models.CharField(max_length=10, choices=EXPIRATION_CHOICES, default='market')
    market_leasing_profile = models.ForeignKey(MarketLeasingProfile, on_delete=models.SET_NULL, null=True, blank=True)
    escalation_method = models.ForeignKey(LeaseEscalationMethod, on_delete=models.SET_NULL, null=True, blank=True)
    RENEWAL_CHOICES = [
        ('market', 'Market'),
        ('prior', 'Prior'),
        ('lesser_of', 'Use Lesser of'),
        ('greater_of', 'Use Greater of'),
    ]
    renewal_rate_option = models.CharField(max_length=12, choices=RENEWAL_CHOICES, default='market')

    def handle_expiration(self):
        # Logic to handle expiration based on selected option
        if self.expiration_option == 'market':
            return self.market_leasing_profile.calculate_market_lease(self)
        # expiration option: reabsorb
        # Definition: The space is reabsorbed into the property and the rent is set to the market rent

    def calculate_renewal_rate(self, month):
        # Logic to calculate renewal rate based on selected option
        if self.renewal_rate_option == 'market':
            return self.market_leasing_profile.calculate_market_lease(self)
        # Add logic for other renewal options

    def calculate_monthly_cashflow(self, month): #todo
        rent = self.escalation_method.calculate_escalation(self, month)
        # Subtract expenses and other calculations
        return rent - self.expenses

    def calculate_monthly_rent(self, month): #todo
        rent = self.financial_details.initial_rent
        escalation_factor = 1 + (self.financial_details.annual_rent_escalation / 100)
        for _ in range(month):
            rent *= escalation_factor
        return rent


    def generate_cashflow_time_series(self, start_date, end_date):
        cashflows = []
        current_date = start_date
        month = 0
        while current_date <= end_date:
            cashflow = self.calculate_monthly_cashflow(month)
            cashflows.append((current_date, cashflow))
            current_date += timedelta(days=30)
            month += 1
        return cashflows

    def calculate_total_value(self):
        return self.property_valuation.appraisal_value + self.property_improvement.cost

    def calculate_total_expenses(self):
        return self.operating_expenses + self.real_estate_taxes + self.utilities + self.capital_costs + self.debt_service

    def calculate_gross_income(self):
        return sum(lease.calculate_monthly_cashflow() for lease in self.leases.all()) * 12


    class Meta:
        verbose_name_plural = "Leases"

    def __str__(self):
        return self.tenant_name

class LeaseDetail(models.Model):
    lease = models.ForeignKey(Lease, related_name='details', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    rent = models.FloatField(validators=[MinValueValidator(0)], default=0)
    historical_vacancy_rates = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    estimated_future_vacancy_rates = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    time_to_lease_up_vacant_space = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    class Meta:
        verbose_name_plural = "Lease Details"

    def __str__(self):
        return f'{self.lease.tenant_name} - {self.date}'
class OperatingExpense(models.Model):
    real_estate_property = models.ForeignKey(RealEstateProperty, related_name='operating_expenses', on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=200)
    amount = models.FloatField(validators=[MinValueValidator(0)], default=0)
    date = models.DateField()

class ExpenseRecovery(models.Model):
    lease = models.ForeignKey(Lease, related_name='expense_recoveries', on_delete=models.CASCADE)
    recovery_type = models.CharField(max_length=200)
    amount = models.FloatField(validators=[MinValueValidator(0)], default=0)
    date = models.DateField()


class ChartOfAccounts(models.Model):
    name = models.CharField(max_length=200)
    external_id = models.CharField(max_length=38, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [('parent', 'Parent Account'), ('child', 'Child Account')]
    CLASS_CHOICES = [('revenue', 'Revenue'), ('expense', 'Expense')]
    LINE_ITEM_TYPE_CHOICES = [...]  # Define as per your requirements
    COST_CODE_TYPE_CHOICES = [...]  # Define as per your requirements

    chart = models.ForeignKey(ChartOfAccounts, related_name='accounts', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.CharField(max_length=50)
    description = models.TextField()
    account_class = models.CharField(max_length=50, choices=CLASS_CHOICES)
    line_item_type = models.CharField(max_length=50, choices=LINE_ITEM_TYPE_CHOICES)
    cost_code_type = models.CharField(max_length=50, choices=COST_CODE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class InvestmentStrategy(models.Model):
    target_irr = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Target levered IRR (%)")
    acquisition_method = models.CharField(max_length=50, choices=[('equity', 'All Equity')], default='equity', help_text="Method of acquisition")
    holding_period_years = models.IntegerField(validators=[models.MinValueValidator(0), models.MaxValueValidator(30)], default=7, help_text="Holding period in years")

    def __str__(self):
        return f"Target IRR: {self.target_irr}%, Acquisition Method: {self.acquisition_method}, Holding Period: {self.holding_period_years} years"

class PropertyAcquisition(models.Model):
    property_name = models.CharField(max_length=200, help_text="Name of the property")
    units = models.IntegerField(validators=[models.MinValueValidator(0)], help_text="Number of units in the property")
    gross_square_feet = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Total gross square feet of the property")
    net_rentable_square_feet = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Net rentable square feet of the property")
    occupancy_rate = models.FloatField(validators=[models.MinValueValidator(0), models.MaxValueValidator(100)], help_text="Current occupancy rate (%)")
    purchase_price_per_unit = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Purchase price per unit")

    def __str__(self):
        return f"{self.property_name} - {self.units} units, {self.net_rentable_square_feet} net rentable sq ft"

class LeasingStrategy(models.Model):
    property_acquisition = models.OneToOneField(PropertyAcquisition, on_delete=models.CASCADE, related_name='leasing_strategy', help_text="Associated property acquisition")
    lease_up_rate_per_month = models.IntegerField(validators=[models.MinValueValidator(0)], help_text="Number of units to be leased per month")
    stabilization_vacancy_rate = models.FloatField(validators=[models.MinValueValidator(0), models.MaxValueValidator(100)], default=5, help_text="Vacancy rate upon stabilization (%)")

    def __str__(self):
        return f"Lease-up Rate: {self.lease_up_rate_per_month} units/month, Stabilization Vacancy: {self.stabilization_vacancy_rate}%"

class RefinancingDetails(models.Model):
    property_acquisition = models.OneToOneField(PropertyAcquisition, on_delete=models.CASCADE, related_name='refinancing_details', help_text="Associated property acquisition")
    interest_rate = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Annual interest rate (%)")
    amortization_period_years = models.IntegerField(validators=[models.MinValueValidator(0), models.MaxValueValidator(30)], help_text="Amortization period in years")
    term_years = models.IntegerField(validators=[models.MinValueValidator(0), models.MaxValueValidator(30)], help_text="Term in years")
    prepayment_penalty_period_years = models.IntegerField(validators=[models.MinValueValidator(0), models.MaxValueValidator(30)], default=4, help_text="Prepayment penalty period in years")
    max_loan_to_value_ratio = models.FloatField(validators=[models.MinValueValidator(0), models.MaxValueValidator(100)], help_text="Max loan to value ratio (%)")
    min_debt_service_coverage_ratio = models.FloatField(validators=[models.MinValueValidator(1)], help_text="Minimum debt service coverage ratio")
    closing_fees_percentage = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Closing fees as a percentage of loan amount (%)")

    def __str__(self):
        return f"Interest Rate: {self.interest_rate}%, Term: {self.term_years} years, Max LTV: {self.max_loan_to_value_ratio}%"

class SaleDetails(models.Model):
    property_acquisition = models.OneToOneField(PropertyAcquisition, on_delete=models.CASCADE, related_name='sale_details', help_text="Associated property acquisition")
    going_out_cap_rate = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Going out cap rate (%)")
    fees = models.FloatField(validators=[models.MinValueValidator(0)], help_text="Fees associated with the sale")

    def __str__(self):
        return f"Going Out Cap Rate: {self.going_out_cap_rate}%, Fees: ${self.fees}"
