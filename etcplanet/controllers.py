import etcplanet.json_rpc
import django.shortcuts
import re

B_BEG = '<tr class = "blue"><td class = "field">'
G_BEG = '<tr class = "grey"><td class = "field">'
MID   = '</td><td class = "value">'
END   = "</td></tr>"

def home(request):
        return django.shortcuts.render(request, "home.html", {})

def search(request):
        try:
                result = etcplanet.json_rpc.json_rpc(request.GET)
        except (KeyError, ValueError):
                result = {}

        return django.shortcuts.render(request,
                                       "search.html",
                                       {"result" : result,
                                        "b"      : B_BEG,
                                        "g"      : G_BEG,
                                        "m"      : MID,
                                        "e"      : END})
