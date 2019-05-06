from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import string

def main():
    story=[];
    #read txt.
    with open("./Story.txt", "r") as fp:
        for i in fp:
            story.append(i);
    
    ready=[];
    for i in story:
        ready.append(getTextReady(i));
    
    kb={};
    getKnowledge(ready,kb);

    QuestionsAndAnswers(kb);

def getTextReady(line):
    stop_words = stopwords.words('english');
    #make all character lower case
    line=line.lower();
    #remove punctuation and widespaces
    line = line.translate(str.maketrans("","", string.punctuation));
    line = line.strip();

    #tockenize 
    tockenized=[]
    tockenized=word_tokenize(line);
    
    #tagg words
    tockenized=nltk.pos_tag(tockenized);

    #remove stop words
    filtered_words = [word for word in tockenized if word[0] not in stop_words];

    #Stemming
    stemmer= PorterStemmer();
    result=[];
    for i in filtered_words:
        temp=(stemmer.stem(i[0]),i[1]);
        result.append(temp);
    return result; 

def getKnowledge(story,kb):
    #populate kb with story
    for i in story:
        Noun=[];
        for indx,j in enumerate(i):
            if(indx==1):
                verb=j[0]
            else:
                Noun.append(j[0]);
        if verb in kb.keys():
            kb[verb].append(Noun);
        else:
            kb[verb]=[Noun];

def QuestionsAndAnswers(kb):
    stop=["stop","done","end"]
    yesorno=['did','does','is'];
    question=input("Please type your question:\n");
    question=question.lower();
    while not question in stop:
        first_word=question.partition(' ')[0];
        #analyze the question
        question=getTextReady(question);
        #generate the answer
        Noun=[];
        for indx,j in enumerate(question):
            if(indx==1):
                verb=j[0]
            else:
                Noun.append(j[0]);
                
        if (verb in kb.keys() and len(kb[verb])>0):
            if first_word in yesorno:
                exist=False;
                for i in range(len(kb[verb])):
                    cnt=0;
                    for j in Noun:
                        if j in kb[verb][i]:
                            cnt+=1;
                    if cnt==len(Noun):
                        exist=True;
                        break;
                if not exist:
                    print("No.");
                else:
                    print("Yes.");
            else:
                index=-1;
                max=0;
                for i in range(len(kb[verb])):
                    same=0;
                    same_words=[];
                    for j in Noun:
                        if j in kb[verb][i]:
                            same_words.append(j);

                        if len(same_words)>1:    
                            for z in range(len(same_words)-1):
                                if(kb[verb][i].index(same_words[z])<kb[verb][i].index(same_words[z+1])):
                                    same+=1;
                                else:
                                    same=-1;
                                    break;    
                        elif len(same_words)==0:
                            same=-1;
                            break;
                        else:
                            same=1;

                        if same>max:
                            index=i;
                            max=same;
                if index!= -1:
                    #formulate the answer.
                    answ_list=kb[verb][index];
                    answer=answ_list[0]+" "+verb;
                    for i in range(1,len(answ_list)):
                        answer=answer+" "+answ_list[i];
                    answer=answer+".";
                    print(answer);
                else:
                    print("I could not find an answer to that.");
        else:
                print("I could not find an answer to that.");

        #ask again
        question=input("Please type your question:\n");
        question=question.lower();


if(__name__=="__main__"):
    main();