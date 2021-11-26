from django import forms
from lists.models import Item

EMPTY_ITEM_MESSAGE = "Please fill in the form. It can't be empty"


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={'placeholder': 'Enter a to-do item here...',
                                                  'class': 'form-control input-lg'})
        }

        error_messages = {
            'text': {'required': EMPTY_ITEM_MESSAGE}
        }

    def save_to_this_list(self, list_):
        self.instance.list = list_
        return super().save()
