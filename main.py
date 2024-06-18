import syllables
import os
import csv
    
file=open("positive-words.txt",'r')
positive_dict={} 
for x in file:
    if x not in positive_dict:
        positive_dict[x[:len(x)-1]]=1 

file=open("negative-words.txt",'r')
negative_dict={} 
for x in file:
    if x not in negative_dict:
        negative_dict[x[:len(x)-1]]=1 

stop=set()

file=open('StopWords/StopWords_Auditor.txt','r')
for x in file:
    stop.add(x[:len(x)-1].lower())
file2=open('StopWords/StopWords_Currencies.txt','r')
for x in file2:
    stop.add(x[:len(x)-1].lower())
file3=open('StopWords/StopWords_DatesandNumbers.txt','r') 
for x in file3:
    stop.add(x[:len(x)-1].lower())
file4=open('StopWords/StopWords_Generic.txt','r')
for x in file4:
    stop.add(x[:len(x)-1].lower())
file5=open('StopWords/StopWords_GenericLong.txt','r')
for x in file5:
    stop.add(x[:len(x)-1].lower())
file6=open('StopWords/StopWords_Geographic.txt','r')
for x in file6:
    stop.add(x[:len(x)-1].lower())
file7=open('StopWords/StopWords_Names.txt','r')
for x in file7:
    stop.add(x[:len(x)-1].lower())

check=['','-',':',',','?','/','!','@','#','$','%','&','\n']


ans=[]
files=os.listdir('C:/Users/saipr/Desktop/TEXT')
for filename in files:
    f=open(f'C:/Users/saipr/Desktop/TEXT/{filename}','r',encoding='utf8')
    text=f.read()
    length=[] 
    total_number_of_characters=0
    arr=[]

    PRONOUNS={"i":0,"we":0, "my":0 ,"ours":0,"us":0}
    curr_length=0
    POSITIVE_SCORE=0 
    NEGATIVE_SCORE=0
    SYLLABLES_COUNT_PER_WORD=0
    COMPLEX_WORDS=0
    s=''
    for i in text:
        if i==' ':
            if s=='':
                continue
            else:
                if s in PRONOUNS:
                    PRONOUNS[s]=PRONOUNS[s]+1
                if s.lower() not in stop:
                    if syllables.estimate(s.lower())>2:
                        COMPLEX_WORDS=COMPLEX_WORDS+1 
                    SYLLABLES_COUNT_PER_WORD=SYLLABLES_COUNT_PER_WORD+syllables.estimate(s.lower())
                    arr.append(s.lower())
                    if s.lower() in positive_dict:
                        POSITIVE_SCORE=POSITIVE_SCORE+1 
                    if s.lower() in negative_dict:
                        NEGATIVE_SCORE=NEGATIVE_SCORE+1
                    total_number_of_characters=total_number_of_characters+len(s)
            s=''
        elif i in check:
            continue 
        elif i=='.':
            if s=='':
                continue
            else:
                if s in PRONOUNS:
                    PRONOUNS[s]=PRONOUNS[s]+1
                if s.lower() not in stop:
                    arr.append(s.lower())
                    if s.lower() in positive_dict:
                        POSITIVE_SCORE=POSITIVE_SCORE+1 
                    if s.lower() in negative_dict:
                        NEGATIVE_SCORE=NEGATIVE_SCORE+1
                    total_number_of_characters=total_number_of_characters+len(s)
            length.append(len(arr)-curr_length)
            curr_length=len(arr)
            s=''
        else:
            s=s+i
      
    if s in PRONOUNS:
        PRONOUNS[s]=PRONOUNS[s]+1
    if s.lower() not in stop:
        arr.append(s.lower())
        if s.lower() in positive_dict:
            POSITIVE_SCORE=POSITIVE_SCORE+1 
        if s.lower() in negative_dict:
            NEGATIVE_SCORE=NEGATIVE_SCORE+1
        length.append(len(arr)-curr_length)
        curr_length=len(arr)
        total_number_of_characters=total_number_of_characters+len(s)



    POLARITY_SCORE=(POSITIVE_SCORE-NEGATIVE_SCORE)/((POSITIVE_SCORE+NEGATIVE_SCORE)+0.000001)
    SUBJECTIVE_SCORE=(POSITIVE_SCORE+NEGATIVE_SCORE)/((len(arr))+0.000001)
    AVERAGE_SENTENCE_LENGTH=len(arr)/len(length)
    AVERAGE_NUMBER_OF_WORDS_PER_SENTENCE=len(arr)/len(length)
    WORD_COUNT=len(arr)
    AVERAGE_WORD_LENGTH=total_number_of_characters/len(arr)
    PERCENTAGE_OF_COMPLEX_WORDS=COMPLEX_WORDS/len(arr) 
    FOG_INDEX=(AVERAGE_SENTENCE_LENGTH+PERCENTAGE_OF_COMPLEX_WORDS)*(0.4)
    PERSONAL_PRONOUNS=sum(PRONOUNS.values())
    ans.append([str(POSITIVE_SCORE),str(NEGATIVE_SCORE),str(POLARITY_SCORE),str(SUBJECTIVE_SCORE),str(AVERAGE_SENTENCE_LENGTH),str(PERCENTAGE_OF_COMPLEX_WORDS),str(FOG_INDEX),str(AVERAGE_NUMBER_OF_WORDS_PER_SENTENCE),str(COMPLEX_WORDS),str(WORD_COUNT),str(SYLLABLES_COUNT_PER_WORD),str(PERSONAL_PRONOUNS),str(AVERAGE_WORD_LENGTH)])
columns=['POSITIVE SCORE',
'NEGATIVE SCORE',
'POLARITY SCORE',
'SUBJECTIVITY SCORE',
'AVG SENTENCE LENGTH',
'PERCENTAGE OF COMPLEX WORDS',
'FOG INDEX',
'AVG NUMBER OF WORDS PER SENTENCE',
'COMPLEX WORD COUNT',
'WORD COUNT',
'SYLLABLE PER WORD',
'PERSONAL PRONOUNS',
'AVG WORD LENGTH'
] 
with open('ans.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    csvwriter.writerows(ans)