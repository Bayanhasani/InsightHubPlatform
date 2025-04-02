from django.contrib import admin
from .models import CustomUser, Verification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified')
    actions = ['verify_users', 'unverify_users']
    
    def verify_users(self, request, queryset):
        for user in queryset:
            user.is_verified = True
            user.save()  # This will update verifications via CustomUser.save()
        self.message_user(request, f"Verified {queryset.count()} users")
    
    def save_model(self, request, obj, form, change):
        obj.clean()  # Runs validation, for email verfiying
        super().save_model(request, obj, form, change)

    def unverify_users(self, request, queryset):
        for user in queryset:
            user.is_verified = False
            user.save()
        self.message_user(request, f"Unverified {queryset.count()} users")

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    actions = ['approve_verifications', 'reject_verifications']
    
    def approve_verifications(self, request, queryset):
        for verification in queryset:
            verification.status = 'approved'
            verification.save()  # This updates user via Verification.save()
        self.message_user(request, f"Approved {queryset.count()} verifications")
    
    def reject_verifications(self, request, queryset):
        for verification in queryset:
            verification.status = 'rejected'
            verification.save()
        self.message_user(request, f"Rejected {queryset.count()} verifications")