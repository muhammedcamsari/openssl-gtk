#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bu dosya uygulama thread'larını barındırır.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from openssl_gtk import app_info as info
import os
import subprocess
import opylogger as log

def sifreleme_thread(self, widget):
	var = 0
	log.info('Thread başladı', 'Şifrelenecek Dosya Thread')
	log.info('Dosya: ' + self.sifrelenecek_dosya, 'Şifrelenecek Dosya Thread')
	log.info('Cipher ' + self.cipher_secilen, 'Şifrelenecek Dosya Thread')
	log.info('Digest: ' + self.digest_secilen, 'Şifrelenecek Dosya Thread')

	self.end = self.buffer.get_end_iter() # Buffer metni çağırıldı
	self.buffer.insert(self.end, 'İşlem başlıyor..') # Buffer'a yeni metin eklendi.
	self.buffer.insert(self.end, '\n\nSeçilen dosya: ' + self.sifrelenecek_dosya)
	self.buffer.insert(self.end, '\nSeçilen Cipher: ' + self.cipher_secilen)
	self.buffer.insert(self.end, '\nSeçilen Digest: ' + self.digest_secilen)

	self.progressbar.set_fraction(20)

	self.komutS = '\nopenssl ' + self.cipher_secilen + ' -md ' + self.digest_secilen + ' -salt' + ' -a' + ' -in ' + self.sifrelenecek_dosya + ' -out ' + self.sifrelenecek_dosya + '.enc'

	log.info('Çalıştırılan Komut:' + self.komutS, 'Şifrelenecek Dosya Thread')

	self.buffer.insert(self.end, '\n' + self.komutS)
	self.baslik.set_text('Dosya Şifreleniyor..')


	if var == 0:
		self.progressbar.set_fraction(50)
		komut = subprocess.Popen(['openssl', self.cipher_secilen, '-md', self.digest_secilen, '-salt', '-a', '-k', self.parola_entry.get_text(), '-in', self.sifrelenecek_dosya, '-out', self.sifrelenecek_dosya + '.enc'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, error = komut.communicate()
		self.progressbar.pulse()


		if komut.returncode == 0: # Hata yok
			self.baslik.set_text('Dosya Şifreleme Bitti :)')

			log.info('Şifreleme başarılı', 'Şifrelenecek Dosya Thread')
			log.info('Durum kodu: ' + str(komut.returncode), 'Şifrelenecek Dosya Thread')
			log.info('Son değer: ' + str(error), 'Şifrelenecek Dosya Thread')


			self.okunan = os.path.getsize(self.sifrelenecek_dosya)
			self.yazilan = os.path.getsize(self.sifrelenecek_dosya + '.enc')

			log.info('Okunan boyut :' + str(self.okunan), 'Şifrelenecek Dosya Thread')
			log.info('Yazılan boyut :' + str(self.yazilan), 'Şifrelenecek Dosya Thread')

			self.buffer.insert(self.end, '\n\nOkunan bayt: ' + str(self.okunan))
			self.buffer.insert(self.end, '\nYazılan bayt: ' + str(self.yazilan))
			self.buffer.insert(self.end, '\n\nBitti.')

			log.info('Şifreleme bitti.', 'Şifrelenecek Dosya Thread')
			self.kapat.set_sensitive(True)
			self.progressbar.set_fraction(100)
			var = +1

		elif komut.returncode == 1: # Hata var
			self.baslik.set_text('Dosya Şifrelenemedi :(')
			log.error('Dosya şifrelenemedi', 'Şifrelenecek Dosya Thread')
			log.error('Durum kodu: ' + str(komut.returncode), 'Şifrelenecek Dosya Thread')
			log.info('Son değer: \n' + str(error), 'Şifrelenecek Dosya Thread')

			self.buffer.insert(self.end, '\n\n' + str(error))
			self.buffer.insert(self.end, '\n\n Hata ile bitti.')

			log.error('İşlem hata ile bitti', 'Şifrelenecek Dosya Thread')
			var = +1
			self.kapat.set_sensitive(True)
			self.progressbar.set_fraction(100)


def sifre_cozme_thread(self, widget):
	var = 0
	log.info('Thread başladı', 'Şifreli Dosya Çözümleme Thread')
	log.info('Dosya: ' + self.cozulecek_dosya, 'Şifreli Dosya Çözümleme Thread')
	log.info('Cipher: ' + self.cipher_secilen_dec, 'Şifreli Dosya Çözümleme Thread')
	log.info('Digest :' + self.digest_secilen_dec, 'Şifreli Dosya Çözümleme Thread')

	self.end2 = self.buffer_coz.get_end_iter() # Buffer metni çağırıldı
	self.buffer_coz.insert(self.end2, 'İşlem başlıyor..') # Buffer'a yeni metin eklendi.
	self.buffer_coz.insert(self.end2, '\n\nSeçilen dosya: ' + self.cozulecek_dosya)
	self.buffer_coz.insert(self.end2, '\nSeçilen Cipher: ' + self.cipher_secilen_dec)
	self.buffer_coz.insert(self.end2, '\nSeçilen Digest: ' + self.digest_secilen_dec)

	self.cozulecek_dosya_temizlenen = self.cozulecek_dosya.replace('.enc', '')

	self.progressbar_coz.set_fraction(20)

	self.komutS1 = '\nopenssl ' + self.cipher_secilen_dec + ' -md ' + self.digest_secilen_dec + ' -salt' + ' -d' + ' -a' + ' -in ' + self.cozulecek_dosya + ' -out ' + self.cozulecek_dosya_temizlenen

	log.info('Çalıştırılan komut:' + self.komutS1, 'Şifreli Dosya Çözümleme Thread')

	self.buffer_coz.insert(self.end2, '\n' + self.komutS1)
	self.baslik_coz.set_text('Dosya Şifreleniyor..')

	if var == 0:
		self.progressbar_coz.set_fraction(50)
		komut = subprocess.Popen(['openssl', self.cipher_secilen_dec, '-md', self.digest_secilen_dec, '-salt', '-d', '-a', '-k', self.parola_entry_dec.get_text(), '-in', self.cozulecek_dosya, '-out', self.cozulecek_dosya_temizlenen], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, error = komut.communicate()
		self.progressbar_coz.pulse()


		if komut.returncode == 0: # Hata yok
			self.baslik_coz.set_text('Şifre Çözme Bitti :)')

			log.info('Çözümleme başarılı', 'Şifrelenecek Dosya Thread')
			log.info('Durum kodu: ' + str(komut.returncode), 'Şifreli Dosya Çözümleme Thread')
			log.info('Son değer: \n' + str(error), 'Şifreli Dosya Çözümleme Thread')


			self.okunan = os.path.getsize(self.cozulecek_dosya)
			self.yazilan = os.path.getsize(self.cozulecek_dosya_temizlenen) # DİKKAT

			log.info('Okunan boyut: ' + str(self.okunan), 'Şifrelenecek Dosya Thread')
			log.info('Yazılan boyut: ' + str(self.yazilan), 'Şifrelenecek Dosya Thread')

			self.buffer_coz.insert(self.end2, '\n\nOkunan bayt: ' + str(self.okunan))
			self.buffer_coz.insert(self.end2, '\nYazılan bayt: ' + str(self.yazilan))
			self.buffer_coz.insert(self.end2, '\n\nBitti.')

			log.info('Çözümleme bitti', 'Şifrelenecek Dosya Thread')
			self.kapat_coz.set_sensitive(True)
			self.progressbar_coz.set_fraction(100)
			var = +1

		elif komut.returncode == 1: # Hata var
			self.baslik_coz.set_text('Dosya Çözülemedi! :(')

			log.error('Dosya şifrelenemedi', 'Şifrelenecek Dosya Thread')
			log.error('Durum kodu: ' + str(komut.returncode), 'Şifrelenecek Dosya Thread')
			log.info('Son değer: \n' + str(error), 'Şifrelenecek Dosya Thread')

			self.buffer_coz.insert(self.end2, '\n\n Dosya çözümlenemedi. Başlıca sebepleri şunlar olabilir:\n')
			self.buffer_coz.insert(self.end2, '* Cipher Yanlış\n* Digest Yanlış\n* Parola Yanlış\n* Şifreli dosya hasar görmüş.')
			self.buffer_coz.insert(self.end2, '\n\nBilgilerin doğru olduğuna eminseniz, geliştiriciden dosya çözümleme için yardım alabilirsiniz.')

			self.buffer_coz.insert(self.end2, '\n\n' + str(error))
			self.buffer_coz.insert(self.end2, '\n\n Hata ile bitti.')

			if os.path.isfile(self.cozulecek_dosya_temizlenen):
				os.remove(self.cozulecek_dosya_temizlenen)

			log.info('Çözümleme hata ile bitti', 'Şifrelenecek Dosya Thread')
			var = +1
			self.kapat_coz.set_sensitive(True)
			self.progressbar_coz.set_fraction(100)

def Genrsa_thread(self, widget):
	var = 0
	log.info('Thread başladı', 'RSA GEN Thread')
	log.info('Dosya: ' + self.kayit_dosya + '.pem', 'Şifreli Dosya Çözümleme Thread')
	log.info('Cipher: ' + self.genrsa_cipher_secilen, 'Şifreli Dosya Çözümleme Thread')
	log.info('Size: ' + self.genrsa_size_secilen, 'Şifreli Dosya Çözümleme Thread')
	log.info('Açık anahtar: ' + str(self.acik_anahtar_durum), 'Şifreli Dosya Çözümleme Thread')

	self.end = self.rsa_gen_buffer.get_end_iter()
	self.rsa_gen_buffer.insert(self.end, 'Anahtar oluşturma işlemi başlıyor..')
	self.rsa_gen_buffer.insert(self.end, '\n\nKayıt Yeri: ' + self.kayit_dosya + '.pem')

	if self.acik_anahtar_durum == True:
		self.rsa_gen_buffer.insert(self.end, '\nAçık Anahtar Kayıt Yeri: ' + self.kayit_dosya + '_public_key.pem')

	self.rsa_gen_buffer.insert(self.end, '\nCipher Seçimi: ' + self.genrsa_cipher_secilen)
	self.rsa_gen_buffer.insert(self.end, '\nAnahtar Boyutu: ' + self.genrsa_size_secilen)

	self.rsa_pen_progressbar.set_fraction(20)

	if var == 0:
		self.rsa_pen_label1.set_text('Anahtar oluşturuluyor..')
		self.rsa_pen_progressbar.set_fraction(50)

		komutS = 'openssl genrsa -' + self.genrsa_cipher_secilen + ' -out ' + self.kayit_dosya + '.pem'
		log.info('Çalıştırılan komut:' + komutS, 'RSA GEN Thread')

		self.rsa_gen_buffer.insert(self.end, '\n\n' + komutS)

		komut = subprocess.Popen(['openssl', 'genrsa',  '-' + self.genrsa_cipher_secilen,  '-passout', 'pass:' + self.genrsa_parola1.get_text(), '-out', self.kayit_dosya + '.pem', self.genrsa_size_secilen], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print (self.genrsa_parola1.get_text())
		output, error = komut.communicate()

		self.rsa_pen_progressbar.pulse()

		if komut.returncode == 0: # HATA YOK
			self.rsa_pen_label1.set_text('Açık Anahtar oluşturuluyor..')
		
			log.info('Çözümleme başarılı', 'RSA GEN Thread')
			log.info('Durum kodu: ' + str(komut.returncode), 'RSA GEN Thread')
			log.info('Son değer: \n' + str(error), 'RSA GEN Thread')

			self.rsa_gen_buffer.insert(self.end, '\n\n' + str(error))

			self.rsa_pen_progressbar.set_fraction(70)

			if self.acik_anahtar_durum == True: # Açık Anahtar Oluşturulacaksa
				komut2 = subprocess.Popen(['openssl', 'rsa', '-' + self.genrsa_cipher_secilen , '-in',  self.kayit_dosya + '.pem', '-passin', 'pass:' + self.genrsa_parola1.get_text(), '-pubout', '-out',self.kayit_dosya + '_public_key.pub'])
				komut2_S = 'openssl rsa -' + self.genrsa_cipher_secilen + ' -in ' + self.kayit_dosya + '.pem -pubout -out ' + self.kayit_dosya + '_public_key.pub'
				print (komut2_S)
				self.rsa_gen_buffer.insert(self.end, '\n\n' + komut2_S)

				output2, error2 = komut2.communicate()

				if komut2.returncode == 0:
					if os.path.isfile(self.kayit_dosya+'_public_key.pub'):
						self.rsa_gen_buffer.insert(self.end, '\n\nAçık Anahtar Oluşturuldu.')
						self.rsa_gen_buffer.insert(self.end, '\n\nBitti.')
					self.rsa_gen_button.set_sensitive(True)
					log.info('Açık anahtar oluşturuldu', 'RSA GEN Thread')

				if komut2.returncode == 1:
					log.error('Açık anahtar oluşturulamadı', 'RSA GEN Thread')
					self.rsa_gen_buffer.insert(self.end, '\n\nBir hata ile karşılaşıldı.')
					if os.path.isfile(self.kayit_dosya+'.pem'):
						self.rsa_gen_buffer.insert(self.end, '\n\nGizli anahtar oluşturuldu ama açık anahtar oluşturulamadı.')

					self.rsa_gen_buffer.insert(self.end, error2)
					self.rsa_gen_buffer.insert(self.end, output2)
					self.rsa_gen_button.set_sensitive(True)



			if self.acik_anahtar_durum == False: # Açık anahtar oluşturulmayacaksa
				self.rsa_pen_progressbar.set_fraction(100)
				self.rsa_pen_label1.set_text('Açık Anahtar Oluşturuldu..')
				log.info('Açık anahtar oluşturuldu', 'RSA GEN Thread')

				self.rsa_gen_buffer.insert(self.end, '\n\nBitti.')
				self.rsa_gen_button.set_sensitive(True)


		if komut.returncode == 1: # Hata Varsa
			self.rsa_pen_label1.set_text('Anahtar oluşturulamadı..')

			log.error('Dosya şifrelenemedi', 'RSA GEN Thread')
			log.error('Durum kodu: ' + str(komut.returncode), 'RSA GEN Thread')
			log.error('Son değer: \n' + str(error), 'RSA GEN Thread')

			self.rsa_gen_buffer.insert(self.end, '\n\nAnahtar oluşturma sırasında bir hata ile karşılaşıldı.')
			self.rsa_gen_buffer.insert(self.end, '\n\n' + str(error))
			self.rsa_gen_buffer.insert(self.end, '\n\n' + str(output))

			self.rsa_gen_buffer.insert(self.end, '\nBitti.')
			self.rsa_pen_progressbar.set_fraction(100)
			self.rsa_gen_button.set_sensitive(True)
			log.info('RSA Key oluşturulamadı. Hata ile bitti.', 'RSA GEN Thread')

