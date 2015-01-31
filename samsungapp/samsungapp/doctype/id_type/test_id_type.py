# Copyright (c) 2013, samsungapp and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Id Type')

class TestIdType(unittest.TestCase):
	pass
