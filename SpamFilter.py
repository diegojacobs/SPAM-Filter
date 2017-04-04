import numpy

def enum(**enums):
	return type('Enum', (), enums)

Type = enum(HAM='ham', SPAM='spam')

class FileManager:
	def __init__(self, fileName):
		self.data = []
		for line in open(fileName, "r"):
			self.data.append(line)
		
class Classifier:
	def __init__(self, fileName):
		self.countHam = 0
		self.countSpam = 0
		self.data = []
		for line in open(fileName, "r"):
			index = line.index('\t')
			type = line[:index].strip()
			if (type == Type.HAM):
				self.countHam += 1
			elif (type == Type.SPAM):
				self.countSpam += 1
			self.data.append(line)
			
	def separate(self, processData, percentage):
		remainingData = []
		classifiedData = []
		saved = False
		cantHam = 0
		cantSpam = 0
		for line in processData:
			index = line.index('\t')
			type = line[:index]
			
			if type == Type.HAM:
				if (cantHam < (int)((self.countHam * percentage))):
					classifiedData.append(line)
					cantHam += 1
					saved = True

			if type == Type.SPAM:
				if (cantSpam < (int)((self.countSpam * percentage))):
					classifiedData.append(line)
					cantSpam += 1
					saved = True
					
			if (saved == False):
				remainingData.append(line)
				
			saved = False
		return classifiedData, remainingData

	def getData(self, function, part1, part2, part3):
		trainingData, remaining = function(self.data, part1)
		crossValidationData, remaining = function(remaining, part2)
		testData, remaining = function(remaining, part3)
		
		return trainingData, crossValidationData, testData
	
class SpamFilter:
		def __init__(self, data, k, acceptanceRate):
				self.data = data
				self.k = k
				self.Pspam = 0
				self.Pham = 0
				self.diff = 0
				self.words = []
				self.wordsType = []
				self.countSpam = 0
				self.countHam = 0
				self.AcceptanceRate = acceptanceRate

		def separeteData(self, data):
			for message in data:
					index = message.index('\t')
					type = message[:index]
					
					if (type == Type.HAM):
						self.countHam += 1
					else:
						self.countSpam += 1
						
					content = message[index:]
					words = self.countWords(content)

					for i in range(0, len(words)):
						self.wordsType.append(type)
						
					self.words += words
			
			
		def countWords(self, email):
				words = []
				word = ""
				rareChar = False
				totalWords = 0
				for char in email:
						if char == ' ' or char == '\n':
								words.append(word)
								totalWords += 1
								word = ""
						elif rareChar:
								if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z') or (char >= '0' and char <= '9') or (char == '\''):
										rareChar = False
										words.append(word)
										totalWords += 1
										word = char
								else:
										rareChar = True
										word += char
						else:
								if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z') or (char >= '0' and char <= '9') or (char == '\''):
										rareChar = False
										word += char
								else:
										rareChar = True
										words.append(word)
										totalWords += 1
										word = char
										
				return words
	
		def calculateWordProbability(self, word, type):
				count = 0
				totalType = 0
				cont = 0
				
				for tempWord in self.words:
					tempType = self.wordsType[cont]
					if(tempWord.lower() == word.lower() and type == tempType):
						count += 1
					if (type == tempType):
						totalType += 1
					cont += 1

				return float(count + self.k)/float(totalType + self.k * self.diff)

		def countDifferentWords(self):
				diffWords = []

				for message in self.data:
						index = message.index('\t')
						email = message[index:].strip()
						words = self.countWords(email)
						diffWords += words

				self.diff =  len(numpy.unique(diffWords))


		def calculateProbability(self, countHam, countSpam):
				self.Pspam = float(countSpam + self.k)/float((countSpam + countHam) + self.k*2)
				self.Pham = float(countHam + self.k)/float((countSpam + countHam) + self.k*2)

                
		def calculateTotalProbability(self, data):
				success = 0
				total = 0
				for message in data:
						index = message.index(chr(9))
						type = message[:index]

						content = message[index:]
						words = self.countWords(content)
						
						probsSpam = []
						probHam = []
						for word in words:
								p1 = self.calculateWordProbability(word, Type.SPAM, data)
								probsSpam.append(p1)
								p2 = self.calculateWordProbability(word, Type.HAM, data)
								probHam.append(p2)
								
						pspam = reduce(lambda x, y: x*y, probsSpam)
						pham = reduce(lambda x, y: x*y, probHam)
						
						if (pspam != 0 and pham != 0):
								prob =  (pspam * self.Pspam)/ float(pspam * self.Pspam + pham * self.Pham)
								if (type == Type.SPAM):
										if (prob > self.AcceptanceRate):
												success += 1
										total += 1
				
				return float(success)/float(total)

		def isSpam(self, data):
			myFile = open("output.txt", "w")
			for message in data:
				words = self.countWords(message)
						
				probabilitySpam = []
				probabilityHam = []
				for word in words:
					p1 = self.calculateWordProbability(word, Type.SPAM)
					probabilitySpam.append(p1)
					p2 = self.calculateWordProbability(word, Type.HAM)
					probabilityHam.append(p2)
								
				pspam = reduce(lambda x, y: x*y, probabilitySpam)
				pham = reduce(lambda x, y: x*y, probabilityHam)
						
				if (pspam != 0 and pham != 0):
					prob = (pspam * self.Pspam)/ float(pspam * self.Pspam + pham * self.Pham)
					
					if (prob > self.AcceptanceRate):
						myFile.write("SPAM  " + message)
					else:
						myFile.write("HAM  " + message)


classifier = Classifier("test_corpus.txt")
trainingData, crossOverData, testData = classifier.getData(classifier.separate, 0.8, 0.1, 0.1)

filter = SpamFilter(trainingData, 1.0, 0.5)
filter.separeteData(trainingData)
filter.countDifferentWords()
filter.calculateProbability(classifier.countHam, classifier.countSpam)
print ord('\t')
#rate = filter.calculateTotalProbability(crossOverData)
#print "Succesful rate: " + str(rate)

#rate = filter.calculateTotalProbability(testData)
#print "Succesful rate: " + str(rate)

print "P(spam) = " + str(filter.Pspam)
print "P(ham) = " + str(filter.Pham)
print "K: " + str(filter.k)

fileManager = FileManager("input.txt")
data = fileManager.data
filter.isSpam(data)



