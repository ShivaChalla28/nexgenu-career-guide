import urllib.request
import json
import traceback

try:
    response = urllib.request.urlopen('http://localhost:8000/api/admin/stats')
    data = json.loads(response.read())
    with open('stats_output.json', 'w') as f:
        json.dump(data, f, indent=2)
except Exception as e:
    with open('stats_output.json', 'w') as f:
        f.write(str(e) + "\n" + traceback.format_exc())
