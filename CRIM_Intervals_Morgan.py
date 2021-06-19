#!/usr/bin/env python
# coding: utf-8

# ## Start CRIM Intervals
# 
# How to use Morgan Ngrams to examine musical files

# In[8]:


# import items from intervals and 
# get_ipython().run_line_magic('cd', '../intervals/')
import sys, os
sys.path.append(os.path.abspath(os.path.join('.', 'intervals')))
print(os.path.abspath(os.path.join('.', 'intervals')))

from main import *
import re
# from crim_intervals import *
import pandas as pd
import visualizations as viz

"""
# ## Load MEI Files from CRIM or Github by pasting one or more of [these links](https://docs.google.com/spreadsheets/d/1TzRqnzgcYYuQqZR78c5nizIsBWp4pnblm2wbU03uuSQ/edit?auth_email=rfreedma@haverford.edu#gid=0) below.
# 
# *Note:  each file must be in quotation marks and separated by commas
# 

# In[4]:


corpus = CorpusBase(['https://raw.githubusercontent.com/CRIM-Project/CRIM-online/master/crim/static/mei/MEI_3.0/CRIM_Model_0001.mei'])
# corpus = CorpusBase(['https://raw.githubusercontent.com/RichardFreedman/CRIM_additional_works/main/CRIM_Ave_Test.mei_msg.mei'])


# ## Give the scores short names, in order according to the way they were listed above
# * if more than one piece, then `piece1, piece2 = corpus.scores` 
# ** of course this can be `model`, `mass`, or any other name you like, as long as these are used in the requests for particular patterns below
# * if just one piece, then `model = corpus.scores[0]`
# 

# In[5]:


# model, mass = corpus.scores
model = corpus.scores[0]


# 
# ## Or batch process a series of files via the list below
# * Be sure to choose a directory as part of `a.to_csv(f"{short_title}.csv")`
# * You can use _any_ of the methods in the batch process below, so getNotes_Rests, etc.

# In[6]:


titles = ['https://crimproject.org/mei/CRIM_Model_0001.mei',  
'https://crimproject.org/mei/CRIM_Model_0002.mei',  
'https://crimproject.org/mei/CRIM_Model_0008.mei'
'https://crimproject.org/mei/CRIM_Model_0009.mei',  
'https://crimproject.org/mei/CRIM_Model_0010.mei',  
'https://crimproject.org/mei/CRIM_Model_0011.mei',  
'https://crimproject.org/mei/CRIM_Model_0012.mei',  
'https://crimproject.org/mei/CRIM_Model_0013.mei',  
'https://crimproject.org/mei/CRIM_Model_0014.mei',  
'https://crimproject.org/mei/CRIM_Model_0015.mei',  
'https://crimproject.org/mei/CRIM_Model_0016.mei',  
'https://crimproject.org/mei/CRIM_Model_0017.mei',  
'https://crimproject.org/mei/CRIM_Model_0019.mei',  
'https://crimproject.org/mei/CRIM_Model_0020.mei',  
'https://crimproject.org/mei/CRIM_Model_0021.mei',
'https://crimproject.org/mei/CRIM_Mass_0001_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0001_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0001_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0001_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0001_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0002_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0002_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0002_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0002_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0002_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0003_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0003_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0003_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0003_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0003_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0004_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0004_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0004_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0004_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0004_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0005_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0005_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0005_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0005_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0005_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0006_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0006_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0006_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0006_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0006_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0007_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0007_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0007_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0007_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0007_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0008_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0008_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0008_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0008_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0008_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0009_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0009_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0009_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0009_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0009_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0010_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0010_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0010_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0010_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0010_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0011_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0011_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0011_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0011_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0011_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0012_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0012_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0012_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0012_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0012_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0013_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0013_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0013_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0013_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0013_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0014_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0014_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0014_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0014_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0014_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0015_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0015_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0015_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0015_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0015_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0016_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0016_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0016_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0016_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0016_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0017_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0017_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0017_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0017_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0017_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0018_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0018_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0018_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0018_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0018_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0019_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0019_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0019_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0019_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0019_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0020_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0020_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0020_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0020_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0020_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0021_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0021_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0021_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0021_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0021_5.mei',  
'https://crimproject.org/mei/CRIM_Mass_0022_1.mei',  
'https://crimproject.org/mei/CRIM_Mass_0022_2.mei',  
'https://crimproject.org/mei/CRIM_Mass_0022_3.mei',  
'https://crimproject.org/mei/CRIM_Mass_0022_4.mei',  
'https://crimproject.org/mei/CRIM_Mass_0022_5.mei']


# In[9]:


for title in titles:
    try:
        short_title = re.search("([^\/]+$)", title)
        short_title.group()
        corpus = CorpusBase([title])
        piece = corpus.scores[0]
    #   a= piece.getMelodic()
        # a= piece.getNoteRest()
        a = piece.getNgrams(how='modules', cell_type=str)
        #a.to_csv(f"{short_title}.csv")
        # print(a.head())
    except:
        print("Has issues with importing, pass")


# ## Now apply various methods to the scores:
# * **getNoteRest** returns all the notes and rests, each voice as a column
# * **getDuration** returns the durations for all notes and rests, as above
# * **getMelodic** returns the melodic intervals in each voice as a column
# * **getHarmonic** returns pairs of harmonic intervals between each pair of voices
# * **getNgrams**  returns segments of various kinds, melodic (one voice) or modular (pairs of voices, including vertical and horizontal motion)
# ---
# 
# ### Pandas Tools:
# * **df.value_counts()**  returns summary for each pitch, duration for any type
# * save results as variable, then:**`.apply(pd.Series.value_counts).fillna(0).astype(int) `**
# ---
# 
# ### Documentation available via this command:
# * for any method, use the following read documentation:
# `print(model.getNgrams.__doc__)`
# 
# ---
# 

# In[13]:


print(model.getNgrams.__doc__)


# ## Methods and Parameters
# within parentheses, specify paramenters.  These are optional
# * kind="d" for diatonic with major(or q(uality), z(ero based), c(chromatic)
# * directed=True or False
# * compound=True or False
# * unit=2 (or whatever increment is preferred; 1=quarter note)

# In[6]:


d = model.getMelodic(kind="d", directed=True, compound=False)
print(d.head())


# # Notes and Rests
# 

# In[7]:


notes = model.getNoteRest()
notes.fillna(value= "-", inplace=True)
notes.reset_index()


# In[8]:


notes.value_counts()
# notes.stack().value_counts()


# In[9]:


df = notes.apply(pd.Series.value_counts).fillna(0).astype(int)
df


# # Melodic Intervals
# * kind='d' for diatonic; 's' for chromatic/semitone
# * To save as CSV:  
# `mel_int.to_csv('file_name.csv')`
# 

# In[10]:


mel_int = model.getMelodic(kind='d')
mel_int.fillna(value= "-", inplace=True)
mel_int.reset_index()


# # Durations
# 

# In[11]:


durs = model.getDuration()
durs.fillna(value= "-", inplace=True)


# ## Combine Notes and Durations as One DataFrame

# In[12]:


notes_durs = pd.concat([notes, durs], axis=1)
notes_durs


# # Select Columns for One Voice
# 

# In[26]:


notes_durs_s = notes_durs.iloc[:, [0,6]]
notes_durs_s
"""


