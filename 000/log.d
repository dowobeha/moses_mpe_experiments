Defined parameters (per moses.ini or switch):
	config: moses.d.ini 
	distortion-limit: 4 
	feature: PhrasePenalty UnknownWordPenalty WordPenalty Distortion KENLM name=StaticLM0 factor=0 path=static.lm PhraseDictionaryMemoryPerSentenceOnDemand name=DynamicPT0 num-features=4 tuneable=true input-factor=0 output-factor=0 table-limit=20 valuesAreProbabilities=false 
	input-factors: 0 
	mapping: 0 T 0 
	server: 
	server-port: 52732 
	verbose: 1 
	weight: PhrasePenalty0= 1 UnknownWordPenalty0= 1 WordPenalty0= -1 Distortion0= 0.2 StaticLM0= 0.5 DynamicPT0= 1 1 1 1 
line=PhrasePenalty
FeatureFunction: PhrasePenalty0 start: 0 end: 0
line=UnknownWordPenalty
FeatureFunction: UnknownWordPenalty0 start: 1 end: 1
line=WordPenalty
FeatureFunction: WordPenalty0 start: 2 end: 2
line=Distortion
FeatureFunction: Distortion0 start: 3 end: 3
line=KENLM name=StaticLM0 factor=0 path=static.lm
Loading the LM will be faster if you build a binary file.
Reading static.lm
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
The ARPA file is missing <unk>.  Substituting log10 probability -100.000.
****************************************************************************************************
FeatureFunction: StaticLM0 start: 4 end: 4
line=PhraseDictionaryMemoryPerSentenceOnDemand name=DynamicPT0 num-features=4 tuneable=true input-factor=0 output-factor=0 table-limit=20 valuesAreProbabilities=false
FeatureFunction: DynamicPT0 start: 5 end: 8
Loading PhrasePenalty0
Loading UnknownWordPenalty0
Loading WordPenalty0
Loading Distortion0
Loading StaticLM0
Loading DynamicPT0
RUN SERVER at pid 0
[moses/server/Server.cpp:49] Listening on port 52732
[moses/server/TranslationRequest.cpp:291] Input: <s> ich kaufe sie eine katze </s>
Translating: <s> ich kaufe sie eine katze </s> 
Line 0: Collecting options took 0.000 seconds at moses/Manager.cpp Line 141
Line 0: Search took 0.000 seconds
[moses/server/TranslationRequest.cpp:465] BEST TRANSLATION: <s> i buy you a cat </s> [1111111]  [total=-4.424] core=(4.000,0.000,-7.000,0.000,-9.210,1.843,-6.902,-0.223,-5.537)  
Signal of Class 15 received.  Exiting
