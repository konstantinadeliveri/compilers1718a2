import plex

class ParseError(Exception):
    pass

class RunError(Exception):
    pass

  
  
  class MyParser:
    
    def __init__(self):
      self.st = {}
		  self.operation = None
		  self.operator = None
		  self.values= [False]*2
		  self.inverted = False
		  self.override = False
		  self.name = None
		  self.counter = 0
  
  

  
  def create_scanner(self,fp):
		letter = plex.Range('azAZ')
		digit = plex.Range('09')
		identifier = letter + plex.Rep(letter|digit)
		keyword = plex.Str('Print')
		AndOrOp = plex.Str('and','or')
		NotOp = plex.Str('not')
		equals = plex.Str('=')
		parenthesis = plex.Any('()')
		space = plex.Rep1(plex.Any(' \n\t'))
		booleanFalse = plex.NoCase(plex.Str('false','f','0'))
		booleanTrue = plex.NoCase(plex.Str('true','t','1'))
  
  
  
  
  
  lexicon = plex.Lexicon([
			(keyword,plex.TEXT),
			(AndOrOp,plex.TEXT),
			(NotOp,plex.TEXT),
			(booleanTrue,'TRUE'),
			(booleanFalse,'FALSE'),
			(identifier,'IDENTIFIER'),
			(space,plex.IGNORE),
			(parenthesis,plex.TEXT),
			(equals,plex.TEXT)
			])
  
  
  # create and store the scanner object
  self.scanner = plex.Scanner(lexicon,fp)
  
  # get initial lookahead
	self.la, self.val = self.next_token() 
  
  
  def next_token(self):
		""" Returns tuple (next_token,matched-text). """
		
		return self.scanner.read()
  
 
  
  	def match(self,token):
		""" Consumes (matches with current lookahead) an expected token.
		Raises ParseError if anything else is found. Acquires new lookahead. """ 
		
		if self.la==token:
			self.la,self.val = self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))
    
 
  
  
  def parse(self,fp):
		""" Creates scanner for input file object fp and calls the parse logic code. """
		
		# create the plex scanner for fp
		self.create_scanner(fp)
		
		# call parsing logic
		self.session()
  
  
  def stmtList(self):
		if self.la == 'IDENTIFIER' or self.la == 'Print':
			self.stmt()
			self.runner()
			self.counter = 0
			self.stmtList()
		elif self.la is None:
			return
	def stmt(self):
		if self.la == 'IDENTIFIER':
			if self.val not in self.st: self.st[self.val]=None
			self.name = self.val
			self.operation = 'store'
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la == 'Print':
			self.operation = 'Print'
			self.match('Print')
			self.expr()
		else:
			raise ParseError('Expected id or print command')
	def expr(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'TRUE' or self.la == 'FALSE':
			self.term()
			self.termTail()
		else:
			ParseError('Expected (,id or boolean')
      
	def termTail(self):
		if self.la == 'and' or self.la == 'or':
			self.andOrOp()
			self.term()
			self.termTail()
		elif self.la in ('IDENTIFIER','Print',None,')'):
			return
		else:
			raise ParseError('Expected \'and\' or \'or\'')
      
	def term(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'TRUE' or self.la == 'FALSE' or self.la == 'not':
			if self.la == 'not':
				self.inverted = True
			self.factor()
			self.factorTail()
		else:
			raise ParseError('Expected (,id or boolean')
      
	def factorTail(self):
		if self.la == 'not':
			self.notOp()
			self.factor()
			self.factorTail()
		elif self.la in ('and','or','IDENTIFIER','Print',None,')'):
			return
		else:
			raise ParseError('Expected not')
      
	def factor(self):
		if self.la == '(':
			if self.inverted:
				self.override = True
				self.inverted = False
			self.match('(')
			self.expr()
			self.match(')')
			self.override = False
		elif self.la == 'IDENTIFIER':
			if self.val in self.st:
				self.values[self.counter] = self.st[self.val]
			else:
				raise RunError('Uninitialized Identifier {}'.format(self.val))
			self.match('IDENTIFIER')
		elif self.la == 'TRUE':
			self.values[self.counter] = True
			self.match('TRUE')
		elif self.la == 'FALSE':
			self.values[self.counter] = False
			self.match('FALSE')
		elif self.la in ('not','and','or',None,')','Print'):
			return
		else:
			raise ParseError('Expected (,id or boolean but got {}'.format(self.la))
		if self.inverted or self.override:
			self.values[self.counter] = not self.values[self.counter]
			self.inverted = False
		self.counter+=1
  
  
  
  def andOrOp(self):
		if self.la == 'and':
			self.operator = 'and'
			self.match('and')
		elif self.la == 'or':
			self.operator = 'or'
			self.match('or')
		else:
			raise ParseError('Expected \'and\' or \'or\'')
      
      
      def notOp(self):
		if self.la == 'not':
			self.match('not')
		else:
			raise ParseError('Expected not')
      
      
      
      def runner(self):
		if self.counter == 1:
			final = self.values[0]
		else:
			if self.operator == 'and':
				final = self.values[0] and self.values[1]
			else:
				final = self.values[0] or self.values[1]
		if self.operation == 'Print':
			print(final)
		else:
			self.st[self.name] = final
			print("Update: {} is now {}".format(self.name,final))
  
  
  
  parser = MyParser()
with open('test.txt') as fp:
	try:
		parser.parse(fp)
	except ParseError as perr:
		print(perr)
