from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '상호명'
        self.fields['title'].widget.attrs.update({
            'placeholder': '상호명을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
            'style': "width: 91%;"
        })
        self.fields['addr'].label = '주소지'
        self.fields['addr'].widget.attrs.update({
            'placeholder': '주소지를 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'style': "width: 91%;"
        })
        self.fields['tel'].label = '전화번호'
        self.fields['tel'].widget.attrs.update({
            'placeholder': '전화번호를 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'style': "width: 91%;"
        })
        self.fields['description'].label = '설명'
        self.fields['description'].widget.attrs.update({
            'placeholder': '설명을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',     
            'style': "width: 91%; height:40%;"
        })
        self.fields['category'].label = '분류'
        self.fields['category'].widget.attrs.update({
           
            'class': 'form-control',
            'id': 'form_title',     
            'style': "width: 91%;"
        })
        self.fields['image'].label = '사진'
        self.fields['image'].widget.attrs.update({
           
            'class': 'form-control',
            'id': 'form_title',     
            'style': "width: 91%;"
        })

    class Meta:
        model = Restaurant
        fields = ['title', 'addr', 'category','tel','description', 'image']
    # class Meta:
    #     model = Restaurant
    #     fields = ['title', 'addr','category','image']    