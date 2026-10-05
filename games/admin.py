from django.contrib import admin
from .models import User, History, Guess

# Register your models here.
class HistoryAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'total_attempts', 'is_solved')
	ordering = ('date',)

class GuessAdmin(admin.ModelAdmin):
	list_display = ('user', 'guess_word', 'result', 'attempt_times')

admin.site.register(User)
admin.site.register(History, HistoryAdmin)
admin.site.register(Guess, GuessAdmin)