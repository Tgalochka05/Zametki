from django import forms

class NoteForm(forms.Form): #Форма для заполнения заметок
    title = forms.CharField( #Оформление поля заголовка
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заголовок заметки'
        }),
        label='Заголовок'
    )
    
    content = forms.CharField( #Оформление поля содержания заметок
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите содержание заметки',
            'rows': 4
        }),
        label='Содержание'
    )