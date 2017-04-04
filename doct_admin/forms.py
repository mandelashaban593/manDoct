
from django import forms
from Doct.models import  Register,UserActions,LoginInfo
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry


class ChangeAdminTelephoneForm(forms.Form):
	old_phone=forms.CharField(max_length=128)
	new_phone=forms.CharField(max_length=128)



class ChangeAdminPassword(forms.Form):
	old_pass=forms.CharField(max_length=128)
	new_pass=forms.CharField(max_length=128)



class CreateAdminUserForm(forms.Form):

    """
    Form for migrating user phonebook
    """

    fname = forms.CharField(required=True, max_length=255)
    sname = forms.CharField(required=True, max_length=255)
    page = forms.CharField(required=True, max_length=255)
    gender = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=True, max_length=255)
    username = forms.CharField(required=True, max_length=255)
    street = forms.CharField(required=True, max_length=255)
    specialty = forms.CharField(required=True, max_length=255)
    password = forms.CharField(required=True, max_length=255)
    password2 = forms.CharField(required=True, max_length=255)
    profile_pic = forms.CharField(required=True, max_length=255)
    role = forms.CharField(required=True, max_length=255)
   

    def clean(self):

        # check passwords
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data




class EditAdminUserForm(forms.Form):

    """
    Form for migrating user phonebook
    """

    fname = forms.CharField(required=True, max_length=255)
    sname = forms.CharField(required=True, max_length=255)
    page = forms.CharField(required=True, max_length=255)
    gender = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=True, max_length=255)
    username = forms.CharField(required=True, max_length=255)
    street = forms.CharField(required=True, max_length=255)
    specialty = forms.CharField(required=True, max_length=255)
    password = forms.CharField(required=True, max_length=255)
    password2 = forms.CharField(required=True, max_length=255)
    profile_pic = forms.CharField(required=True, max_length=255)
    role = forms.CharField(required=True, max_length=255)
   

    def clean(self):

        # check passwords
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

 
 
class UserActionsForm(forms.ModelForm):

    """Form for saving user details on signup"""
    class Meta:
        model = UserActions
        fields = ['session', 'log_entry', 'user']


class LoginInfoForm(forms.ModelForm):

    """Form for saving user details on login"""
    class Meta:
        model = LoginInfo
        fields = ['user_agent', 'remote_addr', 'user']


class LogEntryForm(forms.ModelForm):

    """Form for saving user details on signup"""
    class Meta:
        model = LogEntry
        fields = ['user', 'content_type', 'object_id',
                  'object_repr', 'action_flag', 'change_message']
