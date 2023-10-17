
from . import __version__ as app_version

app_name = "fuelbuddy"
app_title = "fuelbuddy"
app_publisher = "ibsl"
app_description = "fuelbuddy"
app_email = "ibsl@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/fuelbuddy/css/fuelbuddy.css"
# app_include_js = "/assets/fuelbuddy/js/fuelbuddy.js"

# include js, css files in header of web template
# web_include_css = "/assets/fuelbuddy/css/fuelbuddy.css"
# web_include_js = "/assets/fuelbuddy/js/fuelbuddy.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "fuelbuddy/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "fuelbuddy.utils.jinja_methods",
#	"filters": "fuelbuddy.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "fuelbuddy.install.before_install"
# after_install = "fuelbuddy.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "fuelbuddy.uninstall.before_uninstall"
# after_uninstall = "fuelbuddy.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "fuelbuddy.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Lead": {
		"after_insert": "fuelbuddy.fuel.chem",
#		"on_cancel": "method",
#		"on_trash": "method"
	},
	"Sales Order": {
		"after_insert": "fuelbuddy.fuel.sdf",
	},
	"Supplier": {
		"before_save": "fuelbuddy.fuel.supplier_onboarding",
	},
	"Purchase Receipt": {
		"after_insert": "fuelbuddy.fuel.margin",
	},
	"Delivery Fees Cal": {
		"before_save": "fuelbuddy.fuel.Delivery Fees Calculations",
	},
	"Sales Order":{
		"before_save": "fuelbuddy.fuel.POC",
	},
	"Journal Entry":{
		"after_insert": "fuelbuddy.fuel.journal_entry",
	},
	"Planning": {
		"after_insert": "fuelbuddy.fuel.oap",
	},
	"Finance": {
		"after_insert": "fuelbuddy.fuel.oauf",
	},
	"Customer": {
		"before_save": "fuelbuddy.fuel.on_boarding",
	},
	"Sales Order": {
		"before_save": "fuelbuddy.fuel.party_balance",
	},
	"Customer": {
		"before_save": "fuelbuddy.fuel.lead_cl",
	},
	"GL Entry": {
		"before_save": "fuelbuddy.fuel.ggl_ec",
	},
	"Opportunity": {
		"before_save": "fuelbuddy.fuel.activity",
	},
	"Opportunity": {
		"after_save": "fuelbuddy.fuel.item_opportunity",
	},
	"Address": {
		"before_save": "fuelbuddy.fuel.address_validation",
	},
	"Contact": {
		"before_save": "fuelbuddy.full_name",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"fuelbuddy.tasks.all"
#	],
#	"daily": [
#		"fuelbuddy.tasks.daily"
#	],
#	"hourly": [
#		"fuelbuddy.tasks.hourly"
#	],
#	"weekly": [
#		"fuelbuddy.tasks.weekly"
#	],
#	"monthly": [
#		"fuelbuddy.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "fuelbuddy.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "fuelbuddy.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "fuelbuddy.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["fuelbuddy.utils.before_request"]
# after_request = ["fuelbuddy.utils.after_request"]

# Job Events
# ----------
# before_job = ["fuelbuddy.utils.before_job"]
# after_job = ["fuelbuddy.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"fuelbuddy.auth.validate"
# ]
