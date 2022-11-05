from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'id': 'form_title',
            'autofocus': True,
         
        })

        self.fields['image'].label = '첨부 이미지'
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
            'style': "width: 40%; "
        })
    class Meta:
        model = Review
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment 
        fields = ['content',]