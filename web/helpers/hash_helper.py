# -*- coding: utf-8 -*-
import hashlib
import hmac
import base64


def get_content_md5(data):
    m = hashlib.md5()
    m.update(data)
    signature = base64.b64encode(m.digest())
    return signature


def get_api_sign(secret, data):
    keys = sorted(data.keys())

    post = []
    for key in keys:
        if isinstance(data[key], unicode):
            post.append('%s=%s' % (key, data[key].encode('utf-8')))
        else:
            post.append('%s=%s' % (key, data[key]))

    H = hmac.new(secret, digestmod=hashlib.sha512)
    H.update('&'.join(post))
    return H.hexdigest()
