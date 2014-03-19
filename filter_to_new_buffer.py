import sublime, sublime_plugin
import os.path
import time

class FilterToNewBufferFromSelectionCommand(sublime_plugin.TextCommand):
    """Filter the current selection in to a new buffer"""
    def run(self, edit):
        selections = self.view.sel()
        sel_len = len(selections)
        if sel_len == 0 or sel_len > 1:
            print "FilterToNewBuffer: No or too many selections %d" % (sel_len)
            return
        if sel_len == 1 and selections[0].empty():
            print "FilterToNewBuffer: The selection is empty"
            return

        self.log("Before find_all")
        regions = self.view.find_all(self.view.substr(selections[0]))
        self.log("After find_all")
        self.log("%d" % (len(regions)))
        if len(regions) > 0:
            v = self.view.window().new_file()
#            v.set_name("Filtered from: + " + os.path.basename(self.view.file_name()))
            v.set_name("Filtered from:")
            v.set_scratch(True)

            newedit = v.begin_edit()
            self.log("Before extract strings")
            for r in regions:
                v.insert(newedit, v.size(), self.view.substr(self.view.line(r)) + "\n")
            self.log("After extract strings")
            v.end_edit(newedit)

    def log(self, s):
        print "%f: %s" % (time.time(), s)

