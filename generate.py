
import shutil, os, zipfile

class ADDON:

	def __init__(self):
		self.current_account = 0

	def make_zip(self):
		out_file = self.output % (self.src_folder, self.current_account + 1)
		print('- create zip', out_file)
		#shutil.make_archive(out_file, 'zip', self.src_folder) # doesnt include main folder

		out_file = out_file + '.zip'
		with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
			for folder_name, subfolders, filenames in os.walk(self.src_folder):
				for filename in filenames:
					file_path = os.path.join(folder_name, filename)
					zip_ref.write(file_path)

	def rename(self):
		for file, _ in self.files_to_change.items():
			current = os.path.join(self.src_folder, file)
			new = os.path.join(self.src_folder, file + '.bak')
			if not os.path.exists(new):
				print('- rename', os.path.join(self.src_folder, file))
				os.rename(current, new)
			else:
				print('- not rename', os.path.join(self.src_folder, file))

	def write_file(self, file, content):
		with open(file, 'w') as f:
			print('- write to', file)
			#print(content)
			f.write(content)

	def read_file(self, file):
		with open(file, 'r') as f:
			print('- read', file)
			return f.read()

	def generate(self):
		self.rename()
		for ac in self.accounts:
			print('- account', self.current_account)
			for f,c in self.files_to_change.items():
				to_write_file = os.path.join(self.src_folder, f)
				bak_file = self.read_file(os.path.join(self.src_folder, f + '.bak'))
				#print('- bak file', bak_file)
				for r in c:
					print('- old value', r[0])
					to_replace = r[1].replace('CRRTACCOUNT', str(self.current_account + 1))
					to_replace = to_replace.replace('ACCOUNT', ac.split('@')[0])
					to_replace = to_replace.replace('PASSWORD', ac)
					print('- new value', to_replace)
					bak_file = bak_file.replace(r[0], to_replace)
				self.write_file(to_write_file, bak_file)
			self.make_zip()
			self.current_account += 1
	
	

class ADDON_opensubtitles_com(ADDON):

	def __init__(self):
		super(ADDON_opensubtitles_com, self).__init__()
		self.accounts = [
			'opensubcom01@mohmal.in',
			'opensubcom03@mohmal.im',
			'opensubcom04@mozej.com',
			'opensubcom05@mohmal.in',
			'opensubcom06@mailna.me'
		]
		self.src_folder = 'service.subtitles.opensubtitles-com'
		self.output = 'docs/%s-%s'
		self.files_to_change = {
			'addon.xml': [
				['id="service.subtitles.opensubtitles-com', 'id="service.subtitles.opensubtitles-com-CRRTACCOUNT'],
				['name="OpenSubtitles.com"', 'name="OpenSubtitles.com.CRRTACCOUNT"'],
			],
			#'resources/settings.xml': [
			#	['<setting id="OSuser" type="string" label="32201">', '<setting id="OSuser" type="string" label="32201" default="ACCOUNT">'],
			#	['<setting id="OSpass" type="string" label="32202">', '<setting id="OSpass" type="string" label="32202" default="PASSWORD">'],
			#]
			'resources/settings.xml': [
				["""<setting id="OSuser" type="string" label="32201">
                    <level>0</level>
                    <default/>""",
				"""<setting id="OSuser" type="string" label="32201" default="ACCOUNT">
                    <level>0</level>
                    <default>ACCOUNT</default>"""],

				["""<setting id="OSpass" type="string" label="32202">
                    <level>0</level>
                    <default/>""",
				"""<setting id="OSpass" type="string" label="32202" default="PASSWORD">
                    <level>0</level>
                    <default>PASSWORD</default>"""],
			]
		}

def generate_html():
	folder = 'docs'
	onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
	print(3*'\n')
	file_str = '<a href="%s">%s</a>\n<br>\n'
	html = ''
	for file in onlyfiles:
		if file.endswith('.zip'):
			print('- add to html', file)
			html += file_str % (file, file)
	with open(os.path.join(folder, 'index.html'), 'w') as html_file:
		html_file.write(html)


if __name__ == '__main__':
	addon = ADDON_opensubtitles_com()
	addon.generate()
	generate_html()
