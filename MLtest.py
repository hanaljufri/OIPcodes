import os
import json
import re
from pathlib import Path

file_paths = [
    os.path.join(Path().absolute(),'clean.jpg')
]
project_Id = '1fe4c61f-e2d4-4bc3-96aa-9200a5365fc9'
coder="""curl --silent --request POST\
    --url https://app.slickk.ai/api/project/entryPoint\
    --header 'Accept: */*'\
    --header 'Accept-Language: en-US, en;q=0.5'\
    --header 'Connection: keep-alive'\
    --header 'Content-Type: multipart/form-data'\
    --form 'projectId={1}'\
    {0}""".format(
       ' '.join(['--form data=@{0}'.format(path) for path in file_paths]),project_Id)

results = os.popen(coder).read()
results = re.sub(r'{"progress":\d+,"max":\d+}', "", results)

if len(results)==0:
    pass
elif len(results)>0:
    results = json.loads(results)
    print(len(results))
    print([result["text"] for result in results])