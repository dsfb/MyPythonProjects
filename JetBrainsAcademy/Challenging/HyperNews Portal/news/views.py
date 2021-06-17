
import json
import simplejson
from collections import defaultdict
from datetime import datetime

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
class CommingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news')


class CreateNewView(View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as file:
            data_from_json = list(json.load(file))
            new = {'text': text, 'title': title, 'link': 9234732 + len(data_from_json),
                   'created': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}
            data_from_json.append(new)

        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json_file.write(simplejson.dumps(data_from_json, ensure_ascii=False, encoding="utf-8"))

        return redirect('/news')

    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/new.html'
        )

class NewView(View):
    def get(self, request, *args, **kwargs):
        if request.GET:
            if request.GET['q']:
                q = request.GET['q']
            else:
                q = None
        else:
            q = None
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            data_from_json = json.load(file)
            sorted_dates = sorted(data_from_json, key=lambda i: i['created'][:10], reverse=True)
            ddict = defaultdict(list)
            for obj in sorted_dates:
                if q is None:
                    ddict[obj['created'][:10]].append({'link': obj['link'], 'title': obj['title']})
                elif obj['title'].find(q) > -1:
                    ddict[obj['created'][:10]].append({'link': obj['link'], 'title': obj['title']})
            result = [{'date': k, 'list': v} for k, v in ddict.items()]
        return render(
            request, 'news/index.html',
            {'data': result}
        )


class NewDetailView(View):
    def get(self, request, *args, **kwargs):
        try:
            link = kwargs['link']
        except ValueError:
            raise Http404

        the_entry = None
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            file_contents = file.read()
            json_contents = json.loads(file_contents)
            for entry in json_contents:
                if entry['link'] == link:
                    the_entry = entry
                    break
        return render(
            request, 'news/detail.html',
            {'new': the_entry}
        )
