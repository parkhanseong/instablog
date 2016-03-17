from django import forms
from .models import Post
from django.forms import ValidationError


class PostForm(forms.Form):
    title = forms.CharField(label='글제목')
    # title = forms.CharField(required=False) 검사안하고 무조건 통과.
    content = forms.CharField(widget=forms.Textarea)
    # widget은 해석? 변경?의 역할

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'tags', )
        #전체를 담고 싶을때, all 사용. but created_at 과 같은것은 받을 수 없음.
        # fields = '__all__'
        # exclud = ('title', 'category')

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if '바보' in title:
            raise ValidationError('바보 냄새가 난다. 다시 입력해주세요.')
        return title.strip()

    def clean(self):
        super(PostEditForm, self).clean()
        title = self.cleaned_data.get('title', '')
        content = self.cleaned_data.get('content', '')

        if '안녕' in title:
            self.add_error('title', '안녕은 이제 그만~')
        if '안녕' in content:
            self.add_error('content', '안녕은 이제 그만~')
