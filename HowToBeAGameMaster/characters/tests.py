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

    def test_character_talent_calculation_skill_markups(self):
        full_character = create_full_character()
        character = full_character[0]
        skill_talent_markup_diff_values = character.calculate_talents()
        self.assertEqual(skill_talent_markup_diff_values, (13, 13, 14))
        test_character = Character.objects.get(pk=character.pk)
        for skill in test_character.skill_set.all():
            if skill.name == 'Skill1' or skill.name == 'Skill2' or skill.name == 'Skill3':
                self.assertEqual(skill.value, 100)
            elif skill.name == 'Skill4' or skill.name == 'Skill5':
                self.assertEqual(skill.value, 43)
            else:
                self.assertEqual(skill.value, 54)

    def test_character_rescue_point_calculation(self):
        full_character = create_full_character()
        character = full_character[0]
        character.calculate_talents()
        character.calculate_rescue_points()
        # without reload of character
        self.assertEqual(character.rescue_points, 3)
        # with reload of character
        test_character = Character.objects.get(pk=character.pk)
        self.assertEqual(test_character.rescue_points, 3)


class SkillModelTests(TestCase):
    def test_skill_str_representation(self):
        skill = Skill(name='Test Skill')
        self.assertEqual(str(skill), 'Test Skill')

    def test_skill_talent_markup_calc_exceeding(self):
        full_character = create_full_character()
        skills = full_character[1]
        diff = skills[0].add_talent_markup(10)
        self.assertEqual(skills[0].value, 100)
        self.assertEqual(diff, 10)

    def test_skill_talent_markup_calc_not_exceeding(self):
        full_character = create_full_character()
        skills = full_character[1]
        diff = skills[3].add_talent_markup(10)
        self.assertEqual(skills[3].value, 40)
        self.assertEqual(diff, 0)


class InventoryModelTests(TestCase):
    def test_inventory_str_representation(self):
        char = Character(name='Test Char')
        inv = Inventory(character=char)
        self.assertEqual(str(inv), 'Test Char')

    def test_inventory_verbose_name_plural(self):
        self.assertEqual(str(Inventory._meta.verbose_name_plural), 'Inventories')
