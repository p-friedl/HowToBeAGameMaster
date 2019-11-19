from django.test import TestCase

from .models import Inventory


class InventoryModelTest(TestCase):

    def test_inventory_verbose_name_plural(self):
        self.assertEqual(str(Inventory._meta.verbose_name_plural), 'Inventories')
