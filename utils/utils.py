import time, os
from flask import current_app
from PIL import ImageSequence
from .plugin import uploaded_avatars
# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)
    # 中文 windows 平台默认打开的文件编码是 gbk 所以需要指定一下

    # with open('log.log', 'a', encoding='utf-8') as f:
    #     # 通过 file 参数可以把输出写入到文件 f 中
    #     # 需要注意的是 **kwargs 必须是最后一个参数
    #     print(dt, *args, file=f, **kwargs)


def save_avatar(img, filename):
    path = current_app.config['UPLOADED_AVATAR_DEST']
    log(path)
    filename = uploaded_avatars.save(img, name=filename)

    return filename


def remove_avatar(filename):
    try:
        if filename != 'default_avatar.jpg':
            path = current_app.config['UPLOADED_AVATAR_DEST']
            p = os.path.join(path, filename)
            os.remove(p)
    except Exception as e:
        print(e)
