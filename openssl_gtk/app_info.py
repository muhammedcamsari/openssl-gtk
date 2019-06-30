#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bu dosya uygulama hakkında bilgi tutan değişkenleri içerir.
"""

__author__ = "Muhammed Çamsarı"
__appname__ = "OpenSSL-GTK"
__definition__ = "Terminal kullanmadan Openssl işlemlerinizi gerçekleştirin."
__legalnote__ = __appname__ + ' hiçbir garanti vermez.\nKullanım amacı tamamen kullanıcının sorumluluğundadır.\nDaha fazla bilgi için MIT lisansını inceleyiniz.'
__copyright__ = "Copyright (c) 2019 " + __author__
__license__ = "MIT"
__version__ = "1.0.2"
__status__ = "Beta"
__email__ = "muhammedcamsari@icloud.com"
__pgp__ = 'F294 1D36 A8C8 101B EEB0  16A7 B260 DBA5 2DAA 962A'
__logo__ = 'openssl_gtk/logo.png'

cipher_list = ['aes-128-cbc', 'aes-128-ecb', 'aes-192-cbc', 'aes-192-ecb', 'aes-256-cbc (Önerilen)', 'aes-256-ecb']
digest_list = ['md5', 'md_gost94', 'ripemd160', 'sha1', 'sha224', 'sha256 (Önerilen)', 'sha384', 'sha512', 'streebog256', 'streebog512', 'whirlpool']

surum_notlari = """
 * Bu sürüm itibariyle, Openssl enc modeliyle dosyalarınızı şifreleyebilecek ve şifresini çözebileceksiniz.

Bu beta sürüm ve hatayla karşılaşılma olasılığı oldukça yüksek.
Lütfen karşılaştığınız hataları geliştiriye bildirin: muhammedcamsari@icloud.com
"""
