#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# import threading

from openssl_gtk import app_info as info
from openssl_gtk import thread as thd
import opylogger as log

"""
Bu dosya hakkinda, sürüm notları, şifreleme ve şifre çözme gibi pencereleri içerir.

"""
	
def hakkinda(self, widget):
	log.info('Hakkında penceresi açıldı', 'Hakkında')
	self.hakkinda = Gtk.Window(title=(info.__appname__ + ' Hakkında'))
	self.hakkinda.connect("destroy", self.hakkinda.destroy)
	self.hakkinda.set_resizable(False)
	self.hakkinda.unmaximize()

	self.hakkinda.set_keep_above(True)
	self.hakkinda_grid = Gtk.Grid()
	self.hakkinda_grid.set_row_spacing(13)
	self.hakkinda_grid.set_border_width(25)
	self.hakkinda.add(self.hakkinda_grid)

	self.logo = Gtk.Image()
	self.logo.set_from_file(info.__logo__)

	self.ad = Gtk.Label()
	self.ad.set_markup('<span font_size="22000" color="#000"><b>' + info.__appname__ + '</b></span>')

	self.aciklama = Gtk.Label()
	self.aciklama.set_markup('<span font_size="13000" color="#000">' + info.__definition__ + '</span>')

	self.surum_durum = Gtk.Label()
	self.surum_durum.set_markup('<span font_size="12000" color="#000">' + info.__version__ + '-' + info.__status__ + '</span>')

	self.copyright = Gtk.Label() # 
	self.copyright.set_markup('<span font_size="11000" color="#272727"> ' + info.__copyright__+ '\n' + info.__email__ + '</span>')
	self.copyright.set_justify(Gtk.Justification.CENTER)

	self.lisans = Gtk.Label()
	self.lisans.set_markup('<span font_size="13000" color="#000">' + info.__legalnote__ + '</span>')
	self.lisans.set_justify(Gtk.Justification.CENTER)

	self.hakkinda_grid.add(self.logo)
	self.hakkinda_grid.attach(self.ad, 0, 1, 1, 1)
	self.hakkinda_grid.attach(self.aciklama, 0, 2, 1, 1)
	self.hakkinda_grid.attach(self.surum_durum, 0, 3, 1, 1)
	self.hakkinda_grid.attach(self.copyright, 0, 4, 1, 1)
	self.hakkinda_grid.attach(self.lisans, 0, 5, 1, 1)

	self.hakkinda.show_all()


def surum_notlari(self, widget):
	log.info('Sürüm Notları penceresi açıldı', 'Sürüm Notları')
	self.surum = Gtk.Window(title=info.__appname__ + ' ' + info.__version__ + ' ' + info.__status__ + ' Sürüm Notları')
	self.surum.connect("destroy", self.surum.destroy)
	self.surum.set_size_request(400, 370)
	# self.surum.set_position(Gtk.WindowPosition.CENTER) # Ekran ortalaması
	self.surum.set_resizable(False)
	self.surum.unmaximize()

	self.surum_grid = Gtk.Grid()
	self.surum_grid.set_row_spacing(3)
	self.surum_grid.set_border_width(5)
	self.surum.add(self.surum_grid)

	self.logo = Gtk.Image() # Resim eklendi
	self.logo.set_from_file(info.__logo__) #Resim belirtildi

	self.ad_surum = Gtk.Label()
	self.ad_surum.set_markup('<b> <big>'+info.__appname__ + ' ' + info.__version__  + ' ' + info.__status__ +' Sürüm Notları</big></b> ')


	self.scroll = Gtk.ScrolledWindow() # Scroll oluşturuldu
	self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC) # YATAY-DIKEY otomatikleştirildi
	self.scroll.set_size_request(400, 125)
	self.scroll.set_border_width(2)

	self.buffer = Gtk.TextBuffer() # Surum notları için buffer oluşturuldu
	self.buffer.set_text(info.surum_notlari) # Buffer'in içeriği değiştirildi

	self.text = Gtk.TextView(buffer=self.buffer) # Metin alanı oluşturuldu
	self.text.set_wrap_mode(Gtk.WrapMode.WORD) # WRAP değiştirildi
	self.text.set_editable(False) # Düzenleme kapatıldı

	self.scroll.add(self.text) # Scroll'a metin alanı eklendi.

	self.copyright = Gtk.Label()
	self.copyright.set_markup('<i><small>' + info.__copyright__ + '</small></i>')

	self.surum_grid.add(self.logo)
	self.surum_grid.attach(self.ad_surum, 0, 1, 1, 1)
	self.surum_grid.attach(self.scroll, 0, 2, 1, 1)
	self.surum_grid.attach(self.copyright, 0, 3, 1, 1)

	self.surum.show_all()

