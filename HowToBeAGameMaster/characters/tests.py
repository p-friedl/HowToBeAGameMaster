from django.test import TestCase
from django.contrib.auth.models import User


from .models import Character, Skill, Inventory


def create_full_character():
    """
    Helper function to create a full character with skills and inventory
    Returns character, skills and inventory
    """
    user = User.objects.create_user(username='admin',
                                    email='admin@django.com',
                                    password='test')

    character = Character(name='Test Char',
                          gender='M',
                          marital_status='single',
                          kind='PC',
                          creator=user)
    character.save()

    skills = [
        Skill(character=character, talent='act', name='Skill1', value=100),
        Skill(character=character, talent='knowledge', name='Skill2', value=100),
        Skill(character=character, talent='social', name='Skill3', value=100),
        Skill(character=character, talent='act', name='Skill4', value=30),
        Skill(character=character, talent='knowledge', name='Skill5', value=30),
        Skill(character=character, talent='social', name='Skill6', value=40)
    ]
    for skill in skills:
        skill.save()

    inventory = Inventory(character=character)
    inventory.save()

    return character, skills, inventory


class CharacterModelTests(TestCase):
    def test_character_str_representation(self):
        char = Character(name='Test Char')
        self.assertEqual(str(char), 'Test Char')

    def test_character_talent_calculation(self):
        full_character = create_full_character()
        character = full_character[0]
        character.calculate_talents()
        # without reload of character
        self.assertEqual(character.talent_act, 13)
        self.assertEqual(character.talent_knowledge, 13)
        self.assertEqual(character.talent_social, 14)
        # with reload of character
        test_character = Character.objects.get(pk=character.pk)
        self.assertEqual(test_character.talent_act, 13)
        self.assertEqual(test_character.talent_knowledge, 13)
        self.assertEqual(test_character.talent_social, 14)


class SkillModelTests(TestCase):
    def test_skill_str_representation(self):
        skill = Skill(name='Test Skill')
        self.assertEqual(str(skill), 'Test Skill')


class InventoryModelTests(TestCase):
    def test_inventory_str_representation(self):
        char = Character(name='Test Char')
        inv = Inventory(character=char)
        self.assertEqual(str(inv), 'Test Char')

    def test_inventory_verbose_name_plural(self):
        self.assertEqual(str(Inventory._meta.verbose_name_plural), 'Inventories')
