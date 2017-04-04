from django import forms
from Doct.models import Page, UserProfile, Topup, Register, Illness, Diognosis,Contact,converse,convPersonFrien,Messages,Contact
from django.contrib.auth.models import User





class PageForm(forms.ModelForm):
	title=forms.CharField(max_length=128, help_text="Please enter the title of the oage.")
	url=forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	views=forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	def clean(self):
		cleaned_data=self.cleaned_data
		url=cleaned_data.get('url')

		# if url is not empty and doesn't start with 'http://', prepend 'http://'.
		if url and not url.startswith('http://'):
			url='http://' + url
			cleaned_data['url']=url



		return cleaned_data

	class Meta:
		#Provide an association between the ModelForm and a model
		model=Page

		# What fields do we want to include in our form?
		# This way we don't need every field in the model present
		# Some fields may allow NULL values, so we may not want to include them...
		# Here, we are hidding the foreign key.
		fields={'title', 'url', 'views'}





class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Username.")
	email = forms.CharField(help_text="Email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Password.")
	class Meta:
		model = User
		fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
	website = forms.URLField(help_text="Please enter your website.", required=False)
	picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
	class Meta:
		model = Register
		fields = ['username', 'email', 'password']




# class UserProfileForm(forms.ModelForm):
# 	class Meta:
# 		model = UserProfile
# 		fields = ('fname', 'picture')



class PatientForm(forms.ModelForm):
	class Meta:
		model = Register
		fields = ('fname', 'sname', 'page', 'gender', 'telno','username','password','email', 'street', 'city', 'state', 'zip_code', 'role', 'specialty')

class DoctorForm(forms.ModelForm):
	class Meta:
		model = Register
		fields = ('fname', 'sname', 'page', 'gender', 'telno','username','password','email', 'street', 'city', 'state', 'zip_code', 'role', 'specialty', 'profile_pic')


class IllnessForm(forms.ModelForm):
	class Meta:
		model = Illness
		fields = ('gender', 'pname','illness','amb','username', 'page')


class DiognosisForm(forms.ModelForm):
	class Meta:
		model = Diognosis
		fields = ('dname', 'telno','gender', 'diognosis','page','email', 'amb')



class TopupForm(forms.ModelForm):

	class Meta:
# Provide an association between the ModelForm and a model
		model = Topup
		fields = ['amount_sent', 'receiver_number', 'receiver_fname', 'receiver_lname', 'sender_fullname', 'receiver_country_code']








class AddIllDetForm(forms.ModelForm):

    """
    Form for adding  Illness details
    """
    class Meta:
        model = Illness
        fields = ['gender','kin','kintelno','username','email']


class ContactForm(forms.ModelForm):

    """
    Form for adding  Illness details
    """
    class Meta:
        model = Contact
        fields = ['telno','email','msg']

class LoginForm(forms.ModelForm):

    """
    Form for adding  Illness details
    """
    class Meta:
        model = Register
        fields = ['username','password','role','page']




class patientConverseForm (forms.ModelForm):

    """
    Form for adding  Illness details
    """
    class Meta:
        model = converse
        fields = ['username','dusername','pmsg']


class doctorConverseForm (forms.ModelForm):

    """
    Form for adding  Illness details
    """
    class Meta:
        model = converse
        fields = ['username','dusername','dmsg']


class MessagesForm(forms.ModelForm):

    """
    Form for adding  Illness details
    """
    class Meta:
        model = Messages
        fields = ['password_phone','password_phone','msg']


