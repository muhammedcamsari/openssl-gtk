# OpenSSL-GTK :tr:

**Terminal kullanmadan Openssl işlemlerinizi gerçekleştirin.**


## OpenSSL-GTK Nedir? 

OpenSSL-GTK, OpenSSL işlemlerini komut satırı kullanmaksızın gerçekleştirmenizi hedefleyen projedir.


## Desteklenen OpenSSL Modelleri

1.0 sürümüyle OpenSSL-GTK, yalnızca OPENSSL ENC modelini destekler. 

 - enc: Dosya şifreleme işlemleri için kullanılır.


## OpenSSL-GTK Kurulumu

### Linux

Kaynak kod indirilerek çalıştırılabilir. Bunu tercih etmezseniz pip ile kurulumu yapabilirsiniz. 

	pip3 install openssl-gtk

Ardından openssl-gtk.py komutuyla uygulamayı başlatmalısınız. Menü kısayolu şu an desteklenmemektedir. 


### MacOS

İlerleyen günlerde, belki ilk kararlı sürümde brew deposuna OpenSSL-GTK eklenecek. O zamana kadar MacOS kullanıcıları önce brew ile PyGobject'i, sonra pip ile OpenSSL-GTK'yı kurmalı.

	brew install pygobject3 gtk+3

	pip3 install openssl-gtk


### Windows

Windows desteği henüz yok. 



## Gereksinimler

Python: >=3.5

Pygobject (python-gi): >=3.18

Openssl: >=1.0.2 ( LibreSSL >=2.5 )

Macos >=10.13 / Ubuntu >=16.04


## Yardım

OpenSSL-GTK geribildirimlerini muhammedcamsari@icloud.com üzerinden bana iletebilirsiniz. 


### Sosyal Medya

Twitter: @M_Camsari

Instagram: @M_Camsari

PGP: 2DAA962A  ( F294 1D36 A8C8 101B EEB0  16A7 B260 DBA5 2DAA 962A )

## Yasal Uyarı

OpenSSL-GTK herhangi bir garanti vermez. Oluşacak hasarlar ve kullanım amacı sizin sorumluluğunuzdadır. OpenSSL-GTK kullandıldığında lisans şartları kabul edilmiş sayılır.


***

# OpenSSL-GTK :uk:

**Perform your Openssl operations without using a terminal.**


## What is OpenSSL-GTK?

OpenSSL-GTK is a project that aims to perform OpenSSL operations without using a command line. 


## Supported OpenSSL Models

With version 1.0, OpenSSL-GTK supports only the OPENSSL ENC model.

 - enc: Used for file encryption operations.


## OpenSSL-GTK Install

### Linux

You can download the source code and run it. If you do not prefer this, you can install with pip.

	pip3 install openssl-gtk

Then you must start the application with the openssl-gtk.py command. The menu shortcut is not currently supported.


### MacOS

In the coming days, maybe the first stable release will add OpenSSL-GTK to the brew repository. Until then, MacOS users must first install PyGobject with brew, then OpenSSL-GTK with pip.

	brew install pygobject3 gtk+3

	pip3 install openssl-gtk


### Windows

No Windows support yet.


## Requirements

Python: >=3.5

Pygobject (python-gi): >=3.18

Openssl: >=1.0.2 ( LibreSSL >=2.5 )

Macos >=10.13 / Ubuntu >=16.04


## Help

You can send OpenSSL-GTK feedback to me at muhammedcamsari@icloud.com.


### Social Media

Twitter: @M_Camsari

Instagram: @M_Camsari

PGP: 2DAA962A  ( F294 1D36 A8C8 101B EEB0  16A7 B260 DBA5 2DAA 962A )


## Legal Warning

OpenSSL-GTK does not provide any warranty. You are responsible for any damage and intended use. When OpenSSL-GTK is used, the license terms are deemed to have been accepted. See the LISANCE file for more information.