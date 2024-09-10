from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import MarkDown, MarkDownForm
from spellchecker import SpellChecker
from markdown import markdown

# Create your views here.
def list_markdown(request):
    markdown = MarkDown.objects.all()
    return render(request, 'markdown_list.html', {'markdown': markdown})

@csrf_exempt
def upload_markdown(request):
    form = MarkDownForm()
    if request.method == 'POST':
        form = MarkDownForm(request.POST, request.FILES)
        if form.is_valid():
            markdown = form.save()
            filename = request.FILES['file'].name
            markdown.filename = filename
            markdown.save()
            return redirect('list-markdown')
        return JsonResponse({'error': 'Invalid form submission'}, status=400)
    return render(request, 'upload.html', {'form': form})

@csrf_exempt
def check_grammar(request, file_id):
    try:
        file_instance = MarkDown.objects.get(id=file_id)
        # Read the file content directly from the file object
        content = file_instance.file.read().decode('utf-8')
        spell = SpellChecker()
        words = content.split()
        corrected_words = [spell.candidates(word).pop() if spell.candidates(word) else word for word in words]
        corrected_text = " ".join(corrected_words)
        return HttpResponse(corrected_text, content_type='text/html')
    except MarkDown.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)

# @csrf_exempt
# def save_note_view(request):
#     if request.method == 'POST':
#         form = NoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             filename = file.name
#             content = file.read().decode('utf-8')
#             note, created = Note.objects.get_or_create(filename=filename, defaults={'content': content})
#             if not created:
#                 note.content = content
#                 note.save()
#             return JsonResponse({'message': f'File {filename} uploaded successfully'})
#         return JsonResponse({'error': 'Invalid form submission'}, status=400)
#     return render(request, 'notes/upload.html')

def render_note(request, file_id):
    try:
        file_instance = MarkDown.objects.get(id=file_id)
        file_content = file_instance.file.read().decode('utf-8')
        # Convert Markdown content to HTML
        html_content = markdown(file_content)
        return HttpResponse(html_content, content_type='text/html')
    except MarkDown.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)
