import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone

from properties.models import SalesProgression, LettingsProgression


def quarter_year_calc():
    def calculate_start_month(date):
        start_month = (((date.month - 1) // 3) * 3) + 1
        return start_month

    def calculate_start_year(date):
        start_year = date.year
        return start_year

    todays_date = timezone.now()

    start_month = int(calculate_start_month(todays_date))
    start_year = int(calculate_start_year(todays_date))

    if start_month == 10:
        start_year += 1

    return str(start_year)


def quarter_and_year_calc(date):

    data = dict()

    def calculate_start_month(date):
        start_month = (((date.month - 1) // 3) * 3) + 1
        return start_month

    def calculate_start_year(date):
        start_year = date.year
        return start_year

    start_month = int(calculate_start_month(date))
    start_year = int(calculate_start_year(date))
    company_year = start_year

    if start_month == 10:
        company_year += 1

    if start_month == 10:
        quarter = "q1"
    elif start_month == 1:
        quarter = "q2"
    elif start_month == 4:
        quarter = "q3"
    elif start_month == 7:
        quarter = "q4"

    end_month = start_month + 2

    data["start_year"] = start_year
    data["company_year"] = company_year
    data["start_month"] = start_month
    data["end_month"] = end_month
    data["quarter"] = quarter

    return data


def last_quarter_and_year_calc(date):

    data = dict()

    def calculate_start_month(date):
        start_month = (((date.month - 1) // 3) * 3) + 1
        return start_month

    def calculate_start_year(date):
        start_year = date.year
        return start_year

    actual_month = int(calculate_start_month(date))
    start_year = int(calculate_start_year(date))
    company_year = start_year

    if actual_month == 1:
        start_month = 10
        start_year = start_year - 1
    else:
        start_month = actual_month - 3

    if actual_month == 10:
        company_year += 1

    if start_month == 10:
        quarter = "q1"
    elif start_month == 1:
        quarter = "q2"
    elif start_month == 4:
        quarter = "q3"
    elif start_month == 7:
        quarter = "q4"

    end_month = start_month + 2

    data["start_year"] = start_year
    data["company_year"] = company_year
    data["start_month"] = start_month
    data["end_month"] = end_month
    data["quarter"] = quarter

    return data


def calculate_quarter_and_year(date):

    data = []

    def calculate_start_month(date):
        start_month = (((date.month - 1) // 3) * 3) + 1
        return start_month

    def calculate_start_year(date):
        start_year = date.year
        return start_year
    
    start_month = int(calculate_start_month(date))
    start_year = int(calculate_start_year(date))
    
    for idx, quarter in enumerate(range(4)):
        if start_month == 10:
            q1 = "q1"
            q1_start = 10
            q1_end = q1_start + 2
            q1_year = start_year
            q1_company_year = start_year + 1
            q2 = "q4"
            q2_start = 7
            q2_end = q2_start + 2
            q2_year = start_year
            q2_company_year = start_year
            q3 = "q3"
            q3_start = 4
            q3_end = q3_start + 2
            q3_year = start_year
            q3_company_year = start_year
            q4 = "q2"
            q4_start = 1
            q4_end = q4_start + 2
            q4_year = start_year
            q4_company_year = start_year
        elif start_month == 1:
            q1 = "q2"
            q1_start = 1
            q1_end = q1_start + 2
            q1_year = start_year
            q1_company_year = start_year
            q2 = "q1"
            q2_start = 10
            q2_end = q2_start + 2
            q2_year = start_year - 1
            q2_company_year = start_year
            q3 = "q4"
            q3_start = 7
            q3_end = q3_start + 2
            q3_year = start_year - 1
            q3_company_year = start_year - 1
            q4 = "q3"
            q4_start = 4
            q4_end = q4_start + 2
            q4_year = start_year - 1
            q4_company_year = start_year - 1
        elif start_month == 4:
            q1 = "q3"
            q1_start = 4
            q1_end = q1_start + 2
            q1_year = start_year
            q1_company_year = start_year
            q2 = "q2"
            q2_start = 1
            q2_end = q2_start + 2
            q2_year = start_year
            q2_company_year = start_year
            q3 = "q1"
            q3_start = 10
            q3_end = q3_start + 2
            q3_year = start_year - 1
            q3_company_year = start_year
            q4 = "q4"
            q4_start = 7
            q4_end = q4_start + 2
            q4_year = start_year - 1
            q4_company_year = start_year - 1
        elif start_month == 7:
            q1 = "q4"
            q1_start = 7
            q1_end = q1_start + 2
            q1_year = start_year
            q1_company_year = start_year
            q2 = "q3"
            q2_start = 4
            q2_end = q2_start + 2
            q2_year = start_year
            q2_company_year = start_year
            q3 = "q2"
            q3_start = 1
            q3_end = q3_start + 2
            q3_year = start_year
            q3_company_year = start_year
            q4 = "q1"
            q4_start = 10
            q4_end = q4_start + 2
            q4_year = start_year - 1
            q4_company_year = start_year

        quarter_dict = {}

        if idx == 0:
            quarter_dict["quarter"] = q1
            quarter_dict["start_month"] = q1_start
            quarter_dict["end_month"] = q1_end
            quarter_dict["start_year"] = q1_year
            quarter_dict["company_year"] = q1_company_year
        elif idx == 1:
            quarter_dict["quarter"] = q2
            quarter_dict["start_month"] = q2_start
            quarter_dict["end_month"] = q2_end
            quarter_dict["start_year"] = q2_year
            quarter_dict["company_year"] = q2_company_year
        elif idx == 2:
            quarter_dict["quarter"] = q3
            quarter_dict["start_month"] = q3_start
            quarter_dict["end_month"] = q3_end
            quarter_dict["start_year"] = q3_year
            quarter_dict["company_year"] = q3_company_year
        elif idx == 3:
            quarter_dict["quarter"] = q4
            quarter_dict["start_month"] = q4_start
            quarter_dict["end_month"] = q4_end
            quarter_dict["start_year"] = q4_year
            quarter_dict["company_year"] = q4_company_year

        data.append(quarter_dict)

    return data


def sales_progression_percentage(propertyprocess_id):
    instance = get_object_or_404(
        SalesProgression, propertyprocess=propertyprocess_id
    )

    percentages = {}

    phase_1 = 0
    phase_2 = 0
    phase_3 = 0
    phase_4 = 0

    if instance.buyers_aml_checks_and_sales_memo:
        phase_1 += 1
    if instance.buyers_initial_solicitors_paperwork:
        phase_1 += 1
    if instance.sellers_inital_solicitors_paperwork:
        phase_1 += 1
    if instance.draft_contracts_recieved_by_buyers_solicitors:
        phase_1 += 1
    if instance.searches_paid_for:
        phase_1 += 1
    if instance.searches_ordered:
        phase_1 += 1

    if instance.sales_progression_settings.show_mortgage:
        if instance.mortgage_application_submitted:
            phase_2 += 1
        if instance.mortgage_survey_arranged:
            phase_2 += 1
        if instance.mortgage_offer_with_solicitors:
            phase_2 += 1
        if instance.all_search_results_recieved:
            phase_2 += 1
    else:
        if instance.all_search_results_recieved:
            phase_2 += 1

    if instance.sales_progression_settings.show_survey:
        if instance.structural_survey_booked:
            phase_3 += 1
        if instance.structural_survey_completed:
            phase_3 += 1
        if instance.enquiries_raised:
            phase_3 += 1
        if instance.enquiries_answered:
            phase_3 += 1
    else:
        if instance.enquiries_raised:
            phase_3 += 1
        if instance.enquiries_answered:
            phase_3 += 1

    if instance.additional_enquiries_raised:
        phase_4 += 1
    if instance.all_enquiries_answered:
        phase_4 += 1
    if instance.final_contracts_sent_out:
        phase_4 += 1
    if instance.buyers_final_contracts_signed:
        phase_4 += 1
    if instance.sellers_final_contracts_signed:
        phase_4 += 1
    if instance.buyers_deposit_sent:
        phase_4 += 1
    if instance.buyers_deposit_recieved:
        phase_4 += 1
    if instance.completion_date_agreed:
        phase_4 += 1

    percentages["phase_1"] = round(phase_1 / 6, 2) * 100

    if instance.sales_progression_settings.show_mortgage:
        percentages["phase_2"] = round(phase_2 / 4, 2) * 100
    else:
        percentages["phase_2"] = round(phase_2 / 1, 2) * 100

    if instance.sales_progression_settings.show_survey:
        percentages["phase_3"] = round(phase_3 / 4, 2) * 100
    else:
        percentages["phase_3"] = round(phase_3 / 2, 2) * 100

    percentages["phase_4"] = round(phase_4 / 8, 2) * 100

    return percentages


def lettings_progression_percentage(propertyprocess_id):
    instance = get_object_or_404(
        LettingsProgression, propertyprocess=propertyprocess_id
    )

    percentages = {}

    phase_1 = 0
    phase_2 = 0
    phase_3 = 0
    phase_4 = 0

    if instance.contact_touch_point_to_ll_and_tt:
        phase_1 += 1
    if instance.reference_forms_sent_to_tenant:
        phase_1 += 1
    if instance.compliance_form_sent_to_landlord:
        phase_1 += 1
    if instance.google_drive_and_email_inbox:
        phase_1 += 1
    if instance.tenancy_created_on_expert_agent:
        phase_1 += 1

    if instance.lettings_progression_settings.show_gas:
        if instance.gas_safety_certificate:
            phase_2 += 1
    if instance.references_passed:
        phase_2 += 1
    if instance.electrical_certificate:
        phase_2 += 1
    if instance.epc_certificate:
        phase_2 += 1
    if instance.tenancy_certificate_sent:
        phase_2 += 1

    if instance.tenancy_agreement_signed:
        phase_3 += 1
    if instance.tenant_invoice_sent:
        phase_3 += 1
    if instance.move_in_funds_received:
        phase_3 += 1
    if instance.prescribed_info_and_statutory_docs_sent:
        phase_3 += 1

    if instance.deposit_registered_with_tds:
        phase_4 += 1
    if instance.landlord_invoices_sent_to_ea:
        phase_4 += 1
    if instance.right_to_rent:
        phase_4 += 1

    percentages["phase_1"] = round(phase_1 / 5, 2) * 100

    if instance.lettings_progression_settings.show_gas:
        percentages["phase_2"] = round(phase_2 / 5, 2) * 100
    else:
        percentages["phase_2"] = round(phase_2 / 4, 2) * 100

    percentages["phase_3"] = round(phase_3 / 4, 2) * 100

    percentages["phase_4"] = round(phase_4 / 3, 2) * 100

    return percentages


def date_calc(date, filter):

    data = dict()

    def calculate_start_month(date):
        start_month = (((date.month - 1) // 3) * 3) + 1
        return start_month

    def calculate_start_year(date):
        start_year = date.year
        return start_year

    start_month = int(calculate_start_month(date))
    start_year = int(calculate_start_year(date))
    company_year = start_year

    if filter == "last_quarter":
        if start_month == 1:
            start_month = 10
            start_year = start_year - 1
        else:
            start_month = start_month - 3
    elif filter == "year_to_date":
        if start_month < 10:
            start_month = 10
            start_year = start_year - 1
    elif filter == "previous_year":
        if start_month < 10:
            start_month = 10
            start_year = start_year - 2
        else:
            start_year = start_year - 1

    if start_month == 10:
        company_year += 1

    if start_month == 10:
        quarter = "q1"
    elif start_month == 1:
        quarter = "q2"
    elif start_month == 4:
        quarter = "q3"
    elif start_month == 7:
        quarter = "q4"

    if filter == "year_to_date":
        end_month = 9
    elif filter == "previous_year":
        end_month = 9
    else:
        end_month = start_month + 2

    start_date = datetime.date(start_year, start_month, 1)

    if filter == "year_to_date":
        end_date = (
            datetime.date(
                (start_year + 1) + (end_month == 12),
                (end_month + 1 if end_month < 12 else 1),
                1,
            )
            - datetime.timedelta(1)
        )
    elif filter == "previous_year":
        end_date = (
            datetime.date(
                (start_year + 1) + (end_month == 12),
                (end_month + 1 if end_month < 12 else 1),
                1,
            )
            - datetime.timedelta(1)
        )
    elif filter == "all_time":
        end_date = (
            datetime.date(
                (start_year + 1) + (end_month == 12),
                (end_month + 1 if end_month < 12 else 1),
                1,
            )
            - datetime.timedelta(1)
        )
        start_year = 2014
        start_month = 1
        start_date = datetime.date(start_year, start_month, 1)
    else:
        end_date = (
            datetime.date(
                start_year + (end_month == 12),
                (end_month + 1 if end_month < 12 else 1),
                1,
            )
            - datetime.timedelta(1)
        )

    data["start_year"] = start_year
    data["company_year"] = company_year
    data["quarter"] = quarter
    data["start_date"] = start_date
    data["end_date"] = end_date

    return data
