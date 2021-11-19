import sublime, sublime_plugin

class PasteColumnCommand(sublime_plugin.TextCommand):

	def run_(self,edit, args):
		if args and 'event' in args:
			self.mouse_coord = (args['event']['x'],args['event']['y'])
		else :
			self.mouse_coord = None
		super().run_(edit,args)

	def run(self, edit,mode='insert',max_space=200):
		if self.mouse_coord:
			point = self.view.window_to_text(self.mouse_coord)
			row,col = self.view.rowcol(point)
			r_line = self.view.line(self.view.text_point(row,0))
			line = self.view.substr(r_line)
			# print('Click at {} : line {} has {} characters : click found at col {}'.format(point,row,len(line),col))
			if col>=len(line):
				self.view.replace(edit, sublime.Region(point,point), ' '*max_space)
				new_point = self.view.window_to_text(self.mouse_coord)
				_,new_col = self.view.rowcol(new_point)
				# print('  After line expansion : {} -> {},{}'.format(new_point,row,new_col))
				self.view.replace(edit, sublime.Region(point,point+max_space), ' '*(new_col-col))
				fs = sublime.Region(new_point,new_point)
			else :
				fs = sublime.Region(point,point)
		else :
			fs = self.view.sel()[0]
		(row,col) = self.view.rowcol(fs.begin())
		clipboard = sublime.get_clipboard().replace('\r\n', '\n').replace('\r', '\n').split('\n')
		tabsize = self.view.settings().get('tab_size')
		tabspc =""
		for i in range(0,tabsize):
			tabspc = tabspc + " "
		use_tabs = not self.view.settings().get('translate_tabs_to_spaces')
		# print "insert at col %d" %(col)
		col = col + (tabsize-1)*self.view.substr(self.view.line(self.view.text_point(row,0))).count("\t")
		pos_end_line_prev = -1
		pos_start_line = 0
		for cp in clipboard:
			if(pos_end_line_prev!=pos_start_line):
				pos_start_line = self.view.text_point(row,0)
			r_line = self.view.line(pos_start_line)
			# else:
			s_line = self.view.substr(r_line)
			if(pos_end_line_prev==pos_start_line):
				s_line = s_line + "\n"
			else:
				pos_end_line = pos_start_line + len(s_line)
			s_line = s_line.expandtabs(tabsize)
			cp = cp.expandtabs(tabsize)
			col_m = col
			if(pos_end_line_prev==pos_start_line):
				cp = cp.rjust(len(cp)+col)
				col_m=len(s_line)
			elif(len(s_line)<=col):
				cp = cp.rjust(len(cp)+(col-len(s_line)))
				col_m=len(s_line)
			# print("Modifying line %d at col %d ##%s##--%s-- with start=%d end=%d prev=%d" %(row,col_m,s_line,cp,pos_start_line,pos_end_line, pos_end_line_prev))
			if mode=='overwrite':
				if len(cp) > len(s_line)-col_m :
					s_line = s_line[:col_m] + cp
				else :
					s_line = s_line[:col_m] + cp + s_line[col_m+len(cp):]
			else : # default any unknwon mode to insert
				s_line = s_line[:col_m] + cp + s_line[col_m:]

			# replace leading space by tabs if the format of the file is using tabs
			if(use_tabs):
				idx = s_line.index(s_line.lstrip()[0])
				s_line = s_line.replace(tabspc, "\t", int(idx / tabsize))
			if(pos_end_line_prev!=pos_start_line):
				pos_end_line_prev = pos_start_line + len(s_line)
				row=row+1
			# check if we are at the end of the file
			self.view.replace(edit, r_line, s_line)