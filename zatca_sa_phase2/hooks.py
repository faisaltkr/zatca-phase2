app_name = "zatca_sa_phase2"
app_title = "Zatca Sa Phase2"
app_publisher = "Insys Softwares"
app_description = "Zatca phase 2 integration for erpnext"
app_email = "faizeltkr@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zatca_sa_phase2/css/zatca_sa_phase2.css"
# app_include_js = "/assets/zatca_sa_phase2/js/zatca_sa_phase2.js"

# include js, css files in header of web template
# web_include_css = "/assets/zatca_sa_phase2/css/zatca_sa_phase2.css"
# web_include_js = "/assets/zatca_sa_phase2/js/zatca_sa_phase2.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "zatca_sa_phase2/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "zatca_sa_phase2/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "zatca_sa_phase2.utils.jinja_methods",
# 	"filters": "zatca_sa_phase2.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "zatca_sa_phase2.install.before_install"
# after_install = "zatca_sa_phase2.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "zatca_sa_phase2.uninstall.before_uninstall"
# after_uninstall = "zatca_sa_phase2.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "zatca_sa_phase2.utils.before_app_install"
# after_app_install = "zatca_sa_phase2.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "zatca_sa_phase2.utils.before_app_uninstall"
# after_app_uninstall = "zatca_sa_phase2.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zatca_sa_phase2.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"zatca_sa_phase2.tasks.all"
# 	],
# 	"daily": [
# 		"zatca_sa_phase2.tasks.daily"
# 	],
# 	"hourly": [
# 		"zatca_sa_phase2.tasks.hourly"
# 	],
# 	"weekly": [
# 		"zatca_sa_phase2.tasks.weekly"
# 	],
# 	"monthly": [
# 		"zatca_sa_phase2.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "zatca_sa_phase2.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "zatca_sa_phase2.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "zatca_sa_phase2.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["zatca_sa_phase2.utils.before_request"]
# after_request = ["zatca_sa_phase2.utils.after_request"]

# Job Events
# ----------
# before_job = ["zatca_sa_phase2.utils.before_job"]
# after_job = ["zatca_sa_phase2.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"zatca_sa_phase2.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

doc_events = {
    'Sales Invoice': {
        'on_submit': 'zatca_sa_phase2.zatca_sa_phase2.doctype.einvoices.create_invoices.zatca_Background_on_submit'
    },
    'Purchase Invoice': {
        'on_submit': 'zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.submit.on_submit'
    },
    "Item": {
        "after_insert": "zatca_sa_phase2.zatca_sa_phase2.update_price.update_item_price"
        # "on_update": "zatca_sa_phase2.zatca_sa_phase2.update_price.update_item_price"

    }
}

# after_install = "zatca_sa_phase2.zatca_sa_phase2.doctype.rename_fields"

#"filters": [["module", "=", "Zatca Sa Phase2"]],
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", ["Account-custom_code"]],
            ["name", "in", [
                "Sales Invoice-e_invoicing_details_tab",
                "Sales Invoice-zatca_details_section",
                "Sales Invoice-custom_zatca_status",
                "Sales Invoice-custom_zatca_tax_category",
                "Sales Invoice-custom_pih",
                "Sales Invoice-custom_ih",
                "Sales Invoice-custom_submit_time",
                "Sales Invoice-custom_icv",
                "Sales Invoice-custom_xml_file",
                "Sales Invoice-custom_qr_code_file",
                "Sales Invoice-custom_zatca_validation_result",
                "Sales Invoice-custom_invoice_transaction_type1",
                "Sales Invoice-custom_invoice_transaction_type2"
            ]]
        ]
    },
    {"dt": "Client Script", "filters": [["name", "in", ["Label Change","Make Readonly"]]]}
]





