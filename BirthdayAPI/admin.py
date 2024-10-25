from django.contrib import admin
from .models import Birthday

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'description')  # Use existing fields
    search_fields = ('user__username', 'description')  # Enable searching by username and description
    list_filter = ('date',)  # Filter by date

    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'description')  # Include all fields in the admin form
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
