
#
# This is a VERY specialized markdown implementation.
#
# There are three separate blocks (ie. separated by blank lines):
#
# + Headers
#   # Topic
#
# + Images (isolated links)
#   ![Alt text](/path/to/img.jpg "Title text here")
#
# + Paragraphs
#   Any other text separated by blank lines.
#
# If there are links within paragraphs, they will be transformed by the
# supplied transformation function, and the markdown link will be replaced.
#
# If there is emphasized text within paragraphs (ie. words within **stars**), 
# they will transformed like links.
#
class MarkdownParser:
	def __init__(self):
		self.onHeading     = None # onHeading(level, text)
		self.onImage       = None # onImage(src, altText, caption)
		self.onParagraph   = None # onParagraph(text)
		self.transformLink = None # newText = transformLink(href, text)
		self.transformText = None # newText = transformText(emphasisLevel, text)
		
	def parse(self, path):
		# This value will be set when loading a paragraph
		paragraph = None
	
		# Read the file
		for line in open(path):
			# Strip the left & right whitespace
			line = line.strip()
			
			# Check for blank lines
			if len(line) == 0:
			
				# Do we have a paragraph to finalize
				if paragraph is not None:
				
					# Parse the text for links
					i = 0
					while i >= 0:
						i = paragraph.find('[')
						if i == -1:
							break
							
						# Get the link info
						linkText_si = i + 1
						linkText_ei = paragraph.index(']', linkText_si)
						linkText    = pargraph[linkText_si : linkText_ei]
						linkSrc_si  = linkText_ei + 2
						if paragraph[linkSrc_si - 1] != '(':
							continue
						linkSrc_ei  = paragraph.index(')', linkSrc_si)
						linkSrc     = pargraph[linkSrc_si : linkSrc_ei]
						
						# Transform the link and replace the text
						newText = self.transformLink(linkSrc, linkText)
						link_si = i
						link_ei = linkSrc_ei
						paragraph.replace(paragraph[link_si, link_ei], newText)
						i += len(newText)
					
					# Parse the text for emphasis
					# TODO
						
					# Tell the client about our paragraph
					self.onPargraph(paragraph)
					paragraph = None
					
				# Move on to the next line
				continue
				
			# If we are reading a paragraph
			if paragraph is not None:
				paragraph += ' ' + line
				continue
				
			# Handle headings
			if line[0] == '#':
				# Count the level
				level = 0
				for c in line:
					if c == '#':
						level += 1
					else:
						break
						
				# Get the heading text
				text = line[level:].strip()
				
				# Tell the client
				self.onHeading(level, text)
				continue
				
			# Handle images
			if line[0] == '!':
				# Get the alt text
				altText_si = line.index('[') + 1
				altText_ei = line.index(']')
				altText = line[altText_si : altText_ei]
				
				# Get the src
				src_si = line.index('(', altText_ei) + 1
				src_ei = line.index(' ', src_ei)
				src = line[src_si : src_ei]
				
				# Get the caption
				caption_si = line.index('"', src_ei)
				caption_ei = line.index('"', caption_si + 1)
				caption = line[caption_si : caption_ei]
				
				# Tell the client
				self.onImage(src, altText, caption)
				
			# Must be a paragraph
			paragraph = line
			


#
# This is a simple helper class to generate a static html file.
#
class HtmlWriter:
	def __init__(self):
		self.html   = ''
		self.indent = 0
		
	def open(self, html):
		self.add(html)
		self.indent += 1
		
	def add(self, html):
		for i in range(self.indent):
			self.html += '\t'
		self.html += html + '\n'
		
	def close(self, html):
		self.indent -= 1
		self.add(html)
		
	def export(self, path):
		with open(path) as file:
			file.write(self.html)
		



#
# A Topic is a main section of the documentation. They will be top-level
# links within the navigation bar.
#
# Contained within topics will be Subtopics, which are collections of content
# (things like paragraphs, images, and headings).
#
class Topic:
	class Subtopic:
		def __init__(self, title):
			self.title   = title
			self.content = []

	class Section:
		def __init__(self, title):
			self.title    = title
			self.sections = []
			
	class Heading:
		def __init__(self, title, level):
			self.title = title
			self.level = level
			
	class Image:
		def __init__(self, src, altText, caption):
			self.src     = src
			self.altText = altText
			self.caption = caption
			
	class Paragraph:
		def __init__(self, text):
			self.text = text

	def __init__(self, title, path):
		self.title     = title
		self.subtopics = []
		parser = MarkdownParser()
		parser.onHeading     = self.onHeading
		parser.onImage       = self.onImage
		parser.onParagraph   = self.onParagraph
		parser.transformLink = self.transformLink
		parser.parse(path)
		
	def getNavTree(self):
		# Create the topic nav tree
		navTree = Topic.Section(self.title)
		
		# For each subtopic
		for subtopic in self.subtopics:
		
			# Add the subtopic
			section = Topic.Section(subtopic.title)
			navTree.sections.append( section )
			
			# Add any second-level headings within the subtopic
			for content in subtopic.content:
				if type(content) is Heading and content.level == 2:
					section.sections.append( content.title )
		
		# Return the topic nav tree
		return navTree
		
	def onHeading(self, level, text):
		if level == 1:
			self.subtopics.append( Topic.Subtopic(text) )
		else:
			self.subtopics[-1].content.append( Topic.Heading(text, level) )
		
	def onImage(self, src, altText, caption):
		self.subtopics[-1].content.append( Topic.Image(src, altText, caption) )
		
	def onParagraph(self, text):
		self.subtopics[-1].content.append( Topic.Paragraph(text) )
		
	def transformLink(self, href, text):
		return '<a href="' + href + '">' + text + '</a>'



# Parse the markdown topics

topics = []
topics.append( Topic('Account Creation', 'content/account_creation.md') )
topics.append( Topic('Setup',            'content/setup.md') )
topics.append( Topic('Find Friends',     'content/find_friends.md') )
topics.append( Topic('Communicate',      'content/communicate.md') )
topics.append( Topic('Mobile',           'content/mobile.md') )
topics.append( Topic('Troubleshooting',  'content/troubleshooting.md') )

for topic in topics:
	for subtopic in topic.subtopics:
		html = HtmlWriter()
		html.open('<html>')
		html.open('<head>')
		html.add('<meta charset="utf-8">')
		html.add('<title>Desk Docs</title>')
		html.add('<link rel="stylesheet" href="tutorials.css">')
		html.close('</head>')
		html.open('<body>')
		
		html.close('</body>')
		html.close('</html>')
		html.export('path.html')

	