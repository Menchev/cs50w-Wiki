import random
import markdown2
from django.shortcuts import render
from django import forms

from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': 'form-control'}), label="" ,max_length=64);

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': NewSearchForm(),
    })

def entry_page_view(request, TITLE):
    entry = util.get_entry(TITLE);
    if entry is not None:
        return render(request, "encyclopedia/entry_page.html", {
            'entry': entry,
            'title': TITLE,
            'form': NewSearchForm(),
        })
    elif entry is None:
        return render(request, "encyclopedia/entry_page.html", {
            'message': "No such entry exists!",
            'form': NewSearchForm(),
        })

def search(request):
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid() is True:
            title = form.cleaned_data["search"]
            entry = util.get_entry(title)
            if entry is not None:
                return render(request, "encyclopedia/entry_page.html", {
                    'entry': entry,
                    'title': title,
                    'form': NewSearchForm(),
                })
            # if the searched title is not present we can check for a substring
            elif entry is None:
                # get the substring
                substring = title
                # store the entries that match the substring
                entries = []
                list_entries = util.list_entries()
                # loop through all entry titles
                for entry in list_entries:
                    if substring.lower() in entry.lower():
                        entries.append(entry)
                # return the page with all mathching titles
                if entries:
                    return render(request, "encyclopedia/search.html", {
                        'entries': entries,
                        'title': title,
                        'form': NewSearchForm(),
                    })
                if not entries:
                    return render(request, "encyclopedia/entry_page.html", {
                        'message': "No such entry exists!",
                        'form': NewSearchForm(),
                    })

# form for e new page
class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}) ,max_length=64, label="")
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Body/Text'}), max_length=256, label="")

# creating a new page
def create_page_view(request):
    # sending info via POST method
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            # extracting the info
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            # check if an entry with this title already exists
            entries = util.list_entries()
            if title not in entries:
                # creating the new entry
                util.save_entry(title, body)
                # render the new entry's page
                entry = util.get_entry(title)
                return render(request, "encyclopedia/entry_page.html",{
                    'title': title,
                    'entry': entry,
                    'form': NewSearchForm(),
                })
            if title in entries:
                return render(request, "encyclopedia/create_page.html",{
                    'form': NewSearchForm(),
                    'form_page': NewPageForm(),
                    'message': "An entry with this title already exists!",
                })

    # getting the page via a GET method
    if request.method == "GET":
        return render(request, "encyclopedia/create_page.html", {
            'form_page': NewPageForm(),
            'form': NewSearchForm(),
        })

# edit a page
def edit_view(request, title):
    # find the entry
    entry = util.get_entry(title)
    edit_form = NewPageForm(initial={'title': title, 'body': entry})
    return render(request, "encyclopedia/edit.html", {
        'form_edit': edit_form,
        'form': NewSearchForm(),
    })

# updating an edited page
def update_view(request):
    # check if request is post
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title,body)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry_page.html", {
                'title': title,
                'entry': entry,
                'form': NewSearchForm()
            })

# generate a random page
def random_view(request):
    if request.method == 'GET':
        title = random.choice(util.list_entries())
        entry = util.get_entry(title)
        return render(request, "encyclopedia/entry_page.html", {
            'title': title,
            'entry': markdown2.markdown(entry),
            'form': NewSearchForm(),
        })