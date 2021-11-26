from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_MESSAGE = "Please fill in the form. It can't be empty"
DUPLICATE_ITEM_MESSAGE = "You've already got this in your list"
FORM_PLACEHOLDER = "Enter a to-do item here..."


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={'placeholder': FORM_PLACEHOLDER,
                                                  'class': 'form-control input-lg'})
        }

        error_messages = {
            'text': {'required': EMPTY_ITEM_MESSAGE}
        }

    def save_to_this_list(self, list_):
        self.instance.list = list_
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_MESSAGE]}
            self._update_errors(e)
