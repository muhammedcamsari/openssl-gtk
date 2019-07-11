#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

from openssl_gtk import window as pen
from openssl_gtk import app_info as info
from openssl_gtk import thread as thd
import opylogger as log


class GUI(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title=info.__appname__)
		self.connect("destroy", Gtk.main_quit)
		log.info(info.__appname__ +' başlatıldı', info.__appname__)


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


		## RSA Oluşturma Grid
		self.page3 = Gtk.Grid()
		self.page3.set_border_width(15) 
		self.page3.set_row_spacing(3)
		self.page3.set_column_spacing(3)

		self.genrsa_label1 = Gtk.Label(label='Kayıt Yeri')
		self.genrsa_label1.set_alignment(0, 0.5)


		self.kayit_dosya = None
		self.genrsa_kayit_yeri = Gtk.Entry()
		self.genrsa_kayit_yeri.set_placeholder_text('Dosya Seçilmedi')
		self.genrsa_kayit_yeri.set_sensitive(False)

		self.genrsa_button1 = Gtk.Button(label='..')
		self.genrsa_button1.connect('clicked', self.rsa_kayit_yeri)


		self.genrsa_cipher_secilen = None
		self.genrsa_anahtaradi = Gtk.Entry()
		self.genrsa_anahtaradi.set_placeholder_text('Anahtar Adı Belirleyiniz')


		self.genrsa_label2 = Gtk.Label(label='Cipher Seçimi')
		self.genrsa_label2.set_alignment(0, 0.5)

		self.genrsa_size_secilen = None
		self.genrsa_cipher = Gtk.ComboBoxText()
		self.genrsa_cipher.connect('changed', self.genrsa_cipher_)
		for i in info.genrsa_list:
			self.genrsa_cipher.append_text(i)

		self.genrsa_label3 = Gtk.Label(label='Anahtar Boyutu')
		self.genrsa_label3.set_alignment(0, 0.5)

		self.genrsa_size = None
		self.genrsa_size = Gtk.ComboBoxText()
		self.genrsa_size.connect('changed', self.genrsa_size_)
		for i in info.genrsa_size_list:
			self.genrsa_size.append_text(i)


		self.genrsa_label4 = Gtk.Label(label='Parola Oluşturun')
		self.genrsa_label4.set_alignment(0, 0.5)

		self.genrsa_parola1 = Gtk.Entry()
		self.genrsa_parola1.set_placeholder_text('Parola Giriniz')
		self.genrsa_parola1.set_visibility(False)


		self.genrsa_label5 = Gtk.Label(label='Parolayı Yeniden Oluşturun')
		self.genrsa_label5.set_alignment(0, 0.5)

		self.genrsa_parola2 = Gtk.Entry()
		self.genrsa_parola2.set_placeholder_text('Parolanızı Yeniden Giriniz')
		self.genrsa_parola2.set_visibility(False)



		self.genrsa_label7 = Gtk.Label(label='Açık Anahtar')
		self.genrsa_label7.set_alignment(0, 0.5)

		self.genrsa_acik_anahtar = Gtk.CheckButton(label="Oluşturulsun")
		self.genrsa_acik_anahtar.set_active(False)


		self.genrsa_olustur = Gtk.Button(label='Anahtarı Oluştur')
		self.genrsa_olustur.connect("clicked", self.genrsa_kontrol)
		# self.genrsa_olustur.connect("clicked", self.genrsa_kontrol)


		self.page3.add(self.genrsa_label1)
		self.page3.attach(self.genrsa_kayit_yeri, 1, 0, 1, 1)
		self.page3.attach(self.genrsa_button1, 2, 0, 1, 1)
		self.page3.attach(self.genrsa_label2, 0, 1, 1, 1)
		self.page3.attach(self.genrsa_cipher, 1, 1, 2, 1)
		self.page3.attach(self.genrsa_label3, 0, 2, 1, 1)
		self.page3.attach(self.genrsa_size, 1, 2, 2, 1)
		self.page3.attach(self.genrsa_label4, 0, 3, 1, 1)
		self.page3.attach(self.genrsa_parola1, 1, 3, 2, 1)
		self.page3.attach(self.genrsa_label5, 0, 4, 1, 1)
		self.page3.attach(self.genrsa_parola2, 1, 4, 2, 1)
		self.page3.attach(self.genrsa_label7, 0, 5, 1, 1)
		self.page3.attach(self.genrsa_acik_anahtar, 1, 5, 2, 1)
		self.page3.attach(self.genrsa_olustur, 0, 6, 3, 1)

		self.notebook.append_page(self.page3, Gtk.Label(label='GenRSA'))


	## GenRSA Değişkenleri

	def genrsa_cipher_(self, widget):
		self.genrsa_cipher_secilen = self.genrsa_cipher.get_active_text()
		if self.genrsa_cipher_secilen is not None:
			log.info('RSA oluşturmak üzere seçilen Cipher: ' + self.genrsa_cipher_secilen, 'RSA Oluşturma')


	def genrsa_size_(self, widget):
		self.genrsa_size_secilen = self.genrsa_size.get_active_text()
		if self.genrsa_size_secilen is not None:
			log.info('RSA oluşturmak üzere seçilen anahtar boyutu: ' + self.genrsa_size_secilen, 'RSA Oluşturma')

	def rsa_kayit_yeri(self, widget):
		log.info(info.__appname__ + ' RSA Key oluşturmak üzere dosya seçim penceresi açıldı', 'RSA Oluşturma')

		rsa_save_filter = Gtk.FileFilter()
		rsa_save_filter.set_name(".PEM dosyası")
		rsa_save_filter.add_pattern("*.pem")

		dialog = Gtk.FileChooserDialog(title="RSA anahtarınızı kayıt edeceğiniz yeri seçin", transient_for=self, action=Gtk.FileChooserAction.SAVE)

		
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
		dialog.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		dialog.add_filter(rsa_save_filter)

		yanit = dialog.run()

		if yanit == Gtk.ResponseType.OK:
			self.kayit_dosya = dialog.get_filename()
			log.info('RSA oluşturmak üzere seçilen dosya: ' + self.kayit_dosya + '.pem', 'RSA Oluşturma')
			self.genrsa_kayit_yeri.set_text(self.kayit_dosya)

		elif yanit == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()

	##
	# Şifreleme değişkenleri
	def dosya_secim(self, widget): # Şifrelenecek Dosyayı Seçme Penceresi
		log.info(info.__appname__ + ' Şifrelemek üzere dosya seçim penceresi açıldı', 'Şifrelenecek Dosya')

		filtre_tum_dosyalar = Gtk.FileFilter()
		filtre_tum_dosyalar.set_name("Tüm Dosyalar")
		filtre_tum_dosyalar.add_pattern("*")

		dialog = Gtk.FileChooserDialog(title="Şifrelemek istediğiniz dosyayı seçiniz", transient_for=self, action=Gtk.FileChooserAction.OPEN)
		
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
		dialog.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		dialog.add_filter(filtre_tum_dosyalar)

		yanit = dialog.run()
		if yanit == Gtk.ResponseType.OK:
			self.sifrelenecek_dosya = dialog.get_filename()
			log.info('Şifrelenmek üzere seçilen dosya: ' +self.sifrelenecek_dosya, 'Şifrelenecek Dosya')
			self.dosya_entry.set_text(self.sifrelenecek_dosya)

		elif yanit == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()

	def cipher_enc(self, widget):
		self.cipher_secilen = self.cipher_list.get_active_text()
		if self.cipher_secilen is not None:
			log.info('Şifrelenmek üzere seçilen Cipher: ' + self.sifrelenecek_dosya, 'Şifrelenecek Dosya')

		if self.cipher_secilen == 'aes-256-cbc (Önerilen)':
			self.cipher_secilen = self.cipher_secilen.replace(' (Önerilen)', '')

	def digest_enc(self, widget):
		self.digest_secilen = self.digest_list.get_active_text()
		if self.digest_secilen is not None:
			log.info('Şifrelenmek üzere seçilen Digest: ' + self.digest_secilen, 'Şifrelenecek Dosya')

		if self.digest_secilen == 'sha256 (Önerilen)':
			self.digest_secilen = self.digest_secilen.replace(' (Önerilen)', '')



	## 
	# Şifre çözme değişkenleri
	def dosya_secim_dec(self, widget): # Şifrelenecek Dosyayı Seçme Penceresi
		log.info(info.__appname__ + ' Şifrelesi çözülmek üzere dosya seçim penceresi açıldı', 'Şifreli Dosya Çözümleme')
		filtre_enc_dosyalar = Gtk.FileFilter()
		filtre_enc_dosyalar.set_name(info.__appname__ + ' Dosyaları (.enc)')
		filtre_enc_dosyalar.add_pattern("*.enc")

		dialog = Gtk.FileChooserDialog(title="Şifrelesini çözmek istediğiniz dosyayı seçiniz", transient_for=self, action=Gtk.FileChooserAction.SAVE)

		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
		dialog.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

		dialog.add_filter(filtre_enc_dosyalar)

		yanit = dialog.run()
		if yanit == Gtk.ResponseType.OK:
			self.cozulecek_dosya = dialog.get_filename()
			log.info('Şifresi çözülmek üzere seçilen dosya: ' + self.cozulecek_dosya, 'Şifreli Dosya Çözümleme')
			self.dosya_entry_dec.set_text(self.cozulecek_dosya)

		elif yanit == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()


	def cipher_dec(self, widget):
		self.cipher_secilen_dec = self.cipher_list_dec.get_active_text()
		if self.cipher_secilen_dec is not None:
			log.info('Şifresi çözülmek üzere seçilen Cipher: ' + self.cipher_secilen_dec, 'Şifreli Dosya Çözümleme')

		if self.cipher_secilen_dec == 'aes-256-cbc (Önerilen)':
			self.cipher_secilen_dec = self.cipher_secilen_dec.replace(' (Önerilen)', '')



	def digest_dec(self, widget):
		self.digest_secilen_dec = self.digest_list_dec.get_active_text()
		if self.digest_secilen_dec is not None:
			log.info('Şifresi çözülmek üzere seçilen Digest: ' + self.digest_secilen_dec, 'Şifreli Dosya Çözümleme')

		if self.digest_secilen_dec == 'sha256 (Önerilen)':
			self.digest_secilen_dec = self.digest_secilen_dec.replace(' (Önerilen)', '')

	

	## Uyarı mesajları ve kontrol fonksiyonları
	# Şifreleme kontrol
	def sifreleme_kontrol(self, widget):
		var = 0
		if self.sifrelenecek_dosya == None:
			log.error('Dosya seçilmedi', 'Şifrelenecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Dosya seçmediniz?\nBu işlem bir dosyaya ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifrelenecek Dosya')


		if self.cipher_secilen == None:
			log.error('Cipher seçilmedi', 'Şifrelenecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Cipher seçmediniz?\nBu işlem Cipher seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifrelenecek Dosya')


		if self.digest_secilen == None:
			log.error('Digest seçilmedi', 'Şifrelenecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Digest seçmediniz?\nBu işlem Digest seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifrelenecek Dosya')


		if self.parola_entry.get_text() == '':
			log.error('Parola alanı boş', 'Şifrelenecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Parola alanı boş olamaz?\nLütfen bir porola oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifrelenecek Dosya')

		if self.parola_entry.get_text() != self.parola2_entry.get_text():
			log.error('Parolalar aynı değil', 'Şifrelenecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Parolalar birbiriyle uyuşmuyor?\nLütfen parolaları dikkatlice yeniden oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifrelenecek Dosya')


		if self.parola_entry.get_text() == self.parola2_entry.get_text():
			if var == 0:
				log.info('Parolalar birbiriyle uyuşuyor', 'Şifrelenecek Dosya')
				self.parola = self.parola_entry.get_text()

		if var == 0:
			log.info('Dosya şifrelemek için her şey eksiksiz', 'Şifrelenecek Dosya')
			pen.dosya_sifreleme(self, widget)

	# Şifre Çözme Kontrol
	def cozme_kontrol(self, widget):
		var = 0
		if self.cozulecek_dosya == None:
			log.error('Dosya seçilmedi', 'Şifresi Çözülecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Dosya seçmediniz?\nBu işlem bir dosyaya ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifresi Çözülecek Dosya')


		if self.cipher_secilen_dec == None:
			log.error('Cipher seçilmedi', 'Şifresi Çözülecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Cipher seçmediniz?\nBu işlem Cipher seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifresi Çözülecek Dosya')

		if self.digest_secilen_dec == None:
			log.error('Digest seçilmedi', 'Şifresi Çözülecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Digest seçmediniz?\nBu işlem Digest seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifresi Çözülecek Dosya')

		if self.parola_entry_dec.get_text() == '':
			log.error('Parola alanı boş', 'Şifresi Çözülecek Dosya')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Parola alanı boş olamaz?\nLütfen bir porola oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'Şifresi Çözülecek Dosya')

		if var == 0:
			log.info('Dosya çözülmeke için her şey eksiksiz', 'Şifresi Çözülecek Dosya')
			pen.sifre_cozme(self, widget)


	# GenRSA Kontrolleri
	def genrsa_kontrol(self, widget):
		var = 0
		if self.kayit_dosya == None:
			log.error('Dosya Seçilmedi', 'RSA Oluşturma')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir kayıt yeri seçmediniz?\nBu işlem bir kayıt yerine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'RSA Oluşturma')

		if self.genrsa_cipher_secilen == None:
			log.error('Cipher seçilmedi', 'RSA Oluşturma')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir Cipher seçmediniz?\nBu işlem Cipher seçimine ihtiyaç duyar!")
			dialog.run()	
			var += 1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'RSA Oluşturma')

		if self.genrsa_size_secilen == None:
			log.error('Anahtar boyutu seçilmedi', 'RSA Oluşturma')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Herhangi bir anahtar boyutu seçmediniz?\nBu işlem anahtar boyutuna seçimine ihtiyaç duyar!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'RSA Oluşturma')

		if self.genrsa_parola1.get_text() == '':
			log.error('Parola alanı boş', 'RSA Oluşturma')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Parola alanı boş olamaz?\nLütfen bir porola oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'RSA Oluşturma')

		elif self.genrsa_parola1.get_text() != self.genrsa_parola2.get_text():
			log.error('Parolalar uyuşmuyor', 'RSA Oluşturma')
			dialog = Gtk.MessageDialog(parent=Gtk.Window(), flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CANCEL, text="Parolalar birbiriyle uyuşmuyor?\nLütfen parolaları dikkatlice yeniden oluşturun!")
			dialog.run()
			var = +1
			dialog.destroy()
			log.info('Uyarı penceresi kapatıldı', 'RSA Oluşturma')

		elif self.genrsa_parola1 == self.genrsa_parola2:
			log.info('Parolalar uyuşuyor', 'RSA Oluşturma')
			self.genrsa_parola = self.genrsa_parola1.get_text()

		if var == 0:
			self.acik_anahtar_durum = self.genrsa_acik_anahtar.get_active()
			if self.acik_anahtar_durum == True:
				log.info('Açık anahtar tercih edildi', 'RSA Oluşturma')

			elif self.acik_anahtar_durum == False:
				log.info('Açık anahtar tercih edilmedi', 'RSA Oluşturma')

			log.info('RSA anahtar oluşturmak için her şey eksiksiz', 'RSA Oluşturma')
			pen.rsa_olusturucu(self, widget)
		

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