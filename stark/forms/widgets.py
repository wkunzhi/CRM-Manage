# by 362416272@qq.com
from django import forms


class DateTimePickerInput(forms.TextInput):
    template_name = 'stark/forms/widgets/datetime_picker.html'
