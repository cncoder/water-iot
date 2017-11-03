import requests
import time
def wechatreporter(text,desp):
    WECHAT_URL = 'https://sc.ftqq.com/SCU7014T8ba253e09742d7e426b9e7de539900bd58d6c530305d1.send'
    param  = {'text':text, 'desp':desp}

    r = requests.get (WECHAT_URL, params = param)
    print r.content