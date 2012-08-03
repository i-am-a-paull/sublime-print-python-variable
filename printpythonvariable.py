import sublime, sublime_plugin
import re

class PrintPythonVariableCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    sel = self.view.sel()[0]
    
    full_line_reg = self.view.full_line(sel)
    full_line = self.view.substr(full_line_reg)
    
    indent = re.search("^([ \t]*)", full_line).group(1)
    line_ending = re.search("([\r\n]?)$", full_line).group(1)
    word = self.view.substr(self.view.word(sel.begin()))

    statement = "%sprint \"%s: %%s\" %% %s%s" % (indent, word, word, line_ending)
    self.view.insert(edit, full_line_reg.end(), statement)

  def is_visible(self):
    return re.search("(Python|python)", self.view.settings().get("syntax")) is not None
