# Copyright (c) 2013, Web Notes Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

template = "templates/generators/poll.html"
condition_field = "published"
no_cache = 1

class DuplicateVoteError(frappe.ValidationError): pass

class Poll(WebsiteGenerator):
	def get_context(self, context):
		context.maxvotes = max([d.votes for d in self.poll_options])
		context.sorted_options = sorted(self.poll_options,
			key=lambda d: (d.votes, -d.idx), reverse=True)
		return context

def insert_vote(option_name):
	vote = frappe.new_doc("Poll Vote")
	vote.option_name = option_name
	vote.poll = frappe.db.get_value("Poll Option", option_name, "parent")
	vote.insert(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def add_vote(option_name):
	try:
		insert_vote(option_name)
		return "Thank you for voting. Your vote has been registered!"
	except DuplicateVoteError:
		return "You have already voted on this poll"

