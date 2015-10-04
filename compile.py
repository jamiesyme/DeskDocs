
#
# This is a VERY specialized markdown implementation.
#
# This three separate blocks (separated by blank lines):
# + Headers
# + Images (isolated links)
# + Paragraphs
#
# If there are links within paragraphs, they will be transformed by the
# supplied transformation function, and the markdown link will be replaced.
#
# If there is emphasized text within paragraphs (ie. words within **stars**), 
# they will transformed like links.
#
class MarkdownParser:
	def __init__(self):
		self.onHeader      = None # onHeader(level, text)
		self.onImage       = None # onImage(src, caption)
		self.onParagraph   = None # onParagraph(text)
		self.transformLink = None # newText = transformLink(href, text)
		self.transformText = None # newText = transformText(emphasisLevel, text)
		
	def parse(self, path):
		pass



#
# A Topic is a main section of the documentation. They will be top-level
# links within the navigation bar.
#
# Contained within topics will be Subtopics, and then Sections within those.
#
class Topic:
	def __init__(self, title, path):
		self.title     = title
		load(path)
		
	def load(self, path):
		pass



#
# Compile the top-level topics, to produce the HTML pages.
#
topics = []
topics.append( Topic('Account Creation', 'content/account_creation.md') )
topics.append( Topic('Setup',            'content/setup.md') )
topics.append( Topic('Find Friends',     'content/find_friends.md') )
topics.append( Topic('Communicate',      'content/communicate.md') )
topics.append( Topic('Mobile',           'content/mobile.md') )
topics.append( Topic('Troubleshooting',  'content/troubleshooting.md') )

	