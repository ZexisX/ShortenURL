# 
#  Created by Le Vinh Khang on 23/03/2024.
#  The interface was created by v0.dev, not me!
#  But all the functionalities were made by me.
#
# 
#                         _ooOoo_       
#                        o8888888o                       
#                        88" . "88                       
#                        (| -_- |)
#                        O\  =  /O
#                     ____/`---'\____
#                   .'  \\|     |//  `.
#                  /  \\|||  :  |||//  \
#                 /  _||||| -:- |||||_  \
#                 |   | \\\  -  /'| |   |
#                 | \_|  `\`---'//  |_/ |
#                 \  .-\__ `-. -'__/-.  /
#               ___`. .'  /--.--\  `. .'___
#            ."" '<  `.___\_<|>_/___.' _> \"".
#           | | :  `- \`. ;`. _/; .'/ /  .' ; |
#           \  \ `-.   \_\_`. _.'_/_/  -' _.' /
# ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
#                         `=--=-'                    

import sqlite3
from flask import Flask, request, redirect, render_template_string
import string
import random

app = Flask(__name__)

ket_noi = sqlite3.connect('urls.db', check_same_thread=False)
con_tro = ket_noi.cursor()
con_tro.execute('''CREATE TABLE IF NOT EXISTS urls
             (short_url TEXT PRIMARY KEY, long_url TEXT)''')
ket_noi.commit()

def tao_url_ngan():
    ky_tu = string.ascii_letters + string.digits
    url_ngan = ''.join(random.choice(ky_tu) for _ in range(6))
    return url_ngan

@app.route('/')
def trang_chu():
    return render_template_string('''
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rút gọn URL</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .toast {
            position: fixed;
            top: -100px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #000;
            color: #fff;
            padding: 10px 20px;
            border-radius: 5px;
            transition: top 0.5s ease;
            z-index: 9999;
        }

        .toast.show {
            top: 20px;
        }

        .toast-thanh_cong {
            background-color: #48BB78;
        }

        .toast-loi {
            background-color: #F56565;
        }
    </style>
</head>
<body class="bg-white flex justify-center items-center h-screen">
    <div class="rounded-lg border bg-card text-card-foreground shadow-sm w-full max-w-lg" data-v0-t="card">
        <div class="p-4 grid gap-4">
            <div class="space-y-2">
                <label class="font-medium peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-sm" for="url">
                    URL gốc
                </label>
                <input class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" id="url" placeholder="Nhập URL để rút gọn">
            </div>
            <div class="space-y-2">
                <label class="font-medium peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-sm" for="shortened">
                    URL rút gọn
                </label>
                <div class="flex items-center space-x-2">
                    <input class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" id="shortened" readonly="">
<button onclick="saoChepUrlNgan()" class="inline-flex items-center justify-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-black text-white h-9 rounded-md px-3" id="copyButton" style="color: white;">
    Sao chép
</button>
                </div>
            </div>
<button onclick="rutGonUrl()" class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-black text-white h-10 px-4 py-2 w-full" id="shortenButton">
    Rút gọn
</button>

            <div id="loading" class="hidden">
                <div class="spinner-border text-primary mt-2" role="status">
                    <span class="sr-only">Đang tải...</span>
                </div>
            </div>
        </div>
    </div>

    <div id="copySuccessPopup" class="toast toast-thanh_cong">Sao chép URL thành công!</div>
    <div id="shortenSuccessPopup" class="toast toast-thanh_cong">Rút gọn URL thành công!</div>
    <div id="shortenErrorPopup" class="toast toast-loi">Lỗi khi rút gọn URL!</div>

    <script>
        function hienThongBao(message, type) {
            var toast = document.createElement('div');
            toast.className = 'toast show';
            toast.classList.add(type);
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(function() {
                toast.classList.remove('show');
                setTimeout(function() {
                    document.body.removeChild(toast);
                }, 500);
            }, 3000);
        }

        function rutGonUrl() {
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('shortenButton').disabled = true;
            var url_goc = document.getElementById('url').value;
            fetch('/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ long_url: url_goc })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('shortened').value = data.shortened_url;
                hienThongBao('Rút gọn URL thành công!', 'toast-thanh_cong');
            })
            .catch(error => {
                hienThongBao('Lỗi khi rút gọn URL!', 'toast-loi');
            })
            .finally(() => {
                document.getElementById('loading').classList.add('hidden');
                document.getElementById('shortenButton').disabled = false;
            });
        }

        function saoChepUrlNgan() {
            var url_rutgon = document.getElementById('shortened');
            url_rutgon.select();
            document.execCommand('copy');
            hienThongBao('Sao chép URL thành công!', 'toast-thanh_cong');
        }
    </script>
</body>
</html>
''')

@app.route('/shorten', methods=['POST'])
def rut_gon_url():
    url_goc = request.json['long_url']
    url_rutgon = tao_url_ngan()

    con_tro.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (url_rutgon, url_goc))
    ket_noi.commit()

    return {'shortened_url': f'{request.host}/{url_rutgon}'}

@app.route('/<url_rutgon>')
def chuyen_huong_den_url_goc(url_rutgon):
    con_tro.execute("SELECT long_url FROM urls WHERE short_url=?", (url_rutgon,))
    row = con_tro.fetchone()
    if row:
        return redirect(row[0])
    else:
        return 'Không tìm thấy URL rút gọn', 404

if __name__ == '__main__':
    app.run(debug=True)

