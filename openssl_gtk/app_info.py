#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bu dosya uygulama hakkında bilgi tutan değişkenleri içerir.
"""
import os

__author__ = "Muhammed Çamsarı"
__appname__ = "OpenSSL-GTK"
__definition__ = "Terminal kullanmadan Openssl işlemlerinizi gerçekleştirin."
__copyright__ = "Copyright (c) 2019 " + __author__
__license__ = "MIT"
__version__ = "1.1"
__status__ = "Beta"
__email__ = "muhammedcamsari@icloud.com"
__pgp__ = 'F294 1D36 A8C8 101B EEB0  16A7 B260 DBA5 2DAA 962A'
__legalnote__ = __appname__ + ' hiçbir garanti vermez.\nKullanım amacı tamamen kullanıcının sorumluluğundadır. \nDaha fazla bilgi için ' + __license__ + ' lisansını inceleyiniz.'
__logo__ = os.path.dirname(__file__) + '/logo.png'

cipher_list = ['aes-128-cbc', 'aes-128-ecb', 'aes-192-cbc', 'aes-192-ecb', 'aes-256-cbc (Önerilen)', 'aes-256-ecb']
digest_list = ['md5', 'md_gost94', 'ripemd160', 'sha1', 'sha224', 'sha256 (Önerilen)', 'sha384', 'sha512', 'streebog256', 'streebog512', 'whirlpool']

genrsa_list = ['aes128', 'aes192', 'aes256', 'aria128', 'aria192', 'aria256', 'camellia128', 'camellia192', 'camellia256', 'des', 'des3', 'idea']
genrsa_size_list = ['1024', '2048', '3072', '4096']

surum_notlari = """
  1.1 sürümü, aşağıdaki değişiklikleri barındırır.

 * GenRSA modeli eklendi.
 * GenRSA modeli ile açık anahtarı dışa aktarabilme özelliği eklendi.
 * Log yönetimi için Opy-Logger entegrasyonu tamamlandı.
 * Hakkımızda ve sürüm notları penceresindeki görüntü sorunu giderildi.
 * Dosya seçme penceresindeki PyGTKDeprecationWarning hatası giderildi.
 * Hata mesajları penceresindeki PyGTKDeprecationWarning hataları giderildi.
 * Sürüm notları penceresindeki başlık metnine durum bilgisi eklendi.
 * Hakkında penceresindeki yasal uyarı metninde düzenlemeler yapıldı.


OpenSSL-GTK hala geliştirme aşamasında ve hatayla karşılaşma olasılığınız yüksek.
Lütfen karşılaştığınız hataları geliştiriye bildirin: muhammedcamsari@icloud.com
"""
