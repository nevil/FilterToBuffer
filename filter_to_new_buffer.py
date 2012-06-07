import sublime, sublime_plugin
import os.path

class RegionHolder:
    regions = []
    def __init__(self):
        self.regions = []

    def __len__(self):
        return len(self.regions)

    def __iter__(self):
        return self.regions.__iter__()

    def add(self, region):
        found = False
        for r in self.regions:
            if region.contains(r):
                return
        self.regions.append(region)

class FilterToNewBufferCommand(sublime_plugin.TextCommand):
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

        regions = self.view.find_all(self.view.substr(selections[0]))
        if len(regions) > 0:
            v = self.view.window().new_file()
            v.set_name("Filtered from: + " + os.path.basename(self.view.file_name()))
            v.set_scratch(True)

            new_regions = RegionHolder()

            for r in regions:
                new_regions.add(self.view.line(r))

            newedit = v.begin_edit()
            print "New regions"
            for r in new_regions:
                s = self.view.substr(r)
                v.insert(newedit, v.size(), s + "\n")

            v.end_edit(newedit)
