from django import forms

class AddMangaTitleForm(forms.Form):
    title_name = forms.CharField(max_length=255)
    URL = forms.URLField(max_length=255)
    last_read = forms.CharField(max_length=255)
    image_link = forms.URLField(max_length=255)


class AddMangaChapterForm(forms.Form):
    chapter_number = forms.CharField(max_length=255)
    URL = forms.URLField(max_length=255)