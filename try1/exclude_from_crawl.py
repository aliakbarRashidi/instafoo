user_names = [
'jack',
'kevin',
'mikeyk',
'instagram',
'arianagrande',
'therock',
'justinbieber',
'kendalljenner',
'nike',
'victoriassecret',
'kevinhart4real',
'theellenshow',
'champagnepapi',
'kingjames',
'zacefron',
'ladygaga',
'nba',
'danbilzerian',
'thenotoriousmma',
'natgeotravel',
'leonardodicaprio',
'snoopdogg',
'floydmayweather',
'wizkhalifa',
'sommerray',
'buzzfeedtasty',
'starbucks',
'loganpaul',
'sabrinacarpenter',
'pewdiepie',
'gopro',
'schwarzenegger',
'fuckjerry',
'willsmith',
'lamborghini',
'gianlucavacchi',
'timed.perfection',
'rondarousey',
'djkhaled',
'kevindurant',
'mtv',
'markwahlberg',
'houseofhighlights',
'bestofhorror',
'societyfeelings',
'videosposts',
'debbyryan',
'humansofny',
'elonmusk',
'alexandradaddario',
'nick__bateman',
'tyleroakley',
'coltonlhaynes',
'ygtrece',
'marianodivaio',
'betches',
'steveaoki',
'liverpoolfc',
'amazingvideo.s',
'vines',
'g_eazy',
'tattoos_of_instagram',
'viralvideosmediabackup',
'daily_wtf_facts',
'couplegoals',
'logic',
'lol_vines',
'robdyrdek',
'youtubewtf',
'gq',
'barstoolsports',
'bored',
'macideshanebookout',
'stancenation',
'buzzfeed',
'gazgshore',
'nochilllcomedy',
'tonimahfud',
'okcthunder',
'sophiaesperanza',
'basketballvideos',
'joerogan',
'jjwatt',
'garyvee',
'caseyneistat',
'chanelwestcoast',
'tailopez',
'brockohurn',
'wsl',
'scottgshore',
'muhammadali',
'drpimplepopper',
'liamferrari',
'calumvonmoger',
'archdigest',
'michaelblackson',
'azizansari',
'nicolette_shea',
'bossgirlscertified',
'kylierae',
'drunkpeopledoingthings',
'richardbranson',
'tavicastro',
'williamsfalade',
'nicole',
'josh']

user_ids = [52797702]

'''
select concat("'",user_name,"',") 
-- select user_name, bio
from users where user_name not in ('sommerray2',
'instagrambodybuilding',
'sergiconstance',
'sandraprikker',
'jeff_seid',
'mariotestino',
'kaigreene',
'laurendrainfit',
'rosannaarkle',
'simeonpanda',
'paigehathaway',
'katyaelisehenry',
'viki_odintcova',
'ulissesworld',
'svetabily',
'tammyhembrow',
'kayla_itsines',
'anllela_sagra',
'thinkgrowprosper',
'fefrancooficial',
'genesislopezfitness',
'jessicaarevalo_',
'millionaire_mentor',
'bradleymartyn',
'philheath',
'bodybuildingcom',
'jaycutler',
'michelle_lewin') order by follower_count desc limit 100 \G

'''