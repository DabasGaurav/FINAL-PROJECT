import re
import nltk
import pandas as pd
import bs4
import requests
import spacy
from spacy import displacy
from networkx_query import search_nodes, search_edges
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher 
from spacy.tokens import Span 

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm

pd.set_option('display.max_colwidth', 200)



# --------------------------------------------------- GET RELATIONS ----------------------------------------------------------------------




def get_relation(sent):

  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1", None, pattern) 

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text)




# --------------------------------------------------- GET ENTITIES ----------------------------------------------------------------------





def get_entities(sent):
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  
  for tok in nlp(sent):
      
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
      
    if tok.dep_ != "punct":
        
      # check: token is a compound word or not
        
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
          
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
          
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
        
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
        
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text

  return [ent1.strip(), ent2.strip()]




# --------------------------------------------------------- MAIN ------------------------------------------------------------------------





text = """confused and frustrated, connie decides to leave on her own.
later, a woman’s scream is heard in the distance.
christian is then paralyzed by an elder.
the temple is set on fire.
outside, the cult wails with him.
it's a parable of a woman's religious awakening—
c. mackenzie, and craig vincent joined the cast.
later, craig di francia and action bronson were revealed to have joined the cast.
sebastian maniscalco and paul ben-victor were later revealed as being part of the cast.
we just tried to make the film.
we went through all these tests and things
m global was also circling to bid for the film's international sales rights.
canadian musician robbie robertson supervised the soundtrack.
it features both original and existing music tracks.
it is the worst reviewed film in the franchise.
but she injures quicksilver and accidentally kills mystique before flying away.
military forces tasked with her arrest.
the train is attacked by vuk and her d'bari forces.
kota eberhardt portrays telepath selene gallio,
singer did not return to direct the sequel, x-men:
the last stand, which was written by penn and simon kinberg.
jessica chastain was also potentially being considered for the same character.
mauro fiore served as cinematographer.
filming was completed on october 14, 2017.
the soundtrack was released digitally on june 7.
the album was released digitally on august 2, 2019.
the film is distributed by walt disney studios motion pictures.
it ended up debuting to just $103.7 million internationally and $136.5 million worldwide.
the film stars kyle chandler, vera farmiga, millie bobby brown, bradley whitford, sally hawkins, charles dance, thomas middleditch, aisha hinds, o'shea jackson jr., david strathairn, ken watanabe, and zhang ziyi.
it is dedicated to executive producer yoshimitsu banno and original godzilla suit
vivienne graham approach former employee dr.
emma frees and awakens monster zero, which kills several monarch members, including dr.
disillusioned, madison disowns her mother.through mythological texts, dr.
joe morton appears as an older dr.
godzilla, rodan, mothra, and king ghidorah were credited as themselves.
when asked about his reaction to being asked to direct, dougherty stated, 'yes.'
we're empathizing with godzilla.
legendary's only mandate was to include monarch, rodan, mothra, and king ghidorah.
ten writers contributed to building on the treatment.
the script took a year to come together.
dougherty also changed, revised, and improved lines during filming and post-production.
due to this, the film became an ensemble piece.
it can't just look like big dinosaurs.
other actors perform the body.
production designer scott chambliss managed all the art directors.
the single was released on may 13, 2019.

all tracks are written by bear mccreary, except where noted.
the score is also conducted by mccreary.

on december 10, 2018, the film's first teaser poster and ccxp trailer were released.
in april 2019, the main theatrical poster was released online.
the film was originally scheduled to be released on june 8, 2018.
the collectible tickets were offered in two sizes: standard  and godzilla-sized .
the 4k release includes hdr10, hdr10
the retail exclusives will also include limited special clear files.
such heroes are ready with one-liners, puns, and dry quips.
it was action with a science fiction twist.
currently, action films requiring extensive stunt work and special effects tend to be expensive.
examples include the indiana jones franchise and many superhero films.
themes or elements often prevalent in typical action-horror films
paul blart: mall cop is a recent spoof of this trend .
they are usually the films' primary appeal and entertainment value and are often the method of storytelling, character expression, and development.
both had many roles.
the producer also supervises the pre-production, production, and post-production stages of filmmaking.
finally, the producer will oversee the marketing and distribution.
the line producer can be credited as produced by in certain cases.
however, most producers start in a college, university or film school.
some film directors started as screenwriters, cinematographers, producers, film editors or actors.
other film directors have attended a film school.
directors use different approaches.
some directors also take on additional roles, such as producing, writing or editing.
some film schools are equipped with sound stages and post-production facilities.
a full degree course can be designed for up to five years of studying.
the german film and television academy berlin consequently cooperates with the berlin/brandenburg tv station rbb  and arte.
la femis in paris, tel aviv university, and vancouver film school.
the national film awards is the most prominent film award ceremonies in india.
the awards were first presented in 1954.
the national film awards are presented in two main categories: feature films and non-feature films.
he returns home and enters sophie's apartment.
a mass riot breaks out in gotham.
arthur is imprisoned at arkham state hospital.
after his film war dogs premiered in august 2016.
we're not even doing joker, but the story of becoming joker.
and then we'd reshoot that three weeks later.
that month, dante pereira-olson and douglas hodge joined the cast.
it is scheduled to be released theatrically by warner bros.
it's really been eye-opening for me.
i can't wait to see it.
they did it.
i can't wait to see it.
they did it.
film is a 1965 short film written by samuel beckett, his only screenplay.
a second draft was produced by 22 may and a 40-leaf shooting script followed thereafter.
both beckett and the director alan schneider were interested in zero mostel and jack macgowran.
beckett then suggested buster keaton.
this being his only visit to the united states.
david rayner clark directed max wall.
suddenly, the camera  shifts violently to the left.
the couple look at each other and the man
the camera cuts to the vestibule.
the camera gives us a brief close-up.
she descends slowly and with fumbling feet.
she closes her eyes and collapses.
his coat tails are seen flying up the stairs.
although stated simply, the mechanics needed to execute these tasks are laborious .
he ignores them and sits.
he still has the eye patch.
he half starts from the chair, then stiffens.
“esse est percipi aut percipere” .
but he can't get away from himself.
but e is also self, not merely o’s self but the self of any person or people,
e is, so to speak, o's blind eye.
beckett's script has been interpreted in various ways.
the viewers are being asked to consider the work structurally and dramatically rather than emotionally or philosophically.
however, for this particular project, beckett became personally involved.
four directors worked on the series: chris columbus, alfonso cuarón, mike newell, and david yates.
he went out and bought the book, becoming an instant fan.
david heyman was confirmed to produce the film.
their only previous acting experience was in school plays.
barron was later appointed producer on the last four films.
other executive producers include tanya seghatchian and lionel wigram.
but he expressed real passion.
all the directors have been supportive of each other.
the production designer for all eight films is stuart craig.
the  definitely wasn't there originally, and so we were able to add that substantial piece.
the harry potter series has had four composers.
desplat returned to score harry potter and the deathly hallows
– part 2 in 2011.
they came up trumps.
as the director shouts cut for the very last time.
harry potter is an orphaned boy brought up by his unkind muggle  aunt and uncle.
however, part 2 was released in 2d and 3d cinemas as originally planned.
by january 2017, johns and berg reported to emmerich.
principal photography began on august 1, 2011.
, with david ayer confirmed as director.
affleck as bruce wayne / batman and miller as barry allen
justice league was released worldwide on november 17, 2017.
aquaman was announced in october.
pre-production began in august.
the villain mister mind is introduced in a mid-credits scene.
that same month, the sequel was officially announced at san diego comic-con.
pre-production had begun by early december 2017.
that same month, pedro pascal was also cast in a key role.
other filming locations include the warner bros.
wonder woman 1984 is scheduled to be released on june 5, 2020.
the initial script was drafted by berlanti, geoff johns, chris brancato, michael green and marc guggenheim.
dan mazeau was brought on as co-writer.
in march 2018, john francis daley and jonathan goldstein were hired to co-direct.
miller revealed that the plot will involve the speed force multiverse.
pre-production is scheduled to begin by january 2020.
the flash is expected to be released sometime in 2021.
through emmerich and producer peter safran, who were receptive.
pre-production is expected to begin in 2020.
aquaman 2 is scheduled to be released on december 16, 2022.
suicide squad occurred shortly after batman v superman.
by january 2017, johns and berg reported to emmerich.
principal photography began on august 1, 2011.
, with david ayer confirmed as director.
affleck as bruce wayne / batman and miller as barry allen
justice league was released worldwide on november 17, 2017.
aquaman was announced in october.
pre-production began in august.
the villain mister mind is introduced in a mid-credits scene.
that same month, the sequel was officially announced at san diego comic-con."""



sentences = nltk.sent_tokenize(text)

entity_pairs = []

for sent in sentences:
  entity_pairs.append(get_entities(sent))

relations = [get_relation(i) for i in sentences]




# ---------------------------------------------- CONVERT LIST TO GRAPH ----------------------------------------------------------------------




# extract subject
source = [i[0] for i in entity_pairs]

# extract object
target = [i[1] for i in entity_pairs]

c1 = 1
c2 = 1

g = nx.DiGraph()
for i in range(len(source)): 
    g.add_node(c1, product=source[i])
    g.add_node(-c1, product=target[i])
    g.add_edge(c1, -c1, action=relations[i])
    c1=c1+1




# ------------------------------------------------------ PLOT GRAPH ----------------------------------------------------------------------





plt.figure(figsize=(12,12))

pos = nx.spring_layout(g)
nx.draw(g, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()




# ------------------------------------------------------ QUERY GRAPH ----------------------------------------------------------------------



question = """ what was set on fire """

questionentities= get_entities(question)
print(questionentities)




for node_id in search_nodes(g, {"==": [("product",), questionentities[1]]}):
    ans = node_id

if(ans>0):
    print(sentences[ans-1])
else:
    print(sentences[-(ans)-1])



