
from typing import List

def calculate_unlevered_irr(cash_flows: List[float]) -> float:
    """Calculates the unlevered internal rate of return (IRR) for a given series of cash flows.
    
    Args:
        cash_flows (List[float]): The cash flows for each period, including the initial investment and net operating income.

    Returns:
        float: The unlevered IRR as a percentage.
    """
    # Using the NumPy IRR function to calculate the unlevered IRR
    unlevered_irr = np.irr(cash_flows)
    return unlevered_irr * 100

def calculate_levered_irr(
    acquisition_cash_flow: float,
    operating_cash_flows: List[float],
    refinancing_cash_flow: float,
    sale_cash_flow: float,
    debt_payments: List[float]
) -> float:
    """Calculates the levered internal rate of return (IRR) for a given series of cash flows, including debt payments.

    Args:
        acquisition_cash_flow (float): The initial cash flow for acquiring the property (negative value).
        operating_cash_flows (List[float]): The net operating cash flows for each period.
        refinancing_cash_flow (float): The cash flow from refinancing.
        sale_cash_flow (float): The cash flow from selling the property.
        debt_payments (List[float]): The debt payments for each period.

    Returns:
        float: The levered IRR as a percentage.
    """
    # Calculating the net cash flows to equity by subtracting debt payments from operating cash flows
    net_cash_flows_to_equity = [acquisition_cash_flow] + [cf - dp for cf, dp in zip(operating_cash_flows, debt_payments)] + [refinancing_cash_flow] + [sale_cash_flow]

    # Using the NumPy IRR function to calculate the levered IRR
    levered_irr = np.irr(net_cash_flows_to_equity)
    return levered_irr * 100

def calculate_acquisition_cash_flow(purchase_price_per_unit: float, units: int, closing_costs: float) -> float:
    """Calculates the acquisition cash flow for purchasing a property.
    
    Args:
        purchase_price_per_unit (float): The purchase price per unit.
        units (int): The total number of units in the property.
        closing_costs (float): The additional closing costs.

    Returns:
        float: The acquisition cash flow (negative value).
    """
    # Calculating the total purchase price and adding closing costs
    acquisition_cash_flow = -(purchase_price_per_unit * units + closing_costs)
    return acquisition_cash_flow

def calculate_operating_cash_flows(
    in_place_rent: float,
    gross_square_feet: float,
    occupancy_rate: float,
    operating_expenses: float,
    rent_growth_rate: float,
    vacancy_rate: float,
    holding_period_years: int
) -> List[float]:
    """Calculates the operating cash flows for each period during the holding period.
    
    Args:
        in_place_rent (float): The in-place rent per square foot per month.
        gross_square_feet (float): The total gross square feet in the property.
        occupancy_rate (float): The initial occupancy rate as a percentage.
        operating_expenses (float): The total operating expenses for the first year.
        rent_growth_rate (float): The annual rent growth rate as a percentage.
        vacancy_rate (float): The vacancy rate upon stabilization as a percentage.
        holding_period_years (int): The total holding period in years.

    Returns:
        List[float]: The operating cash flows for each period.
    """
    operating_cash_flows = []
    for year in range(holding_period_years):
        # Calculating the effective rent considering occupancy and vacancy
        effective_rent = in_place_rent * gross_square_feet * 12 * ((occupancy_rate - vacancy_rate) / 100)
        
        # Adjusting the rent for rent growth
        effective_rent *= (1 + rent_growth_rate / 100) ** year

        # Calculating the NOI by subtracting operating expenses
        noi = effective_rent - operating_expenses * (1 + 0.03) ** year  # 3% annual growth in operating expenses

        operating_cash_flows.append(noi)

    return operating_cash_flows

def calculate_refinancing_cash_flow(
    noi: float,
    cap_rate: float,
    max_loan_to_value_ratio: float,
    closing_fees_percentage: float
) -> float:
    """Calculates the refinancing cash flow for refinancing a property.
    
    Args:
        noi (float): The net operating income at the time of refinancing.
        cap_rate (float): The capitalization rate used for refinancing valuation.
        max_loan_to_value_ratio (float): The maximum loan-to-value ratio allowed.
        closing_fees_percentage (float): The closing fees as a percentage of the refinanced amount.

    Returns:
        float: The refinancing cash flow.
    """
    # Calculating the property value based on NOI and cap rate
    property_value = noi / (cap_rate / 100)

    # Calculating the refinanced amount considering the max loan-to-value ratio
    refinanced_amount = property_value * max_loan_to_value_ratio / 100

    # Applying closing fees
    closing_fees = refinanced_amount * closing_fees_percentage / 100

    # Calculating the refinancing cash flow
    refinancing_cash_flow = refinanced_amount - closing_fees
    return refinancing_cash_flow

def calculate_sale_cash_flow(
    noi: float,
    going_out_cap_rate: float,
    fees: float
) -> float:
    """Calculates the sale cash flow for selling a property at the end of the investment period.
    
    Args:
        noi (float): The net operating income at the time of sale.
        going_out_cap_rate (float): The going-out capitalization rate used for sale valuation.
        fees (float): The additional fees associated with the sale.

    Returns:
        float: The sale cash flow.
    """
    # Calculating the property value based on NOI and going-out cap rate
    property_value = noi / (going_out_cap_rate / 100)

    # Calculating the sale cash flow after deducting fees
    sale_cash_flow = property_value - fees
    return sale_cash_flow

def calculate_debt_payments(
    principal: float,
    interest_rate: float,
    amortization_period_years: int,
    loan_term_years: int
) -> List[float]:
    """Calculates the periodic debt payments for a loan over the loan term.
    
    Args:
        principal (float): The principal amount of the loan.
        interest_rate (float): The annual interest rate as a percentage.
        amortization_period_years (int): The amortization period in years.
        loan_term_years (int): The loan term in years.

    Returns:
        List[float]: The monthly debt payments for each period within the loan term.
    """
    # Monthly interest rate
    monthly_interest_rate = (interest_rate / 100) / 12

    # Total number of payments (monthly)
    total_payments_amortization = amortization_period_years * 12
    total_payments_loan_term = loan_term_years * 12

    # Monthly payment using the formula for monthly payment on an amortizing loan
    monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-total_payments_amortization))

    # Monthly payments over the loan term
    debt_payments = [monthly_payment] * total_payments_loan_term
    return debt_payments

def calculate_comprehensive_cash_flows(
    acquisition_cash_flow: float,
    operating_cash_flows: List[float],
    refinancing_cash_flow: float,
    sale_cash_flow: float,
    debt_payments: List[float]
) -> List[float]:
    """Calculates the comprehensive cash flows over the holding period, including all investment activities.
    
    Args:
        acquisition_cash_flow (float): The initial cash flow for acquiring the property (negative value).
        operating_cash_flows (List[float]): The net operating cash flows for each period.
        refinancing_cash_flow (float): The cash flow from refinancing.
        sale_cash_flow (float): The cash flow from selling the property.
        debt_payments (List[float]): The debt payments for each period.

    Returns:
        List[float]: The comprehensive cash flows for each period within the holding period.
    """
    # Adding acquisition cash flow
    comprehensive_cash_flows = [acquisition_cash_flow]

    # Adding operating cash flows and debt payments
    for cf, dp in zip(operating_cash_flows, debt_payments):
        comprehensive_cash_flows.append(cf - dp)

    # Adding refinancing cash flow
    comprehensive_cash_flows.append(refinancing_cash_flow)

    # Adding sale cash flow
    comprehensive_cash_flows.append(sale_cash_flow)

    return comprehensive_cash_flows
