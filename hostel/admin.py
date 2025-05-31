from django.contrib import admin
from .models import University, Hostel, Room, Student, HostelApplication

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'contact_phone', 'is_verified')
    search_fields = ('name', 'location', 'contact_email')
    list_filter = ('is_verified',)
    actions = ['verify_university']

    def verify_university(self, request, queryset):
        queryset.update(is_verified=True)
    verify_university.short_description = "Mark selected universities as verified"

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'total_capacity', 'available_capacity')
    search_fields = ('name', 'university__name')
    list_filter = ('university',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hostel', 'room_type', 'capacity', 'available_capacity', 'floor')
    search_fields = ('room_number', 'hostel__name')
    list_filter = ('room_type', 'hostel', 'floor')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'student_id', 'phone_number', 'is_verified')
    search_fields = ('user__username', 'student_id', 'user__email')
    list_filter = ('university', 'is_verified')
    actions = ['verify_students']

    def verify_students(self, request, queryset):
        queryset.update(is_verified=True)
    verify_students.short_description = "Mark selected students as verified"

@admin.register(HostelApplication)
class HostelApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'hostel', 'room', 'status', 'application_date', 'verification_date')
    search_fields = ('student__user__username', 'hostel__name')
    list_filter = ('status', 'hostel', 'application_date')
    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', verification_date=timezone.now())
    approve_applications.short_description = "Approve selected applications"

    def reject_applications(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='rejected', verification_date=timezone.now())
    reject_applications.short_description = "Reject selected applications"
