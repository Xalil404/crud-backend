from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'day', 'description')
    search_fields = ('user__username', 'description')

    fieldsets = (
        (None, {
            'fields': ('user', 'month', 'day', 'description')  # Include all fields in the admin form
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
