from django.contrib import admin

from .models import Character, Skill, Inventory


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    min_num = 1
    fields = ('talent', 'name', 'value', 'include_talent_markup')


class InventoryInline(admin.StackedInline):
    model = Inventory
    max_num = 1
    min_num = 1
    can_delete = False


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'ready_to_play', 'kind', 'creator')
    list_filter = ('kind', 'ready_to_play', 'creator')
    fieldsets = (
        ('GENERAL', {
            'fields': ('creator', 'kind')
        }),
        ('CHARACTER INFORMATION', {
            'fields': ('portrait', 'name', 'gender', 'age', 'appearance',
                       'profession', 'marital_status', 'religion')
        }),
        ('NOTES', {
            'fields': ('game_master_notes', 'player_notes')
        }),
        ('WALLET', {
            'fields': ('money',)
        })
    )
    inlines = [SkillInline, InventoryInline]


admin.site.register(Character, CharacterAdmin)

