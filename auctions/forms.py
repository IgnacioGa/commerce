from django import forms

class Bids(forms.Form):
    updrageBid = forms.DecimalField(max_digits=8, decimal_places=2, required=True, label=False) 
    	
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['updrageBid'].widget.attrs.update({'placeholder': 'Bid'})
        self.fields['updrageBid'].widget.attrs.update({'class': 'form-control'})