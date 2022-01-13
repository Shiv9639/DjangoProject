from django.contrib import admin
from .models import Topic, Course, Student, Order


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'hours', 'topic', 'price', 'for_everyone')
    actions = ['add_50_to_hours']
    search_fields = ('name__startswith',)

    def add_50_to_hours(self, request, queryset):
        for hour in queryset.all():
            queryset.update(hours=(int(hour.hours) + 10))

    add_50_to_hours.short_description = 'Add 10 Hours'


class OrderAdmin(admin.ModelAdmin):
    fields = [('Student', 'order_status'), ('order_date')]
    list_display = ('id', 'Student', 'order_status', 'order_date', 'total_cost')
    search_fields = ('student__first_name__startswith',)


class StudentAdmin(admin.ModelAdmin):
    def upper_case_name(self, obj):
        return obj.first_name.upper() + " " + obj.last_name.upper()

    upper_case_name.short_description = 'Student Full Name'
    fields = ['first_name', 'last_name', 'image', 'address', 'province', 'registered_courses', 'interested_in']
    list_display = ('upper_case_name', 'address', 'province')
    search_fields = ('name__startswith',)


admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