# ## N-Grams in Each Voice
# * for Melodic or Durations

# In[14]:


corpus = CorpusBase(['https://crimproject.org/mei/CRIM_Model_0017.mei'])
model = corpus.scores[0]
mel = model.getMelodic(kind='d', compound=False, unit=4)
mel_ngrams = model.getNgrams(df=mel, n=4, cell_type=str)
mel_ngrams


# In[39]:


out2 = mel_ngrams[mel_ngrams == '1, 2, 1, 2'].stack().dropna().to_frame()
# out2.reset_index(inplace=True)
# out2["measure"] = out2['level_0']/8+1
# out2
out2.index.to_list()



har = model.getHarmonic()
# # regHar = model.regularize(df=har, unit=2)
# # regHar


# # In[196]:


harm = model.getHarmonic(kind="d", compound=True)
h_ng = model.getNgrams(df=harm, how='modules', exclude=['Rest'], cell_type="str")

viz.plot_ngrams_heatmap(h_ng)

h_ng.stack().value_counts().to_frame().head(50)


# # In[195]:


# out3 = h_ng[h_ng == '7_-, 6_-2, 8'].stack().dropna().to_frame()
# out3.reset_index(inplace=True)
# out3["measure"] = out3['level_0']/8+1
# out3


# # # Two-Voice Modules as N-Grams
# # 
# # * 'modules' is in fact the default
# # * 'unit' refers to the durational increment
# # 

# # In[14]:


# ng = model.getNgrams(df=harm, how='columnwise', exclude=['Rest'])
# ng.head()
# ng.stack().to_frame()


# # In[191]:


# ng2 = ng[ng.apply(lambda row: row.astype(str).str.contains('7, -, 6, -2, 8').any(), axis=1)].copy()
# # find_soggetto.reset_index(inplace=True)
# # find_soggetto["measure"] = find_soggetto['index']/8+1
# ng2.head(50)


# # # Filter by Any String of Intervals

# # In[ ]:




# filtered = ng[ng.apply(lambda row: row.astype(str).str.contains('7').any(), axis=1)].copy()
# # filtered = ng[ng.apply(lambda row: row.astype(str).str.contains('6_-2, 6_-2, 6').any(), axis=1)].copy()

# filtered.reset_index(inplace=True)
# filtered["measure"] = filtered['index']/8+1
# filtered


# # ## Ngrams with Real Durations

# # In[ ]:


# print(model.getNgrams.__doc__)


# # In[ ]:


# ng = model.getNgrams(how='modules', cell_type=str)
# ng


# # In[ ]:


# filtered = ng[ng.apply(lambda row: row.astype(str).str.contains('6_-2, 8').any(), axis=1)].copy()
# filtered.reset_index(inplace=True)
# # filtered["measure"] = filtered['index']/8+1
# filtered


# # In[ ]:


# df = ng.value_counts()
# df = ng.stack().value_counts()
# df.tail(50)


# # In[136]:


# corpus = CorpusBase(['https://crimproject.org/mei/CRIM_Mass_0015_2.mei'])
# model = corpus.scores[0]
# mel = model.getMelodic(kind='d')
# mel_ngrams = model.getNgrams(df=mel, n=4, cell_type=str)
# # mel_ngrams
# out = mel_ngrams[mel_ngrams == '-2, -3, 2, -2'].stack().dropna()
# out
# # out.reset_index(inplace=True)
# # out["measure"] = out['index']/8+1


# # In[57]:


# corpus = CorpusBase(['https://crimproject.org/mei/CRIM_Model_0017.mei'])
# model = corpus.scores[0]
# har = model.getHarmonic(kind='d')
# har_ngrams = model.getNgrams(how='modules', df=har, n=3, cell_type=str)
# # har_ngrams.to_csv('model_17_harmonic')

# har_ngrams[har_ngrams == '3_Held, 1_-2, 3'].stack().dropna()


# In[ ]:




