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
	Lovett or Leave It (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	What A Day (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	Hysteria (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	FiveThirtyEight Politics (FiveThirtyEight, 538, ABC News, Nate Silver) [Apple itunes algorithm category 'podcast_by_subscriber']
	Offline with Jon Favreau (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	The NPR Politics Podcast (NPR) [Apple itunes algorithm category 'podcast_by_subscriber']
	Political Gabfest (Slate Podcasts) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Axe Files with David Axelrod (The Institute of Politics & CNN) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Al Franken Podcast (ASF Productions) [Apple itunes algorithm category 'podcast_by_subscriber']
	Keep It! (Crooked Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Daily (The New York Times) [Apple itunes algorithm category 'podcast_by_subscriber']
	Fresh Air (NPR) [Apple itunes algorithm category 'podcast_by_subscriber']
	CounterSpin (Fairness & Accuracy In Reporting) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Daily (The New York Times) [Apple itunes algorithm category 'podcasts_by_genera']
	Up First (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	The Ben Shapiro Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Serial (Serial Productions) [Apple itunes algorithm category 'podcasts_by_genera']
	The Charlie Kirk Show (Charlie Kirk) [Apple itunes algorithm category 'podcasts_by_genera']
	The Dan Bongino Show (Cumulus Podcast Network | Dan Bongino) [Apple itunes algorithm category 'podcasts_by_genera']
	State of Ukraine (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Sent Away (APM Reports, KUER and The Salt Lake Tribune) [Apple itunes algorithm category 'podcasts_by_genera']
	The Glenn Beck Program (Blaze Podcast Network) [Apple itunes algorithm category 'podcasts_by_genera']
	Global News Podcast (BBC World Service) [Apple itunes algorithm category 'podcasts_by_genera']
	NPR News Now (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Morning Wire (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Matt Walsh Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Sweet Bobby (Tortoise Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Bannon's War Room (WarRoom.org) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Foundering (Bloomberg) [Apple itunes algorithm category 'podcasts_by_genera']
	The Michael Knowles Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Megyn Kelly Show (SiriusXM) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	What A Day (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	Lovett or Leave It (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	Hysteria (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	Keep It! (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	This Land (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	America Dissected (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	Pod Save the People (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
	Takeline (Crooked Media) [Apple itunes algorithm category 'podcasts_by_artist']
The #2 recommended podcast for Search term 'biden' Biden's Briefing (Joe Biden)
	The Joe Budden Podcast (The Joe Budden Network) [Apple itunes algorithm category 'podcast_by_subscriber']
	Drink Champs (The Black Effect and iHeartPodcasts) [Apple itunes algorithm category 'podcast_by_subscriber']
	New Rory & MAL (Rory Farrell & Jamil "Mal" Clay) [Apple itunes algorithm category 'podcast_by_subscriber']
	"See, The Thing Is..." (All The Things Productions) [Apple itunes algorithm category 'podcast_by_subscriber']
	Hotboxin With Mike Tyson (Malka Media) [Apple itunes algorithm category 'podcast_by_subscriber']
	CNN Political Briefing (CNN) [Apple itunes algorithm category 'podcast_by_subscriber']
	Apple News Today (Apple News) [Apple itunes algorithm category 'podcast_by_subscriber']
	Global News Podcast (BBC World Service) [Apple itunes algorithm category 'podcast_by_subscriber']
	The NPR Politics Podcast (NPR) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Ben Shapiro Show (The Daily Wire) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Daily (The New York Times) [Apple itunes algorithm category 'podcast_by_subscriber']
	Up First (NPR) [Apple itunes algorithm category 'podcast_by_subscriber']
	The Money with Katie Show (Morning Brew) [Apple itunes algorithm category 'podcast_by_subscriber']
	Office Ladies (Earwolf & Jenna Fischer and Angela Kinsey) [Apple itunes algorithm category 'podcast_by_subscriber']
	Hidden Brain (Hidden Brain) [Apple itunes algorithm category 'podcast_by_subscriber']
	Biden's Briefing (Joe Biden) [Apple itunes algorithm category 'podcasts_by_artist']
	The Daily (The New York Times) [Apple itunes algorithm category 'podcasts_by_genera']
	Up First (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	The Ben Shapiro Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Serial (Serial Productions) [Apple itunes algorithm category 'podcasts_by_genera']
	The Charlie Kirk Show (Charlie Kirk) [Apple itunes algorithm category 'podcasts_by_genera']
	The Dan Bongino Show (Cumulus Podcast Network | Dan Bongino) [Apple itunes algorithm category 'podcasts_by_genera']
	State of Ukraine (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Sent Away (APM Reports, KUER and The Salt Lake Tribune) [Apple itunes algorithm category 'podcasts_by_genera']
	The Glenn Beck Program (Blaze Podcast Network) [Apple itunes algorithm category 'podcasts_by_genera']
	Global News Podcast (BBC World Service) [Apple itunes algorithm category 'podcasts_by_genera']
	NPR News Now (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Morning Wire (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Matt Walsh Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Sweet Bobby (Tortoise Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Bannon's War Room (WarRoom.org) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Foundering (Bloomberg) [Apple itunes algorithm category 'podcasts_by_genera']
	The Michael Knowles Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Megyn Kelly Show (SiriusXM) [Apple itunes algorithm category 'podcasts_by_genera']
The #3 recommended podcast for Search term 'biden' Ridin’ With Biden (Biden War Room)
	Bannon's War Room (WarRoom.org) [Apple itunes algorithm category 'podcast_by_subscriber']
	Sharon Says So (Sharon McMahon) [Apple itunes algorithm category 'podcasts_by_genera']
	The Lawfare Podcast (The Lawfare Institute) [Apple itunes algorithm category 'podcasts_by_genera']
	Democracy Decoded (Campaign Legal Center) [Apple itunes algorithm category 'podcasts_by_genera']
	Strict Scrutiny (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Fever Dreams (The Daily Beast) [Apple itunes algorithm category 'podcasts_by_genera']
	Deep State Radio (The DSR Network) [Apple itunes algorithm category 'podcasts_by_genera']
	Pitchfork Economics with Nick Hanauer (Civic Ventures) [Apple itunes algorithm category 'podcasts_by_genera']
	The Real Story (BBC World Service) [Apple itunes algorithm category 'podcasts_by_genera']
	5-4 (Prologue Projects) [Apple itunes algorithm category 'podcasts_by_genera']
	Macroaggressions (Charlie Robinson) [Apple itunes algorithm category 'podcasts_by_genera']
	Future Hindsight (Mila Atmos) [Apple itunes algorithm category 'podcasts_by_genera']
	Anne Hidalgo - Paris en Commun (Paris en Commun) [Apple itunes algorithm category 'podcasts_by_genera']
	Civics 101 (New Hampshire Public Radio) [Apple itunes algorithm category 'podcasts_by_genera']
	What Roman Mars Can Learn About Con Law (Roman Mars) [Apple itunes algorithm category 'podcasts_by_genera']
	Radiolab Presents: More Perfect (WNYC Studios) [Apple itunes algorithm category 'podcasts_by_genera']
	Zero Blog Thirty (Barstool Sports) [Apple itunes algorithm category 'podcasts_by_genera']
	SOFcast (US Special Operations Command) [Apple itunes algorithm category 'podcasts_by_genera']
	The Truth of the Matter (CSIS | Center for Strategic and International Studies) [Apple itunes algorithm category 'podcasts_by_genera']
	First Things Podcast (First Things) [Apple itunes algorithm category 'podcasts_by_genera']
	سقراط مع عمر الجريسي (ثمانية/ thmanyah) [Apple itunes algorithm category 'podcasts_by_genera']
The #4 recommended podcast for Search term 'biden' Vice President Biden and The Middle Class Task Force - Task Force Meeting (Vice President  Joe Biden & Timothy Geithner)
	The Daily (The New York Times) [Apple itunes algorithm category 'podcasts_by_genera']
	Up First (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	The Ben Shapiro Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Serial (Serial Productions) [Apple itunes algorithm category 'podcasts_by_genera']
	The Charlie Kirk Show (Charlie Kirk) [Apple itunes algorithm category 'podcasts_by_genera']
	The Dan Bongino Show (Cumulus Podcast Network | Dan Bongino) [Apple itunes algorithm category 'podcasts_by_genera']
	State of Ukraine (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Sent Away (APM Reports, KUER and The Salt Lake Tribune) [Apple itunes algorithm category 'podcasts_by_genera']
	The Glenn Beck Program (Blaze Podcast Network) [Apple itunes algorithm category 'podcasts_by_genera']
	Global News Podcast (BBC World Service) [Apple itunes algorithm category 'podcasts_by_genera']
	NPR News Now (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Morning Wire (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Matt Walsh Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Sweet Bobby (Tortoise Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Bannon's War Room (WarRoom.org) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Foundering (Bloomberg) [Apple itunes algorithm category 'podcasts_by_genera']
	The Michael Knowles Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Megyn Kelly Show (SiriusXM) [Apple itunes algorithm category 'podcasts_by_genera']
	School of Freshwater Sciences - All Things Water (University of Wisconsin Milwaukee) [Apple itunes algorithm category 'podcasts_by_artist']
	Great Lakes Water Institute - Research (GLWI Staff) [Apple itunes algorithm category 'podcasts_by_artist']
	El Futuro Maya - El Futuro Maya (CLACS) [Apple itunes algorithm category 'podcasts_by_artist']
	George F. Kennan Distinguished Lecture Series (Institute of World Affairs) [Apple itunes algorithm category 'podcasts_by_artist']
	School of Information Studies - School of Information Studies (University of Wisconsin Milwaukee) [Apple itunes algorithm category 'podcasts_by_artist']
	Institute of World Affairs - International Focus (Institute of World Affairs) [Apple itunes algorithm category 'podcasts_by_artist']
	Poetry Everywhere (UW Milwaukee Creative Writing) [Apple itunes algorithm category 'podcasts_by_artist']
	School of Information Studies - Info Retrieval Seminars (University of Wisconsin Milwaukee) [Apple itunes algorithm category 'podcasts_by_artist']
	Rigoberta Menchu Tum - Rigoberta Menchu Tum (Menchu Tum) [Apple itunes algorithm category 'podcasts_by_artist']
	School of Public Health - Public Health Messages (School of Public Health) [Apple itunes algorithm category 'podcasts_by_artist']
The #5 recommended podcast for Search term 'biden' Please Don’t Make Me Vote for Joe Biden (POODCAST Productions)
	The Daily (The New York Times) [Apple itunes algorithm category 'podcasts_by_genera']
	Up First (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	The Ben Shapiro Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Serial (Serial Productions) [Apple itunes algorithm category 'podcasts_by_genera']
	The Charlie Kirk Show (Charlie Kirk) [Apple itunes algorithm category 'podcasts_by_genera']
	The Dan Bongino Show (Cumulus Podcast Network | Dan Bongino) [Apple itunes algorithm category 'podcasts_by_genera']
	State of Ukraine (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Sent Away (APM Reports, KUER and The Salt Lake Tribune) [Apple itunes algorithm category 'podcasts_by_genera']
	The Glenn Beck Program (Blaze Podcast Network) [Apple itunes algorithm category 'podcasts_by_genera']
	Global News Podcast (BBC World Service) [Apple itunes algorithm category 'podcasts_by_genera']
	NPR News Now (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Morning Wire (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Matt Walsh Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Sweet Bobby (Tortoise Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Bannon's War Room (WarRoom.org) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Foundering (Bloomberg) [Apple itunes algorithm category 'podcasts_by_genera']
	The Michael Knowles Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Megyn Kelly Show (SiriusXM) [Apple itunes algorithm category 'podcasts_by_genera']
The #6 recommended podcast for Search term 'biden' The Biden Transition Podcast (Danielle McLean)
	The Daily (The New York Times) [Apple itunes algorithm category 'podcasts_by_genera']
	Up First (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	The Ben Shapiro Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Serial (Serial Productions) [Apple itunes algorithm category 'podcasts_by_genera']
	The Charlie Kirk Show (Charlie Kirk) [Apple itunes algorithm category 'podcasts_by_genera']
	The Dan Bongino Show (Cumulus Podcast Network | Dan Bongino) [Apple itunes algorithm category 'podcasts_by_genera']
	State of Ukraine (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Sent Away (APM Reports, KUER and The Salt Lake Tribune) [Apple itunes algorithm category 'podcasts_by_genera']
	The Glenn Beck Program (Blaze Podcast Network) [Apple itunes algorithm category 'podcasts_by_genera']
	Global News Podcast (BBC World Service) [Apple itunes algorithm category 'podcasts_by_genera']
	NPR News Now (NPR) [Apple itunes algorithm category 'podcasts_by_genera']
	Morning Wire (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Matt Walsh Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	Sweet Bobby (Tortoise Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Bannon's War Room (WarRoom.org) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save America (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Pod Save the World (Crooked Media) [Apple itunes algorithm category 'podcasts_by_genera']
	Foundering (Bloomberg) [Apple itunes algorithm category 'podcasts_by_genera']
	The Michael Knowles Show (The Daily Wire) [Apple itunes algorithm category 'podcasts_by_genera']
	The Megyn Kelly Show (SiriusXM) [Apple itunes algorithm category 'podcasts_by_genera']
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
The #17 recommended podcast for Search term 'biden' President Biden Really Needs to Try British Candy (Annetta Goodwin)
The #18 recommended podcast for Search term 'biden' Biden on Afghanistan withdrawal: 'This is about America leading the world' (viva)
The #19 recommended podcast for Search term 'biden' Biden our Time (Anna Ward)
The #20 recommended podcast for Search term 'biden' GoodBye Trump and Welcome Biden USA (Alina Ali)
The #21 recommended podcast for Search term 'biden' The Biden Years (Studio O Creative)
The #22 recommended podcast for Search term 'biden' What Biden's Approach to China Could Mean for Tech (Mildreds Ellis)
The #23 recommended podcast for Search term 'biden' Dear Joe Biden (Dennis Trainor Jr)
The #24 recommended podcast for Search term 'biden' Blue for Biden: Politics for All (Students for Biden)
The #25 recommended podcast for Search term 'biden' What Biden Just Said About Crypto And Why You Need (Sidney Fritsch)
The #26 recommended podcast for Search term 'biden' HillMonkey - Biden SmackDown (Tom Boedi)
The #27 recommended podcast for Search term 'biden' Biden's new Covid vaccine push focuses on workers, students, doctor's offices to stifle delta varian (Duane Purdy)
The #28 recommended podcast for Search term 'biden' El pedido a Joe Biden (Fabiana Sánchez Di Natale)
The #29 recommended podcast for Search term 'biden' Wer ist Joe Biden? (Juleon & The American Stream)
The #30 recommended podcast for Search term 'biden' Joe Biden's Venmo account was discovered by reporters in 'less than 10 minutes' (Reyes Rolfson)
The #31 recommended podcast for Search term 'biden' Biden Regime (Grace Killian)
The #32 recommended podcast for Search term 'biden' Quem é Joe Biden (Sub com Ciência)
The #33 recommended podcast for Search term 'biden' Pramuka podcast biden powell (Arief wiranata)
The #34 recommended podcast for Search term 'biden' US election Day 2 wrap: Biden nears win (Earshot)

```
