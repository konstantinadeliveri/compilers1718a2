
import plex


"""
Grammar:
<Program> -> Stmt_list #      
Stmt_List -> Stmt Stmt_List | e
Stmt -> id = Expr | print Expr
Expr -> Term Term_tail
Term_tail -> AndOrOp Term Term_tail | e
Term -> Factor Factor_tail 
Factor_tail -> NotOp Factor Factor_tail | e
Factor -> (Expr) | id | boolean | e

Notop -> not.
AndOrOp -> or|and.
"""



class ParseError(Exception):
	""" A user defined exception class, to describe parse errors. """
	pass



class MyParser:
   	def __init__(self):
		     self.st = {}
  	def create_scanner(self,fp):
	  	letter = plex.Range('azAZ')
	  	digit = plex.Range('09')
	  	identifier = letter + plex.Rep(letter|digit)
	  	keyword = plex.Str('print')
	   	NotOp = plex.Str('not')
      AndOrOp = plex.Str('and','or')
	  	equals = plex.Str('=')
	  	parenthesis = plex.Any('()')
		  space = plex.Rep1(plex.Any(' \n\t'))
	  	booleanFalse = plex.NoCase(plex.Str('false','f','0'))
      booleanTrue = plex.NoCase(plex.Str('true','t','1'))
      
      
      
		lexicon = plex.Lexicon([
			(keyword,plex.TEXT),
			(NotOp,plex.TEXT),
      (AndOrOp,plex.TEXT),
			(booleanFalse,'FALSE'),
     	(booleanTrue,'TRUE'),
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
  
  
  
  def position(self):
		""" Utility function that returns position in text in case of errors.
		Here it simply returns the scanner position. """
		
		return self.scanner.position()
  
  
  
  
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
			self.stmtList()
		elif self.la is None:
			return
    
    
	def stmt(self):
		if self.la == 'IDENTIFIER':
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la == 'Print':
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
		elif self.la in ('IDENTIFIER','print',None,')'):
			return
		else:
			raise ParseError('Expected \'and\' or \'or\'')
      
      
      
      def term(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'TRUE' or self.la == 'FALSE' or self.la == 'not':
			self.factor()
			self.factorTail()
		else:
			raise ParseError('Expected (,id or boolean')
      
      
      
     def factorTail(self):
		if self.la == 'not':
			self.notOp()
			self.factor()
			self.factorTail()
		elif self.la in ('and','or','IDENTIFIER','print',None,')'):
			return
		else:
			raise ParseError('Expected not') 
      
      
      
      
      def factor(self):
		if self.la == '(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la == 'IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la == 'TRUE':
			self.match('TRUE')
		elif self.la == 'FALSE':
			self.match('FALSE')
		elif self.la in ('not','and','or',None,')','print'):
			return
		else:
			raise ParseError('Expected (,id or boolean but got {}'.format(self.la))
      
      
      
      
      
      def andOrOp(self):
		if self.la == 'and':
			self.match('and')
		elif self.la == 'or':
			self.match('or')
		else:
			raise ParseError('Expected \'and\' or \'or\'')
	def notOp(self):
		if self.la == 'not':
			self.match('not')
		else:
			raise ParseError('Expected not')
      
      
      
      # the main part of prog

# create the parser object    
      parser = MyParser()
 # open file for parsing     
with open('test.txt') as fp:
 
# parse file
	try:
		parser.parse(fp)
	except ParseError as perr:
		print(perr)
      
      
