#!/usr/bin/python3
from model.cluster import Creator, Cluster, Clusters
from model.project import Project, Projects

CLUSTERS  = Clusters([
    Cluster(
        'cluster_test',
        'for_testing',
        [ 
            Creator('turk'),
        ]
    ),
    Cluster(
        'asians',
        'subreddit r/twitchasians',
        [ 
            Creator('ahra'),
            Creator('ariasaki'),
            Creator('berry0314'),
            Creator('canahry'),
            Creator('hyoon'),
            Creator('kiaraakitty'),
            Creator('leesherwhy'),
            Creator('meowko'),
            Creator('mvngokitty'),
            Creator('sooflower'),
            Creator('sorammmm'),
            Creator('strawberrybunni'),
            Creator('supcaitlin'),
            Creator('viptoriaaa'),
            Creator('woohankyung'),
            Creator('yeonari'),
            Creator('yuggie_tv'),
        ]
    ),
        Cluster(
        'orange',
        'NA Orange League atlas 2022-01',
        [ 
            Creator('aphromoo'),
            Creator('bjergsenlol'),
            Creator('bobginxd'),
            Creator('broxah'),
            Creator('caedrel'),
            Creator('caps'),
            Creator('doublelift'),
            Creator('dzukill'),
            Creator('gosu'),
            Creator('imaqtpie'),
            Creator('imls'),
            Creator('iwilldominate'),
            Creator('jankos'),
            Creator('lol_nemesis'),
            Creator('loltyler1'),
            Creator('midbeast'),
            Creator('nightblue'),
            Creator('pobelter'),
            Creator('quantum'),
            Creator('ratirl'),
            Creator('sanchovies'),
            Creator('sirhcez'),
            Creator('sneakylol'),
            Creator('solarbacca'),
            Creator('solorenektononly'),
            Creator('tarzaned'),
            Creator('tfblade'),
            Creator('thebausffs'),
            Creator('tobiasfate'),
            Creator('trick2g'),
        ]
    ),
        Cluster(
        'vtubers',
        'vtoobers',
        [ 
            Creator('anny'),
            Creator('apricot'),
            Creator('baoo'),
            Creator('chibidoki'),
            Creator('elly_vt'),
            Creator('filian'),
            Creator('harukakaribu'),
            Creator('ironmouse'),
            Creator('laynalazar'),
            Creator('misu'),
            Creator('momo'),
            Creator('nihmune'),
            Creator('nyanners'),
            Creator('projektmelody'),
            Creator('remuchii'),
            Creator('saruei'),
            Creator('shylily'),
            Creator('silvervale'),
            Creator('snuffy'),
            Creator('foxplushy'),
            Creator('thean1meman'),
            Creator('trashtastepodcast'),
            Creator('veibae'),
            Creator('yuzu'),
            Creator('zentreya'),
        ]
    ),
    Cluster(
        'camgirls',
        'NA sfw camgirls - DarkGreen Atlas + hottub streamers',
        [ 
            Creator('adrianachechik_'),
            Creator('alinity'),
            Creator('amouranth'),
            Creator('evaanna'),
            Creator('faith'),
            Creator('gogogirl_tv'),
            Creator('ibabyrainbow'),
            Creator('kandyland'),
            Creator('kiaraakitty'),
            Creator('kyootbot'),
            Creator('leynainu'),
            Creator('littlelianna'),
            Creator('melina'),
            Creator('miamalkova'),
            Creator('missmercyy'),
            Creator('spoopykitt'),
            Creator('taylor_jevaux'),
        ]
    ),
    Cluster(
        'napopularpinkone',
        'popular NA streamers pink atlas #1',
        [ 
            Creator('alinity'),
            Creator('atrioc'),
            Creator('aurateur'),
            Creator('austinshow'),
            Creator('barbarousking'),
            Creator('bawkbasoup'),
            Creator('botezlive'),
            Creator('calebhart42'),
            Creator('codemiko'),
            Creator('connoreatspants'),
            Creator('cyr'),
            Creator('dashducks'),
            Creator('destiny'),
            Creator('distortion2'),
            Creator('emmiru'),
            Creator('esfandtv'),
            Creator('grandpoobear'),
            Creator('hachubby'),
            Creator('hasanabi'),
            Creator('jerma985'),
            Creator('jinnytty'),
            Creator('jschlatt'),
            Creator('justaminx'),
            Creator('maya'),
            Creator('mizkif'),
            Creator('moistcr1tikal'),
            Creator('nesua'),
            Creator('paymoneywubby'),
            Creator('qtcinderella'),
            Creator('sodapoppin'),
            Creator('surefour'),
            Creator('susu_jpg'),
            Creator('the_happy_hob'),
            Creator('theneedledrop'),
            Creator('vargskelethor'),
            Creator('vinesauce'),
            Creator('willneff'),
            Creator('zoil'),
        ],
    ),
    Cluster(
        'napopularpinktwo',
        'popular NA streamers pink atlas #2',
        [ 
            Creator('moonmoon'),
            Creator('maximilian_dood'),
            Creator('dansgaming'),
            Creator('forsen'),
            Creator('swolejoels'),
            Creator('roflgator'),
            Creator('giantwaffle'),
            Creator('itsmejp'),
            Creator('ezekiel_iii'),
            Creator('cohhcarnage'),
            Creator('burkeblack'),
            Creator('pokelawls'),
            Creator('myth'),
            Creator('nmplol'),
            Creator('erobb221'),
            Creator('mizkif'),
            Creator('lirik'),
            Creator('admiralbahroo'),
            Creator('pointcrow'),
            Creator('smallant'),
            Creator('elajjaz'),
            Creator('fextralife'),
        ]
    ),
])

