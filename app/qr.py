import qrcode
import base64
from io import BytesIO
from PIL import Image
from django.shortcuts import render


def qrpp(self, request):
    img = qrcode.make("aaa")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    param = { 'qr': qr}
    return render(request, 'Index.html', param)
