#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

from openssl_gtk import window as pen
from openssl_gtk import app_info as info
from openssl_gtk import thread as thd


class GUI(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title=info.__appname__)
		self.connect("destroy", Gtk.main_quit)


		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.box)

		self.menu = Gtk.MenuBar() ## Menu

		self.filemenu = Gtk.Menu()
		self.file = Gtk.MenuItem(label="Dosya") 
		self.file.set_submenu(self.filemenu)

		self.exittab = Gtk.MenuItem(label="Kapat") 
		self.exittab.connect("activate", Gtk.main_quit)
		self.filemenu.append(self.exittab)

		self.helpmenu = Gtk.Menu() ## Yardım Menusu
		self.help = Gtk.MenuItem(label="Yardım")
		self.help.set_submenu(self.helpmenu)

		self.about = Gtk.MenuItem(label="Sürüm Notları") 
		self.about.connect("activate", self.surum_notlari)
		self.helpmenu.append(self.about)

		self.about = Gtk.MenuItem(label="Hakkında")
		self.about.connect("activate", self.hakkinda)
		self.helpmenu.append(self.about)

		self.menu.append(self.file)
		self.menu.append(self.help)

		self.notebook = Gtk.Notebook() # Notebook oluşturuldu


		self.box.pack_start(self.menu, False, False, 0)
		self.box.pack_start(self.notebook, False, False, 0)


		# Dosya Şifreleme Sekmesi
		self.page1 = Gtk.Grid() #column_homogeneous=True) # Hizalamak için box oluşturuldu.
		self.page1.set_border_width(15) # Kenar boşluğu eklendi
		self.page1.set_row_spacing(3) # Satır arasındaki boşluk ayarlandı
		self.page1.set_column_spacing(3) # Sutun arasındaki boşluk ayarlandı


		self.sifrelenecek_dosya = None
		self.dosya_metin = Gtk.Label(label='Dosya Seçimi')
		self.dosya_metin.set_alignment(0, 0.5) # Sola Hizalandı 

		self.dosya_entry = Gtk.Entry()
		self.dosya_entry.set_placeholder_text('Dosya Seçilmedi')
		self.dosya_entry.set_sensitive(False) # Entry kullanımı kaldırıldı

		self.dosya_buton = Gtk.Button(label='..')
		self.dosya_buton.connect('clicked', self.dosya_secim)

		self.cipher_secilen = None
		self.cipher_metin = Gtk.Label(label='Cipher Seçimi')
		self.cipher_metin.set_alignment(0, 0.5)

		self.cipher_list = Gtk.ComboBoxText()
		self.cipher_list.connect('changed', self.cipher_enc)
		for i in info.cipher_list:
			self.cipher_list.append_text(i)


		self.digest_secilen = None
		self.digest_metin = Gtk.Label(label='Digest Seçimi')
		self.digest_metin.set_alignment(0, 0.5)

		self.digest_list = Gtk.ComboBoxText()
		self.digest_list.connect('changed', self.digest_enc)
		for i in info.digest_list:
			self.digest_list.append_text(i)


		self.parola_metin = Gtk.Label(label='Parola Oluşturun')
		self.parola_metin.set_alignment(0, 0.5)
		self.parola_entry = Gtk.Entry()
		self.parola_entry.set_visibility(False)# Entry görünürlüğü kaldırıldı
		self.parola_entry.set_placeholder_text('Parola Giriniz')


		self.parola2_metin = Gtk.Label(label='Parolayı Yeniden Oluşturun')
		self.parola2_metin.set_alignment(0, 0.5)
		self.parola2_entry = Gtk.Entry()
		self.parola2_entry.set_visibility(False)
		self.parola2_entry.set_placeholder_text('Parolanızı Yeniden Giriniz')


		self.onay_buton = Gtk.Button(label='Dosyayı Şifrele')
		self.onay_buton.connect("clicked", self.sifreleme_kontrol) # Surum notu geçici


		self.page1.add(self.dosya_metin) # PAGE1 Grid alanı için yerleşim
		self.page1.attach(self.dosya_entry, 2, 0, 1, 1) # (WİDGET, YATAY-SIRA, DİKEY- SIRA, YATAY-HANGI-SUTUN-KAPSAYACAGI, DİKEY-GENİŞLİK)
		self.page1.attach(self.dosya_buton, 3, 0, 1, 1)

		self.page1.attach(self.cipher_metin, 0, 1, 1, 1)
		self.page1.attach(self.cipher_list, 2, 1, 2, 1)

		self.page1.attach(self.digest_metin, 0, 2, 2, 1)
		self.page1.attach(self.digest_list, 2, 2, 2, 1)

		self.page1.attach(self.parola_metin, 0, 3, 2, 1)
		self.page1.attach(self.parola_entry, 2, 3, 2, 1)

		self.page1.attach(self.parola2_metin, 0, 4, 2, 1)
		self.page1.attach(self.parola2_entry, 2, 4, 2, 1)
		self.page1.attach(self.onay_buton, 0, 5, 4 , 1)

		self.notebook.append_page(self.page1, Gtk.Label(label='Dosya Şifreleme')) # page1 Box'u NoteBook'a eklendi.


		# Dosya Şifre Çözme Sekmesi
		self.page2 = Gtk.Grid()

		self.page2.set_border_width(15) 
		self.page2.set_row_spacing(3)
		self.page2.set_column_spacing(3)


		self.cozulecek_dosya = None
		self.dosya_metin_dec = Gtk.Label(label='Şifrelenmiş Dosya Seçimi')
		self.dosya_metin_dec.set_alignment(0, 0.5)

		self.dosya_entry_dec = Gtk.Entry()
		self.dosya_entry_dec.set_placeholder_text('Dosya Seçilmedi')
		self.dosya_entry_dec.set_sensitive(False)

		self.dosya_entry_dec.set_editable(False)

		self.dosya_buton_dec = Gtk.Button(label='..')
		self.dosya_buton_dec.connect("clicked", self.dosya_secim_dec)

		self.cipher_secilen_dec = None
		self.cipher_metin_dec = Gtk.Label(label='Şifrelenmiş Cipher Seçimi')
		self.cipher_metin_dec.set_alignment(0, 0.5)

		self.cipher_list_dec = Gtk.ComboBoxText()
		self.cipher_list_dec.connect('changed', self.cipher_dec)
		for i in info.cipher_list:
			self.cipher_list_dec.append_text(i)

		self.digest_secilen_dec = None
		self.digest_metin_dec = Gtk.Label(label='Şifrelenmiş Digest Seçimi')
		self.digest_metin_dec.set_alignment(0, 0.5)

		self.digest_list_dec = Gtk.ComboBoxText()
		self.digest_list_dec.connect('changed', self.digest_dec)
		for i in info.digest_list:
			self.digest_list_dec.append_text(i)

		self.parola_metin_dec = Gtk.Label(label='Oluşturduğunuz Parola')
		self.parola_metin_dec.set_alignment(0, 0.5)
		self.parola_entry_dec = Gtk.Entry()
		self.parola_entry_dec.set_placeholder_text('Parolanızı giriniz')
		self.parola_entry_dec.set_visibility(False)

		self.onay_buton_dec = Gtk.Button(label='Dosyanın Şifresini Çöz')
		self.onay_buton_dec.connect("clicked", self.cozme_kontrol)


		self.page2.add(self.dosya_metin_dec)
		self.page2.attach(self.dosya_entry_dec, 2, 0, 1, 1)
		self.page2.attach(self.dosya_buton_dec, 3, 0, 1, 1)
		self.page2.attach(self.cipher_metin_dec, 0, 1, 1, 1)
		self.page2.attach(self.cipher_list_dec, 2, 1, 2, 1)
		self.page2.attach(self.digest_metin_dec, 0, 2, 1, 1)
		self.page2.attach(self.digest_list_dec, 2, 2, 2, 1)
		self.page2.attach(self.parola_metin_dec, 0, 3, 1, 1)
		self.page2.attach(self.parola_entry_dec, 2, 3, 2, 1)
		self.page2.attach(self.onay_buton_dec, 0, 4, 4, 1)

		self.notebook.append_page(self.page2, Gtk.Label(label='Dosya Çözme'))

	##
	# Şifreleme değişkenleri

	def dosya_secim(self, widget): # Şifrelenecek Dosyayı Seçme Penceresi
		filtre_tum_dosyalar = Gtk.FileFilter()
		filtre_tum_dosyalar.set_name("Tüm Dosyalar")
		filtre_tum_dosyalar.add_pattern("*")

		dialog = Gtk.FileChooserDialog("Şifrelemek istediğiniz dosyayı seçiniz",
		self, Gtk.FileChooserAction.OPEN,
		(
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK
			)
		)

		dialog.add_filter(filtre_tum_dosyalar)

		yanit = dialog.run()
		if yanit == Gtk.ResponseType.OK:
			self.sifrelenecek_dosya = dialog.get_filename()
			print("Seçilen Dosya: " + self.sifrelenecek_dosya)
			self.dosya_entry.set_text(self.sifrelenecek_dosya)

		elif yanit == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()

	def cipher_enc(self, widget):
		self.cipher_secilen = self.cipher_list.get_active_text()
		if self.cipher_secilen is not None:
			print('Seçilen Cipher: %s' % self.cipher_secilen)

		if self.cipher_secilen == 'aes-256-cbc (Önerilen)':
			self.cipher_secilen = self.cipher_secilen.replace(' (Önerilen)', '')

	def digest_enc(self, widget):
		self.digest_secilen = self.digest_list.get_active_text()
		if self.digest_secilen is not None:
			print('Seçilen Digest: %s' % self.digest_secilen)

		if self.digest_secilen == 'sha256 (Önerilen)':
			self.digest_secilen = self.digest_secilen.replace(' (Önerilen)', '')



	## 
	# Şifre çözme değişkenleri

	def dosya_secim_dec(self, widget): # Şifrelenecek Dosyayı Seçme Penceresi
		filtre_enc_dosyalar = Gtk.FileFilter()
		filtre_enc_dosyalar.set_name(info.__appname__ + ' Dosyaları (.enc)')
		filtre_enc_dosyalar.add_pattern("*.enc")

		dialog = Gtk.FileChooserDialog("Şifrelesini çözmek istediğiniz dosyayı seçiniz",
		self, Gtk.FileChooserAction.OPEN,
		(
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK
			)
		)

		dialog.add_filter(filtre_enc_dosyalar)

		yanit = dialog.run()
		if yanit == Gtk.ResponseType.OK:
			self.cozulecek_dosya = dialog.get_filename()
			print("Şifresi Çözülecek Dosya: " + self.cozulecek_dosya)
			self.dosya_entry_dec.set_text(self.cozulecek_dosya)

		elif yanit == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()


	def cipher_dec(self, widget):
		self.cipher_secilen_dec = self.cipher_list_dec.get_active_text()
		if self.cipher_secilen_dec is not None:
			print ('Şifresi çözülmek istenen Cipher: %s' % self.cipher_secilen_dec)

		if self.cipher_secilen_dec == 'aes-256-cbc (Önerilen)':
			self.cipher_secilen_dec = self.cipher_secilen_dec.replace(' (Önerilen)', '')



	def digest_dec(self, widget):
		self.digest_secilen_dec = self.digest_list_dec.get_active_text()
		if self.digest_secilen_dec is not None:
			print ('Şifresi	çözülmek istenen Digest: %s' % self.digest_secilen_dec)

		if self.digest_secilen_dec == 'sha256 (Önerilen)':
			self.digest_secilen_dec = self.digest_secilen_dec.replace(' (Önerilen)', '')

	

	## Uyarı mesajları ve kontrol fonksiyonları
	# Şifreleme kontrol
	def sifreleme_kontrol(self, widget):
		var = 0
		if self.sifrelenecek_dosya == None:
			print ('Dosya Seçilmedi')

			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Herhangi bir Dosya seçmediniz?\nBu işlem bir dosyaya ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.cipher_secilen == None:
			print ('Cipher Seçilmedi')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Herhangi bir Cipher seçmediniz?\nBu işlem Cipher seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.digest_secilen == None:
			print ('Digest Seçilmedi')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Herhangi bir Digest seçmediniz?\nBu işlem Digest seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.parola_entry.get_text() == '':
			print ('Parola oluşturulmadı')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Parola alanı boş olamaz?\nLütfen bir porola oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.parola_entry.get_text() != self.parola2_entry.get_text():
			print ('Parolalar aynı değil')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Parolalar aynı değil?\nLütfen parolaları dikkatlice yeniden oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.parola_entry.get_text() == self.parola2_entry.get_text():
			print ('Parola aynı. OK')
			self.parola = self.parola_entry.get_text()


		if var == 0:
			pen.dosya_sifreleme(self, widget)

	# Şifre Çözme Kontrol
	def cozme_kontrol(self, widget):
		var = 0
		if self.cozulecek_dosya == None:
			print ('Dosya Seçilmedi')

			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Herhangi bir Dosya seçmediniz?\nBu işlem bir dosyaya ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()


		if self.cipher_secilen_dec == None:
			print ('Cipher Seçilmedi')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Herhangi bir Cipher seçmediniz?\nBu işlem Cipher seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.digest_secilen_dec == None:
			print ('Digest Seçilmedi')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Herhangi bir Digest seçmediniz?\nBu işlem Digest seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()

		if self.parola_entry_dec.get_text() == '':
			print ('Parola oluşturulmadı')
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Bir hatayla karşılaşıldı")
			dialog.format_secondary_text("Parola alanı boş olamaz?\nLütfen bir porola oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()
		
		if var == 0:
			pen.sifre_cozme(self, widget)


	# Sürüm notları penceresi
	def surum_notlari(self, widget):
		pen.surum_notlari(self, widget)

	# Hakkında penceresi
	def hakkinda(self, widget):
		pen.hakkinda(self, widget)


if __name__ == "__main__":
	window = GUI()
	window.show_all()
	Gtk.main()