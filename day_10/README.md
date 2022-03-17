# Apple Podcasts recommendations walker

---
```
Language: Python
Brief: Walk podcast recommendations to a specified depth
Scope: experiment
Tags: web, disinformation
State: 
Result: 
```
---

Inspired by [trapezoid of discovery](https://twitter.com/get_innocuous) on Twitter's disinformation research work on a rightward ratchet of ideology.

Start with a search term, get recommendations, for each of those podcasts get the recommended podcasts, repeat. Put results in a tree.


### Results

Works pretty well. Only to a depth of one-podcast. 

I'm really interested in being able to pust JSON documents into an SQL DB mediated though SQLalchemy. I'm going to return to that for knowledge graphs.

### If I was to do more

- Extend to do recursion on podcast recommendations through the iTunes category algorithm. Should not be hard to do other than keeping track of depth to avoid infinite loops.
- Put the output into a format better suited for visualization. Like neo4j
- Rethink the Nodes and Edges SQLAlchemy objects. Make generic Node and Edge classes that are extended by specific types like a PodcastNode.

### Example output

```
The #1 recommended podcast for Search term 'biden' Rubicon: The First Hundred Days of the Biden Presidency (Crooked Media)
	Lovett or Leave It
	Hysteria
	What A Day
	Pod Save the World
	Pod Save America
	The Daily
	Offline with Jon Favreau
	The Argument
	Up First
	The NPR Politics Podcast
	FiveThirtyEight Politics
	The Rachel Maddow Show
	Political Gabfest
	Keep It!
	Fresh Air
	The Daily
	Up First
	The Ben Shapiro Show
	Serial
	The Charlie Kirk Show
	The Dan Bongino Show
	State of Ukraine
	Sent Away
	The Glenn Beck Program
	Global News Podcast
	NPR News Now
	Morning Wire
	The Matt Walsh Show
	Sweet Bobby
	Bannon's War Room
	Pod Save America
	Pod Save the World
	Foundering
	The Michael Knowles Show
	The Megyn Kelly Show
	Pod Save America
	Pod Save the World
	What A Day
	Lovett or Leave It
	Hysteria
	Keep It!
	This Land
	America Dissected
	Pod Save the People
	Takeline
The #2 recommended podcast for Search term 'biden' Biden's Briefing (Joe Biden)
	The Joe Budden Podcast
	Drink Champs
	New Rory & MAL
	"See, The Thing Is..."
	Hotboxin With Mike Tyson
	CNN Political Briefing
	Apple News Today
	Global News Podcast
	The NPR Politics Podcast
	The Ben Shapiro Show
	The Daily
	Up First
	The Money with Katie Show
	Office Ladies
	Hidden Brain
	Biden's Briefing
	The Daily
	Up First
	The Ben Shapiro Show
	Serial
	The Charlie Kirk Show
	The Dan Bongino Show
	State of Ukraine
	Sent Away
	The Glenn Beck Program
	Global News Podcast
	NPR News Now
	Morning Wire
	The Matt Walsh Show
	Sweet Bobby
	Bannon's War Room
	Pod Save America
	Pod Save the World
	Foundering
	The Michael Knowles Show
	The Megyn Kelly Show
The #3 recommended podcast for Search term 'biden' Ridin’ With Biden (Biden War Room)
	Bannon's War Room
	Sharon Says So
	The Lawfare Podcast
	Democracy Decoded
	Strict Scrutiny
	Fever Dreams
	Deep State Radio
	Pitchfork Economics with Nick Hanauer
	The Real Story
	5-4
	Macroaggressions
	Future Hindsight
	Anne Hidalgo - Paris en Commun
	Civics 101
	What Roman Mars Can Learn About Con Law
	Radiolab Presents: More Perfect
	Zero Blog Thirty
	SOFcast
	The Truth of the Matter
	First Things Podcast
	سقراط مع عمر الجريسي
The #4 recommended podcast for Search term 'biden' Vice President Biden and The Middle Class Task Force - Task Force Meeting (Vice President  Joe Biden & Timothy Geithner)
	School of Freshwater Sciences - All Things Water
	Great Lakes Water Institute - Research
	El Futuro Maya - El Futuro Maya
	George F. Kennan Distinguished Lecture Series
	School of Information Studies - School of Information Studies
	Institute of World Affairs - International Focus
	Poetry Everywhere
	School of Information Studies - Info Retrieval Seminars
	Rigoberta Menchu Tum - Rigoberta Menchu Tum
	School of Public Health - Public Health Messages
	The Daily
	Up First
	The Ben Shapiro Show
	Serial
	The Charlie Kirk Show
	The Dan Bongino Show
	State of Ukraine
	Sent Away
	The Glenn Beck Program
	Global News Podcast
	NPR News Now
	Morning Wire
	The Matt Walsh Show
	Sweet Bobby
	Bannon's War Room
	Pod Save America
	Pod Save the World
	Foundering
	The Michael Knowles Show
	The Megyn Kelly Show
The #5 recommended podcast for Search term 'biden' Please Don’t Make Me Vote for Joe Biden (POODCAST Productions)
	The Daily
	Up First
	The Ben Shapiro Show
	Serial
	The Charlie Kirk Show
	The Dan Bongino Show
	State of Ukraine
	Sent Away
	The Glenn Beck Program
	Global News Podcast
	NPR News Now
	Morning Wire
	The Matt Walsh Show
	Sweet Bobby
	Bannon's War Room
	Pod Save America
	Pod Save the World
	Foundering
	The Michael Knowles Show
	The Megyn Kelly Show
The #6 recommended podcast for Search term 'biden' The Biden Transition Podcast (Danielle McLean)
	The Daily
	Up First
	The Ben Shapiro Show
	Serial
	The Charlie Kirk Show
	The Dan Bongino Show
	State of Ukraine
	Sent Away
	The Glenn Beck Program
	Global News Podcast
	NPR News Now
	Morning Wire
	The Matt Walsh Show
	Sweet Bobby
	Bannon's War Room
	Pod Save America
	Pod Save the World
	Foundering
	The Michael Knowles Show
	The Megyn Kelly Show
The #7 recommended podcast for Search term 'biden' Insider Insights: 100 Days of Biden (Buchanan Ingersoll & Rooney)
The #8 recommended podcast for Search term 'biden' The “Sleepy 😴 Joe Biden Radio Show✊🏾” (TheBlackJoeBidenradio✊🏿)
The #9 recommended podcast for Search term 'biden' Group 12: Joe Biden (Anika Wagner)
The #10 recommended podcast for Search term 'biden' Trump Vs Biden (Kalel Jones)
The #11 recommended podcast for Search term 'biden' Biden Time (Audio Porridge)
The #12 recommended podcast for Search term 'biden' First Public Address of President Joe Biden (Valentin Sarte)
The #13 recommended podcast for Search term 'biden' HPR Talk: Biden's 100 Days (Harvard Political Review)
The #14 recommended podcast for Search term 'biden' Joe Biden? (Drinking Water)
The #15 recommended podcast for Search term 'biden' Is it right for Joe Biden to remove the bust of Winston Churchill from the Oval Office? (Politiking)
The #16 recommended podcast for Search term 'biden' Ohio shooting, Biden, NYC police (Adam Mintz)

```
