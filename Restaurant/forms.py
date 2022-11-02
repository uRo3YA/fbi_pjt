from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['title', 'addr','category','image']    
#     def __init__(self, *args, **kwargs):
#         super(RestaurantForm, self).__init__(*args, **kwargs)
#         self.fields['name'].label = '상호명'
#         self.fields['name'].widget.attrs.update({
#             'placeholder': '상호명을 입력해주세요.',
#             'class': 'form-control',
#             'id': 'form_title',
#             'autofocus': True,
#             'style': "width: 91%;"
#         })
#         self.fields['address'].label = '주소지'
#         self.fields['address'].widget.attrs.update({
#             'placeholder': '주소지를 입력해주세요.',
#             'class': 'form-control',
#             'id': 'form_title',
#             'style': "width: 91%;"
#         })
#         self.fields['phone_number'].label = '전화번호'
#         self.fields['phone_number'].widget.attrs.update({
#             'placeholder': '전화번호를 입력해주세요.',
#             'class': 'form-control',
#             'id': 'form_title',
#             'style': "width: 91%;"
#         })
#         self.fields['menu'].label = '메뉴'
#         self.fields['menu'].widget.attrs.update({
#             'placeholder': '메뉴를 입력해주세요.',
#             'class': 'form-control',
#             'id': 'form_title',     
#             'style': "width: 91%;"
#         })
#         self.fields['category'].label = '분류'
#         self.fields['category'].widget.attrs.update({
           
#             'class': 'form-control',
#             'id': 'form_title',     
#             'style': "width: 91%;"
#         })

#     class Meta:
#         model = Restaurant
#         fields = ['name', 'address', 'phone_number','category','menu', 'image']