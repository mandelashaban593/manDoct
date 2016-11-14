from django import forms
from Doct.models import Page, Category, UserProfile, Topup, Register, Illness, Diognosis
from django.contrib.auth.models import User



class CategoryForm(forms.ModelForm):
	name=forms.CharField(max_length=128, help_text="Please enter the category name.")
	views=forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes=forms.IntegerField(widget=forms.HiddenInput(), initial=0)



	# An initial class to provide additional information on the form
	class Meta:
		# Provide an association between the ModelForm and a model
		model=Category

		fields = "__all__" 


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
	password = forms.CharField(widget=forms.PasswordInput())


	class Meta:
		model = User
		fields = ('username', 'password')



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
		fields = ('fname', 'sname', 'page', 'gender', 'telno','username','password','email', 'street', 'city', 'state', 'zip_code', 'role', 'specialty')


class IllnessForm(forms.ModelForm):
	class Meta:
		model = Illness
		fields = ('email', 'pname','gender', 'illness','kin','kintelno','username', 'page', 'amb')



class DiognosisForm(forms.ModelForm):
	class Meta:
		model = Diognosis
		fields = ('dname', 'telno','gender', 'diognosis','page','email', 'amb')



class TopupForm(forms.ModelForm):

	class Meta:
# Provide an association between the ModelForm and a model
		model = Topup
		fields = ['amount_sent', 'receiver_number', 'receiver_fname', 'receiver_lname', 'sender_fullname', 'receiver_country_code']






