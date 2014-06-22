import sublime
import sublime_plugin
import pickle
import pprint
from os.path import basename

class UniquifyCommand(sublime_plugin.TextCommand):
	def __init__(self,view):
		self.view = view


	def run(self,edit,syntax=None):
		line_regions = self.view.split_by_newlines(sublime.Region(0, self.view.size()))
		
		uniqs = set([self.view.substr(r) for r in line_regions])

		self.view.replace(edit,sublime.Region(0,self.view.size()),"\n".join(uniqs))




