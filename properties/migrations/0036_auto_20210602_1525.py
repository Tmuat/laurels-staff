# Generated by Django 3.2 on 2021-06-02 14:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0035_auto_20210602_1436"),
    ]

    operations = [
        migrations.CreateModel(
            name="SalesProgression",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(blank=True, max_length=100)),
                ("updated_by", models.CharField(blank=True, max_length=100)),
                (
                    "buyers_aml_checks_and_sales_memo",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "buyers_aml_checks_and_sales_memo_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "buyers_initial_solicitors_paperwork",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "buyers_initial_solicitors_paperwork_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "sellers_inital_solicitors_paperwork",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "sellers_inital_solicitors_paperwork_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "draft_contracts_recieved_by_buyers_solicitors",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "draft_contracts_recieved_by_buyers_solicitors_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "searches_paid_for",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "searches_paid_for_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "searches_ordered",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "searches_ordered_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "mortgage_application_submitted",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "mortgage_application_submitted_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "mortgage_survey_arranged",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "mortgage_survey_arranged_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "mortgage_survey_completed",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "mortgage_survey_completed_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "all_search_results_recieved",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "all_search_results_recieved_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "enquiries_raised",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "enquiries_raised_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "structural_survey_booked",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "structural_survey_booked_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "structural_survey_completed",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "structural_survey_completed_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "enquiries_answered",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "enquiries_answered_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "additional_enquiries_raised",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "additional_enquiries_raised_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "all_enquiries_answered",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "all_enquiries_answered_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "final_contracts_sent_out",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "final_contracts_sent_out_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "buyers_final_contracts_signed",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "buyers_final_contracts_signed_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "sellers_final_contracts_signed",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "sellers_final_contracts_signed_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "buyers_deposit_sent",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "buyers_deposit_sent_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "buyers_deposit_recieved",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "buyers_deposit_recieved_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "completion_date_agreed",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Done"), (False, "Not Done")],
                        default=False,
                        null=True,
                    ),
                ),
                (
                    "completion_date_agreed_date",
                    models.DateField(blank=True, null=True),
                ),
                (
                    "sales_notes",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "propertyprocess",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_progression",
                        to="properties.propertyprocess",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sale Progression",
                "verbose_name_plural": "Sale Progression'",
                "ordering": [
                    "propertyprocess__property__postcode",
                    "propertyprocess__property__address_line_1",
                ],
            },
        ),
        migrations.CreateModel(
            name="SalesProgressionPhase",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(blank=True, max_length=100)),
                ("updated_by", models.CharField(blank=True, max_length=100)),
                (
                    "overall_phase",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(4),
                        ],
                    ),
                ),
                ("phase_1", models.BooleanField(default=False)),
                ("phase_2", models.BooleanField(default=False)),
                ("phase_3", models.BooleanField(default=False)),
                ("phase_4", models.BooleanField(default=False)),
                (
                    "sale_progression",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_progression_phase",
                        to="properties.salesprogression",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sale Progression Phase",
                "verbose_name_plural": "Sale Progression' Phase",
                "ordering": [
                    "sale_progression__propertyprocess__property__postcode",
                    "sale_progression__propertyprocess__property__address_line_1",
                ],
            },
        ),
        migrations.CreateModel(
            name="SalesProgressionSettings",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(blank=True, max_length=100)),
                ("updated_by", models.CharField(blank=True, max_length=100)),
                (
                    "show_mortgage",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Show"), (False, "Hide")],
                        default=True,
                        null=True,
                    ),
                ),
                (
                    "show_survey",
                    models.BooleanField(
                        blank=True,
                        choices=[(True, "Show"), (False, "Hide")],
                        default=True,
                        null=True,
                    ),
                ),
                (
                    "sale_progression",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_progression_settings",
                        to="properties.salesprogression",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sale Progression Settings",
                "verbose_name_plural": "Sale Progression' Settings",
                "ordering": [
                    "sale_progression__propertyprocess__property__postcode",
                    "sale_progression__propertyprocess__property__address_line_1",
                ],
            },
        ),
        migrations.RemoveField(
            model_name="salestatusphase",
            name="sale_status",
        ),
        migrations.RemoveField(
            model_name="salestatussettings",
            name="sale_status",
        ),
        migrations.DeleteModel(
            name="SaleStatus",
        ),
        migrations.DeleteModel(
            name="SaleStatusPhase",
        ),
        migrations.DeleteModel(
            name="SaleStatusSettings",
        ),
    ]