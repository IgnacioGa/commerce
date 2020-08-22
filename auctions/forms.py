from django import forms

from .models import Category

class Bids(forms.Form):
    updrageBid = forms.DecimalField(max_digits=8, decimal_places=2, required=True, label=False) 
    	
    def __init__(self, *args, **kwargs):
    	super(Bids, self).__init__(*args, **kwargs)
    	self.fields['updrageBid'].widget.attrs = {
			'placeholder': 'Bid',
       		'class': 'form-control'
       		}



class CreateLis(forms.Form):
	Title = forms.CharField(max_length=80,  required=True)
	Description = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":20}), required=True,)
	InitialBid = forms.DecimalField(max_digits=8, decimal_places=2, required=True)
	URLImagen =  forms.CharField(max_length=200)
	Category = forms.ModelChoiceField(queryset=Category.objects.all())

	def __init__(self, *args, **kwargs):
		super(CreateLis, self).__init__(*args, **kwargs)
		self.fields['Title'].widget.attrs = {
			'class': 'form-control'
			}

		self.fields['Description'].widget.attrs = {
			'class': 'form-control'
			}

		self.fields['InitialBid'].widget.attrs = {
			'class': 'form-control'
			}
		self.fields['URLImagen'].widget.attrs = {
			'class': 'form-control'
			}