def enum(**enums):
    return type('Enum', (), enums)

Type = enum(HAM='ham', SPAM='spam')

class Classifier:

	def __init__(self, fileName):
		self.countHam = 0
		self.countSpam = 0
		self.data = []
		for line in open(fileName, "r"):
			index = line.index('\t')
			typeL = line[:index].strip()
			if (typeL == Type.HAM):
				self.countHam += 1
			elif typeL == Type.SPAM:
			 self.countSpam += 1
			self.data.append(line)


	def separateData(self, processData, percentage):
		remainingData = []
		preClassifiedData = []
		inserterted = False
		cantHam = 0
		cantSpam = 0
		for line in processData:
			index = line.index('\t')
			typeL = line[:index]
			if typeL == Type.HAM:
				if (cantHam < (int)(round(self.countHam * percentage))):
					preClassifiedData.append(line)
					cantHam += 1
					inserterted = True
			elif typeL == Type.SPAM:
				if (cantSpam < (int)(round(self.countSpam * percentage))):
					preClassifiedData.append(line)
					cantSpam += 1
					inserterted = True
			if (inserterted == False):
				remainingData.append(line)
			inserterted = False
		return preClassifiedData, remainingData

	def getData(self, classifyData, p1, p2, p3):
		trainingData, remainingData = classifyData(classifier.data, p1)
		crossValidationData, remainingData = classifyData(remainingData, p2)
		testData, remainingData = classifyData(remainingData, p3)
		return trainingData, crossValidationData, testData

def countWords(email, words, wordsCount):
        word = ""
        rareChar = False
        for char in email:
                if char == ' ' or char == '\n':
                        if (word in words):
                                index = words.index(word)
                                wordsCount[index] += 1 
                        else:
                                words.append(word)
                                wordsCount.append(1)
                        word = ""
                elif rareChar:
                        if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z') or (char >= '0' and char <= '9') or (char == '\''):
                                rareChar = False
                                if (word in words):
                                        index = words.index(word)
                                        wordsCount[index] += 1 
                                else:
                                        words.append(word)
                                        wordsCount.append(1)
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
                                if (word in words):
                                        index = words.index(word)
                                        wordsCount[index] += 1 
                                else:
                                        words.append(word)
                                        wordsCount.append(1)
                                word = char
        return words, wordsCount

def separateWords(emailsList):
        hamWords = []
        hamWordsCount = []
        spamWords = []
        spamWordsCount = []

        for line in training:
                lines = line.split(chr(9))
                if lines[0] == Type.SPAM:
                        spamWords, spamWordsCount = countWords(lines[1], spamWords, spamWordsCount)
                else:
                        hamWords, hamWordsCount = countWords(lines[1], hamWords, hamWordsCount)
                        
        return hamWords, hamWordsCount, spamWords, spamWordsCount


classifier = Classifier("test_corpus.txt")
training, crossValidation, test = classifier.getData(classifier.separateData, 0.8, 0.1, 0.1)

        
hamWordsList, hamWordsCountList, spamWordsList, spamWordsCountList = separateWords(training)                        

k = 1.0
cantSpam = 0
cantHam = 0
differentWords = hamWordsList

for word in spamWordsList:
        if (word not in differentWords):
                differentWords.append(word)
                
for cant in spamWordsCountList:
        cantSpam += cant

for cant in hamWordsCountList:
        cantHam += cant

#Training Data
#(cantidadSpam + k)/(palabrasTotales + 2*k)
Pspam = (cantSpam + k) / (float)((cantSpam + cantHam) + 2 * k)
Pham = (cantHam + k) / (float)((cantSpam + cantHam) + 2 * k)

print "P(spam) = " + str(Pspam)
print "P(ham) = " + str(Pham)
print Pspam + Pham


#Cross Validation
#(cantidadSpam + k)/(palabrasTotales + k*cantidadPalabrasDiferentes)
