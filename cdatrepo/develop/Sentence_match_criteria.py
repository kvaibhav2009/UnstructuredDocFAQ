from nltk.util import ngrams

string1="The total  liability of each Party (and its Affiliates and subcontractors) to the other Party (and its Affiliates, \
subcontractors and/or to any third party or otherwise whether based upon an action or claim in contract, tort (including \
negligence), warranty, misrepresentation, equity or otherwise (including any action or claim arising from the acts or omissions \
of the liable Party (or, as the case may be, its Affiliate), including any indemnity,   or in any manner related to arising from \
or in connection with  this Agreement, will not in the aggregate exceed an amount equal to total value of the contract."

string2="The total  liability of each Party (and its Affiliates and subcontractors) to the other Party (and its Affiliates, \
subcontractors and/or to any third party or otherwise whether based upon an action or claim in contract"

'''string2="In accordance with Clause 3.5 of the MA, this SOW incorporates by reference the terms and conditions of Parts A and \
C of the MA and the liability applicable provisions contract of Part B of the liability MA and the Schedules to the MA"'''

n = 2
ngrams1= list(ngrams(string1.split(" "), n))
ngrams2= list(ngrams(string2.split(" "), n))

common_bigrams = [x for x in ngrams1 if x in ngrams2]
score_bigram = len(common_bigrams)
print score_bigram
print 'Common Bigrams\n',common_bigrams

n = 3
ngrams3= list(ngrams(string1.split(" "), n))
ngrams4= list(ngrams(string2.split(" "), n))

common_trigrams = [x for x in ngrams3 if x in ngrams4]
score_trigram = len(common_trigrams)
print score_trigram
print 'Common Trigrams\n',common_trigrams

n = 4
ngrams5= list(ngrams(string1.split(" "), n))
ngrams6= list(ngrams(string2.split(" "), n))

common_4grams = [x for x in ngrams5 if x in ngrams6]
score_4gram = len(common_4grams)
print score_4gram
print 'Common 4-grams\n',common_4grams

print '\nTotal score :', 2*score_bigram+3*score_trigram+4*score_4gram