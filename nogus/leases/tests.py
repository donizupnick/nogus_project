from django.core.exceptions import ValidationError
from .models import InvestmentStrategy

class InvestmentStrategyModelTest(TestCase):
    def test_create_investment_strategy(self):
        # Creating a valid InvestmentStrategy instance
        investment_strategy = InvestmentStrategy.objects.create(
            target_irr=15,
            acquisition_method='equity',
            holding_period_years=7
        )
        self.assertEqual(investment_strategy.target_irr, 15)
        self.assertEqual(investment_strategy.acquisition_method, 'equity')
        self.assertEqual(investment_strategy.holding_period_years, 7)

    def test_invalid_target_irr(self):
        # Testing an invalid target IRR (negative value)
        with self.assertRaises(ValidationError):
            investment_strategy = InvestmentStrategy(
                target_irr=-5,
                acquisition_method='equity',
                holding_period_years=7
            )
            investment_strategy.full_clean()

class PropertyAcquisitionModelTest(TestCase):
    def test_create_property_acquisition(self):
        # Creating a valid PropertyAcquisition instance
        property_acquisition = PropertyAcquisition.objects.create(
            property_name="Franklin's Tower",
            units=150,
            gross_square_feet=150000,
            net_rentable_square_feet=120000,
            occupancy_rate=60,
            purchase_price_per_unit=315000
        )
        self.assertEqual(property_acquisition.property_name, "Franklin's Tower")
        self.assertEqual(property_acquisition.units, 150)
        self.assertEqual(property_acquisition.gross_square_feet, 150000)
        self.assertEqual(property_acquisition.net_rentable_square_feet, 120000)
        self.assertEqual(property_acquisition.occupancy_rate, 60)
        self.assertEqual(property_acquisition.purchase_price_per_unit, 315000)

    def test_invalid_units(self):
        # Testing an invalid number of units (negative value)
        with self.assertRaises(ValidationError):
            property_acquisition = PropertyAcquisition(
                property_name="Invalid Property",
                units=-10,
                gross_square_feet=150000,
                net_rentable_square_feet=120000,
                occupancy_rate=60,
                purchase_price_per_unit=315000
            )
            property_acquisition.full_clean()

class LeasingStrategyModelTest(TestCase):
    # Creating a PropertyAcquisition instance to associate with LeasingStrategy
    @classmethod
    def setUpTestData(cls):
        cls.property_acquisition = PropertyAcquisition.objects.create(
            property_name="Franklin's Tower",
            units=150,
            gross_square_feet=150000,
            net_rentable_square_feet=120000,
            occupancy_rate=60,
            purchase_price_per_unit=315000
        )

    def test_create_leasing_strategy(self):
        # Creating a valid LeasingStrategy instance
        leasing_strategy = LeasingStrategy.objects.create(
            property_acquisition=self.property_acquisition,
            lease_up_rate_per_month=5,
            stabilization_vacancy_rate=5
        )
        self.assertEqual(leasing_strategy.lease_up_rate_per_month, 5)
        self.assertEqual(leasing_strategy.stabilization_vacancy_rate, 5)

    def test_invalid_lease_up_rate(self):
        # Testing an invalid lease-up rate (negative value)
        with self.assertRaises(ValidationError):
            leasing_strategy = LeasingStrategy(
                property_acquisition=self.property_acquisition,
                lease_up_rate_per_month=-5,
                stabilization_vacancy_rate=5
            )
            leasing_strategy.full_clean()

class RefinancingDetailsModelTest(TestCase):
    # Creating a PropertyAcquisition instance to associate with RefinancingDetails
    @classmethod
    def setUpTestData(cls):
        cls.property_acquisition = PropertyAcquisition.objects.create(
            property_name="Franklin's Tower",
            units=150,
            gross_square_feet=150000,
            net_rentable_square_feet=120000,
            occupancy_rate=60,
            purchase_price_per_unit=315000
        )

    def test_create_refinancing_details(self):
        # Creating a valid RefinancingDetails instance
        refinancing_details = RefinancingDetails.objects.create(
            property_acquisition=self.property_acquisition,
            interest_rate=3.5,
            amortization_period_years=30,
            term_years=7,
            prepayment_penalty_period_years=4,
            max_loan_to_value_ratio=70,
            min_debt_service_coverage_ratio=1.2,
            closing_fees_percentage=1.0
        )
        self.assertEqual(refinancing_details.interest_rate, 3.5)
        self.assertEqual(refinancing_details.amortization_period_years, 30)
        self.assertEqual(refinancing_details.term_years, 7)
        self.assertEqual(refinancing_details.prepayment_penalty_period_years, 4)
        self.assertEqual(refinancing_details.max_loan_to_value_ratio, 70)
        self.assertEqual(refinancing_details.min_debt_service_coverage_ratio, 1.2)
        self.assertEqual(refinancing_details.closing_fees_percentage, 1.0)

class SaleDetailsModelTest(TestCase):
    # Creating a PropertyAcquisition instance to associate with SaleDetails
    @classmethod
    def setUpTestData(cls):
        cls.property_acquisition = PropertyAcquisition.objects.create(
            property_name="Franklin's Tower",
            units=150,
            gross_square_feet=150000,
            net_rentable_square_feet=120000,
            occupancy_rate=60,
            purchase_price_per_unit=315000
        )

    def test_create_sale_details(self):
        # Creating a valid SaleDetails instance
        sale_details = SaleDetails.objects.create(
            property_acquisition=self.property_acquisition,
            going_out_cap_rate=5.5,
            fees=200000
        )
        self.assertEqual(sale_details.going_out_cap_rate, 5.5)
        self.assertEqual(sale_details.fees, 200000)

class PresidioSetupTest(TestCase):
    def setUp(self):
        # Creating an Investment Strategy instance for the Presidio case study
        self.investment_strategy = InvestmentStrategy.objects.create(
            target_irr=15,
            acquisition_method='equity',
            holding_period_years=7
        )

        # Creating a Property Acquisition instance for the Presidio case study
        self.property_acquisition = PropertyAcquisition.objects.create(
            property_name="Franklin's Tower",
            units=150,
            gross_square_feet=150000,
            net_rentable_square_feet=120000,
            occupancy_rate=60,
            purchase_price_per_unit=315000,
            investment_strategy=self.investment_strategy
        )

    
    def setUp(self):
        super().setUp()

        # Creating a Leasing Strategy instance for the Presidio case study
        self.leasing_strategy = LeasingStrategy.objects.create(
            property_acquisition=self.property_acquisition,
            lease_up_rate_per_month=5,
            stabilization_vacancy_rate=5
        )

        # Creating a Refinancing Details instance for the Presidio case study
        self.refinancing_details = RefinancingDetails.objects.create(
            property_acquisition=self.property_acquisition,
            interest_rate=3.5,
            amortization_period_years=30,
            term_years=7,
            prepayment_penalty_period_years=4,
            max_loan_to_value_ratio=70,
            min_debt_service_coverage_ratio=1.2,
            closing_fees_percentage=1.0
        )

        # Creating a Sale Details instance for the Presidio case study
        self.sale_details = SaleDetails.objects.create(
            property_acquisition=self.property_acquisition,
            going_out_cap_rate=5.5,
            fees=200000
        )
# Additional setup for Leasing Strategy, Refinancing Details, and Sale Details will be added later
