from django import forms

class BidForm(forms.Form):
    bid = forms.IntegerField(label="Your Bid ")

class LoginForm(forms.Form):
    username = forms.CharField(label="Username ", widget=forms.TextInput(
        attrs={
            "class": 'form-control'
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            "class": 'form-control'
        }
    ))
    
class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={
            "class": 'form-control'
        }
    ))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={
            "class": 'form-control'
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            "class": 'form-control'
        }
    ))
    confirmation = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={
            "class": 'form-control'
        }
    ))

class CreateForm(forms.Form):
    title = forms.CharField(label="Title ", widget=forms.TextInput(
        attrs={
            "class": 'form-control'
        }
    )) 
    category = forms.ChoiceField(label="Category ",choices=(
        ("Antiques","Antiques"),
        ("Books","Books"),
        ("Crafts","Crafts"),
        ("Electronics","Electronics"),
        ("Jewellery","Jewellery"),
        ("Paintings", "Paintings")
    ), widget=forms.Select(
        attrs={
            "class": 'form-control'
        }
    )) 
    details = forms.CharField(label="Description ", widget=forms.Textarea(
        attrs={
            "class": 'form-control'
        }
    ))
    display = forms.ImageField(label="Upload a picture ", widget=forms.ClearableFileInput(
        attrs={
            "class": 'form-control-file'
        }
    ))
    minbid = forms.IntegerField(label="Starting Bid (₹) ", widget=forms.NumberInput(
        attrs={
            "class": 'form-control'
        }
    ))