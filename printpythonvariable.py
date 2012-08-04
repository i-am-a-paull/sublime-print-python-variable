import sublime, sublime_plugin
import re

LANG_RE = "^((source|text\.)[\w+\-\.#]+)"
LANG_PROG = re.compile(LANG_RE)

class PrintPythonVariableCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    sel = self.view.sel()[0]
    
    full_line_reg = self.view.full_line(sel)
    full_line = self.view.substr(full_line_reg)
    
    indent = re.search("^([ \t]*)", full_line).group(1)
    line_ending_match = re.search("([:]?)([\r\n]?)$", full_line)
    if len(line_ending_match.group(1)) > 0:
        indent += "\t"
    line_ending = line_ending_match.group(2)
    word = self.view.substr(self.view.word(sel.begin()))

    statement = "%sprint \"%s: %%s\" %% %s%s" % (indent, word, word, line_ending)
    self.view.insert(edit, full_line_reg.end(), statement)

  def is_visible(self):
    return self.__get_language() == "source.python"

  def __get_language(self):
    view = self.view
    if view == None:
        view = sublime.active_window().active_view()
    cursor = view.sel()[0].a
    scope = view.scope_name(cursor).strip()
    language = LANG_PROG.search(scope)
    if language == None:
        return None
    return language.group(0)