PROJECTS = Projects([
    Project(
        name='thequarry_30d',
        description='Popular The Quarry twitch clips!',
        title='The Quarry',
        game_ids=['1937599489'],
        days=30,
        n_per_month=2,
        is_active=False,
    ),
    Project(
        name='csgo_30d',
        description='Popular Counter-Strike Global Offensive twitch clips past 30 days!',
        title='CSGO',
        game_ids=['32399'],
        days=30,
        n_per_month=1,
    ),
    Project(
        name='fortnite_30d',
        description='Popular Fortnite twitch clips past 30 days!',
        title='Fortnite',
        game_ids=['33214'],
        days=30,
        n_per_month=1,
    ),
    Project(
        name='gta5_30d',
        description='Popular Grand Theft Auto V twitch clips past 30 days!',
        title='GTA V',
        game_ids=['32982'],
        days=30,
        n_per_month=1,
    ),
    Project(
        name='league_30d',
        description='Popular League of Legends twitch clips past 30 days!',
        title='League of Legends',
        game_ids=['21779'],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='league_7d',
        title='League of Legends',
        description='popular league of legends clips past 7 days',
        game_ids=['21779'],
        days=7,
        n_per_month=4,
    ),
    Project(
        name='valorant_14d',
        title='Valorant',
        description='valorant clips',
        game_ids=['516575'],
        days=14,
        n_per_month=2,
    ),
    Project(
        name='valorant_30d',
        title='Valorant',
        description='valorant clips',
        game_ids=['516575'],
        days=30,
        n_per_month=1,
    ),
    Project(
        name='pools_30d',
        title='Pools, Hot Tubs and Beaches',
        description='Pools, Hot Tubs and Beaches',
        game_ids=['116747788'],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='asmr_30d',
        title='ASMR',
        description='Popular Twitch ASMR clips',
        categories=['ASMR'],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='asmr_short',
        title='ASMR',
        description='Popular Twitch ASMR clips',
        categories=['ASMR'],
        days=10,
        n_per_month=3,
        single=True,
    ),
    Project(
        name='just_chatting_30d',
        title='Just Chatting',
        description='Popular Twitch Just Chatting clips',
        game_ids=['509658'],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='just_chatting_7d',
        title='Just Chatting',
        description='Popular Twitch Just Chatting clips',
        game_ids=['509658'],
        days=7,
        n_per_month=3,
    ),
    Project(
        name='pools_short',
        title='Pools, Hot Tubs and Beaches',
        description='Pools, Hot Tubs and Beaches',
        game_ids=['116747788'],
        clusters=[
            CLUSTERS.by_name('camgirls'),
            CLUSTERS.by_name('asians'),
        ],
        days=7,
        duration=180,
        n_per_month=4,
    ),
    Project(
        name='vtubers_7d',
        title='VTubers',
        description='popular vtuber clips past 7 days',
        clusters=[CLUSTERS.by_name('vtubers')],
        days=7,
        n_per_month=4,
    ),
    Project(
        name='vtubers_30d',
        title='VTubers',
        description='popular vtuber clips',
        clusters=[CLUSTERS.by_name('vtubers')],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='vtubers_short',
        title='VTuber',
        description='Popular Twitch VTuber clip',
        clusters=[CLUSTERS.by_name('vtubers')],
        days=7,
        n_per_month=4,
        single=True,
    ),
    Project(
        name='asians_30d',
        title='AZN',
        description='popular clips form r/twitchasians',
        clusters=[CLUSTERS.by_name('asians')],
        days=30,
        n_per_month=1,
    ),
    Project(
        name='orange_30d',
        title='NA Orange',
        description='NA Orange league',
        clusters=[CLUSTERS.by_name('orange')],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='camgirls_30d',
        title='UHH',
        description='popular twitch clips',
        clusters=[CLUSTERS.by_name('camgirls')],
        days=30,
        n_per_month=2,
    ),
    Project(
        name='napopular_30d',
        title='NA',
        description='NA popular',
        clusters=[CLUSTERS.by_name('napopularpinkone'), CLUSTERS.by_name('napopularpinktwo')],
        days=30,
        n_per_month=4,
    ),
])