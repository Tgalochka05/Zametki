from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
import json

def get_notes_from_cookie(request): #Получаем куки файлы (если их нет, возвращаем пустой список)
    notes_cookie = request.COOKIES.get('user_notes', '[]')
    try:
        return json.loads(notes_cookie)
    except:
        return []

def save_notes_to_cookie(response, notes): #Записываем и сохраняем куки файлы
    response.set_cookie('user_notes', json.dumps(notes), max_age=365*24*60*60) #max_age - срок хранения куки в секундах (установлен год)
    return response

def note_list(request): #Отображаем список заметок и отображем тему сайта
    
    # Получаем текущую тему из cookies или используем светлую по умолчанию
    theme = request.COOKIES.get('theme', 'light')
    
    # Получаем заметки из cookies
    notes = get_notes_from_cookie(request)

    # Флаг для определения, нужно ли обновлять cookies
    update_cookies = False
    
    if 'set_theme' in request.GET:
        theme = request.GET['set_theme']
        update_cookies = True
    
    context = { #Данные для шаблонов
        'notes': notes,
        'current_theme': theme,
        'themes': [
            {'value': 'light', 'name': 'Светлая', 'class': 'theme-light'},
            {'value': 'dark', 'name': 'Темная', 'class': 'theme-dark'},
            {'value': 'blue', 'name': 'Синяя', 'class': 'theme-blue'},
            {'value': 'green', 'name': 'Зеленая', 'class': 'theme-green'},
        ]
    }
    
    response = render(request, 'note_list.html', context) #Делаем рендер html-страницы (т.е. отображем её вместе с вставленными данными)
    
    # Если нужно обновить cookies - обновляем
    if update_cookies:
        if 'set_theme' in request.GET:
            response.set_cookie('theme', theme, max_age=365*24*60*60)
    
    return response

def add_note(request): #Делаем новую заметку
    if request.method == 'POST':
        #Берём информацию от пользователя из полей формы по запросу
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content: #Проверка на пустоту
            # Получаем текущие заметки
            notes = get_notes_from_cookie(request)
            
            # Создаем новую заметку
            new_note = {
                'id': len(notes) + 1,
                'title': title,
                'content': content
            }
            
            notes.append(new_note) #Добавляем её в список
            
            # Перенаправляем с сохранением cookies
            response = redirect('note_list')
            return save_notes_to_cookie(response, notes)
    
    return redirect('note_list')

def delete_note(request, note_id): #Удаляем заметку
    notes = get_notes_from_cookie(request) #Получаем текущий список заметок
    notes = [note for note in notes if note['id'] != note_id] #Перезаполняем, исключая удалённую заметку
    
    response = redirect('note_list')
    return save_notes_to_cookie(response, notes)
