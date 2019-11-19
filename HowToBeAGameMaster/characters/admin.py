from django.contrib import admin

from .models import Character, Skill, Inventory


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    min_num = 1
    fields = ('talent', 'name', 'value')


class InventoryInline(admin.StackedInline):
    model = Inventory
    verbose_name_plural = 'Inventory'
    max_num = 1
    min_num = 1
    can_delete = False


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'talent_act', 'talent_knowledge', 'talent_social')
    list_filter = ('kind', )
    fieldsets = (
        ('CHARACTER INFORMATION', {
            'fields': ('kind', 'portrait', 'name', 'gender', 'age', 'appearance',
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