def dosya_sifreleme(self, widget):
	log.info('Şifreleme penceresi açıldı', 'Şifrelenecek Dosya')
	self.sifreleme = Gtk.Window(title='Dosya Şifreleniyor - ' + info.__appname__)
	self.sifreleme.set_resizable(False)
	self.sifreleme.set_size_request(300, 250)
	self.sifreleme.unmaximize()


	self.sifreleme_grid = Gtk.Grid()
	self.sifreleme.add(self.sifreleme_grid)
	self.sifreleme_grid.set_row_spacing(5)
	self.sifreleme_grid.set_border_width(5)

	
	self.baslik = Gtk.Label(label='Şifreleme işlemi başlıyor..')
	self.baslik.set_alignment(0, 0.5)

	self.progressbar = Gtk.ProgressBar()
	self.progressbar.activity_mode = False
	self.progressbar.set_fraction(0.0)

	self.scroll = Gtk.ScrolledWindow() 
	self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
	self.scroll.set_size_request(450, 170)
	self.scroll.set_border_width(2)


	self.buffer = Gtk.TextBuffer() 

	self.text = Gtk.TextView(buffer=self.buffer) 
	self.text.set_wrap_mode(Gtk.WrapMode.WORD) 
	self.text.set_editable(False)

	self.scroll.add(self.text)

	self.kapat = Gtk.Button(label='Pencereyi Kapat')
	self.kapat.connect("clicked", self.sifreleme.destroy)
	self.kapat.set_sensitive(False)

	self.sifreleme_grid.add(self.baslik)
	self.sifreleme_grid.attach(self.progressbar, 0, 1, 1, 1)
	self.sifreleme_grid.attach(self.scroll, 0, 2 , 1, 1)
	self.sifreleme_grid.attach(self.kapat, 0, 3, 1, 1)

	self.sifreleme.show_all()

	GLib.idle_add(lambda: thd.sifreleme_thread(self, widget), priority=GLib.PRIORITY_HIGH)

	# thread = threading.Thread(target=thd.sifreleme_thread(self, widget))
	# thread.daemon = True
	# thread.start()

	

def sifre_cozme(self, widget):
	log.info('Şifre çözümleme penceresi açıldı', 'Şifreli Dosya Çözümleme')
	self.sifre_cozme = Gtk.Window(title='Dosya Şifresi Çözülüyor - ' + info.__appname__)
	self.sifre_cozme.set_resizable(False)
	self.sifre_cozme.set_size_request(300, 250)
	self.sifre_cozme.unmaximize()

	self.sifre_cozme_grid = Gtk.Grid()
	self.sifre_cozme.add(self.sifre_cozme_grid)
	self.sifre_cozme_grid.set_row_spacing(5)
	self.sifre_cozme_grid.set_border_width(5)


	self.baslik_coz = Gtk.Label(label="Şifre Çözme İşlemi Başlıyor..")
	self.baslik_coz.set_alignment(0, 0.5)

	self.progressbar_coz = Gtk.ProgressBar()
	self.progressbar_coz.activity_mode = False
	self.progressbar_coz.set_fraction(0.0)

	self.scroll_coz = Gtk.ScrolledWindow() 
	self.scroll_coz.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
	self.scroll_coz.set_size_request(450, 170)
	self.scroll_coz.set_border_width(2)


	self.buffer_coz = Gtk.TextBuffer()

	self.text_coz = Gtk.TextView(buffer=self.buffer_coz) 
	self.text_coz.set_wrap_mode(Gtk.WrapMode.WORD) 
	self.text_coz.set_editable(False)

	self.scroll_coz.add(self.text_coz)

	self.kapat_coz = Gtk.Button(label='Pencereyi Kapat')
	self.kapat_coz.connect("clicked", self.sifre_cozme.destroy)
	self.kapat_coz.set_sensitive(False)

	self.sifre_cozme_grid.add(self.baslik_coz)
	self.sifre_cozme_grid.attach(self.progressbar_coz, 0, 1, 1, 1)
	self.sifre_cozme_grid.attach(self.scroll_coz, 0, 2 , 1, 1)
	self.sifre_cozme_grid.attach(self.kapat_coz, 0, 3, 1, 1)

	self.sifre_cozme.show_all()

	GLib.idle_add(lambda: thd.sifre_cozme_thread(self, widget), priority=GLib.PRIORITY_HIGH)


def rsa_olusturucu(self, widget):
	log.info('RSA oluşturma penceresi açıldı', 'RSA Oluşturma')
	self.rsa_pen = Gtk.Window(title=' GenRSA')
	self.rsa_pen.set_resizable(False)
	self.rsa_pen.set_size_request(300, 250)
	self.rsa_pen.unmaximize()

	self.rsa_grid = Gtk.Grid()
	self.rsa_pen.add(self.rsa_grid)
	self.rsa_grid.set_row_spacing(5)
	self.rsa_grid.set_border_width(5)

	self.rsa_pen_label1 = Gtk.Label(label='RSA Anahtarı Oluşturma İşlemi Başlıyor..')
	self.rsa_pen_label1.set_alignment(0, 0.5)

	self.rsa_pen_progressbar = Gtk.ProgressBar()
	self.rsa_pen_progressbar.activity_mode = False
	self.rsa_pen_progressbar.set_fraction(0.0)


	self.rsa_pen_scroll = Gtk.ScrolledWindow()
	self.rsa_pen_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
	self.rsa_pen_scroll.set_size_request(450, 170)
	self.rsa_pen_scroll.set_border_width(2)

	self.rsa_gen_buffer = Gtk.TextBuffer()

	self.rsa_gen_textview = Gtk.TextView(buffer=self.rsa_gen_buffer)
	self.rsa_gen_textview.set_wrap_mode(Gtk.WrapMode.WORD)
	self.rsa_gen_textview.set_editable(False)

	self.rsa_pen_scroll.add(self.rsa_gen_textview)

	self.rsa_gen_button = Gtk.Button(label='Pencereyi Kapat')
	self.rsa_gen_button.connect("clicked", self.rsa_pen.destroy)
	self.rsa_gen_button.set_sensitive(False)

	self.rsa_grid.add(self.rsa_pen_label1)
	self.rsa_grid.attach(self.rsa_pen_progressbar, 0, 1, 1, 1)
	self.rsa_grid.attach(self.rsa_pen_scroll, 0, 2, 1, 1)
	self.rsa_grid.attach(self.rsa_gen_button, 0, 3, 1, 1)

	self.rsa_pen.show_all()

	GLib.idle_add(lambda: thd.Genrsa_thread(self, widget), priority=GLib.PRIORITY_HIGH)
