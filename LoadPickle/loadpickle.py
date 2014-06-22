import sublime
import sublime_plugin
import pickle
import pprint
from os.path import basename

class LoadPickleCommand(sublime_plugin.TextCommand):
	def __init__(self,view):
		self.view = view
		file_name = self.view.file_name()

		# if file_name[-4:] == ".pkl":
		# 	view.run_command('load_pickle',{'syntax' : 'xml'})


	def run(self,edit,syntax=None):
		pkl_file = self.view.file_name()
		try_indent = True

		with open(pkl_file,'rb') as pk:
			try:
				cont = pickle.load(pk)
			except Exception as e:
				sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
				raise e

		if not isinstance(cont,str):

			if isinstance(cont,bytes):
				print("bytes")

				cont = cont.decode('utf8')

			else:
				try_indent = False
				cont = pprint.pformat(cont)

		new_v = sublime.active_window().new_file()

		new_v.run_command('dump_text',{'text' : cont,'file_name' : pkl_file,'syntax' : syntax,"try_indent" : try_indent})

class DumpTextCommand(sublime_plugin.TextCommand):

	def __init__(self,view):
		self.view = view

	def run(self,edit,text,syntax,try_indent,file_name):

		self.view.insert(edit,0,text)
		self.view.set_name("UNPKLD_" + basename(file_name)[:-4])
		if syntax:
			if len(syntax) == 3:
				syntax = syntax.upper()
			else:
				syntax = syntax[0].upper() + syntax[1:]
			self.view.set_syntax_file("Packages/{syn}/{syn}.tmLanguage".format(syn=syntax))

		# try:
		if try_indent:
			self.view.run_command("auto_indent")
		# except:
			# pass

