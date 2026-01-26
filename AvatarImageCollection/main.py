import random
import time
from pathlib import Path

import httpx
import requests

# site home: https://www.pexels.com/zh-cn/search/users/Indian%20persiose/

name_list = [
    "ChaiChai", "SareeLove", "BindiBeauty", "BangleBelle", "MehendiMagic",
    "JhumkaJaisi", "NathNazar", "PayalKiChham", "AnkletAngel", "Mangalsutra",
    "SindoorSringar", "VermilionQueen", "KajalKali", "KohlEyes", "SmokeyEyes",
    "LipstickLover", "BlushBabe", "HighlighterQueen", "ContourGoddess", "SkincareEnthusiast",
    # 现代男生纯印度文昵称
    # 时尚现代
    "आधुनिकयुवा", "फ़ैशनेबल", "स्टाइलिश", "ट्रेंडी", "कूल",
    "हिपस्टर", "मॉडर्न", "यंग", "जेनजेड", "मिलेनियल",

    # 科技网络
    "टेकसेवी", "डिजिटलयोधा", "ऑनलाइनयोद्धा", "वेबसर्फ़र", "इंटरनेटयात्री",
    "साइबरयात्री", "वर्चुअलयोद्धा", "डाटावीर", "कोडसाधक", "प्रोग्रामवीर",
    "ऐपनिर्माता", "सॉफ़्टवेयरसाधु", "हैकरयोगी", "डेवलपरऋषि", "स्टार्टअपतपस्वी",

    # 游戏电竞
    "गेमरयोद्धा", "ईस्पोर्ट्सवीर", "पीयूबीजीयोद्धा", "बीजीएमआईमहारथी", "फ़्रीफ़ायरयोगी",
    "वैलोरैंटयोद्धा", "कंसोलयात्री", "मोबाइलगेमर", "गेमिंगप्रो", "एस्पोर्ट्सतारा",

    # 社交媒体
    "इंस्टाग्रामी", "व्हाट्सऐप्पी", "यूट्यूबर", "ट्विटरयात्री", "फ़ेसबुकी",
    "स्नैपचैटी", "टिकटॉकर", "लिंक्डइनी", "सोशलमीडियायोगी", "डिजिटलकथा",

    # 音乐艺术
    "म्यूज़िकप्रेमी", "गायकयोद्धा", "संगीतसाधक", "रैपरयोगी", "डीजेमहाराज",
    "बीटमेकर", "प्लेलिस्टकर्ता", "म्यूज़िकस्ट्रीमर", "कलाकारयात्री", "क्रिएटिवसाधु",

    # 体育健身
    "जिमयोद्धा", "फ़िटनेससाधक", "वर्कआउटयोगी", "बॉडीबिल्डर", "योगयोद्धा",
    "मेडिटेशनयात्री", "स्वास्थ्यसाधु", "खिलाड़ीयोद्धा", "क्रिकेटसाधक", "फ़ुटबॉलयोगी",

    # 旅行探险
    "यात्रासाधक", "ट्रैवलयोगी", "वंडरलस्टी", "एडवेंचरयोद्धा", "एक्सप्लोरर",
    "रोडट्रिपर", "बैकपैकर", "हाइकरयात्री", "माउंटेनियर", "ट्रेकर",

    # 美食烹饪
    "फ़ूडी", "खानाप्रेमी", "रसोइयायोद्धा", "शेफ़योगी", "पकवानसाधक",
    "स्ट्रीटफ़ूडयात्री", "रेस्तराँखोजी", "कुकिंगयोद्धा", "रेसिपीरचयिता", "गैस्ट्रोनोमी",

    # 电影娱乐
    "फ़िल्मप्रेमी", "सिनेमायात्री", "ओटीटीयोद्धा", "वेबसीरीज़प्रेमी", "स्ट्रीमिंगयोगी",
    "मूवीबफ़", "सीरीज़यात्री", "एंटरटेनमेंटसाधक", "बॉलीवुडयोद्धा", "सिनेमासाधु",

    # 时尚风格
    "फ़ैशनयोद्धा", "स्टाइलयोगी", "कपड़ेप्रेमी", "एक्सेसरीज़साधक", "ग्रूमिंगयात्री",
    "ब्यूटीयोद्धा", "लुकसाधक", "ट्रेंडसेटर", "फ़ैशनिस्टा", "स्टाइलिस्ट",

    # 幽默搞笑
    "मेमेयोद्धा", "ह्यूमरयोगी", "कॉमेडीयात्री", "जोकर", "फ़नमेकर",
    "लाफ़्टरसाधक", "एंटरटेनर", "फ़नयोद्धा", "हास्ययोगी", "मज़ाकिया",

    # 阅读学习
    "बुकवर्म", "रीडिंगयोद्धा", "पढ़ाकू", "ज्ञानयात्री", "लर्निंगसाधक",
    "एजुकेशनयोगी", "कोर्सेसप्रेमी", "ऑनलाइनलर्नर", "स्टडीयोद्धा", "नॉलेजसाधु",

    # 商业创业
    "बिज़नेसयोद्धा", "एंटरप्रेन्योर", "स्टार्टअपयोगी", "इन्वेस्टर", "शेयरमार्केटयात्री",
    "ट्रेडिंगसाधक", "बिज़नेसमाइंड", "इनोवेटर", "क्रिएटिवबिज़नेस", "व्यापारयोद्धा",

    # 汽车摩托
    "कारप्रेमी", "बाइकयोद्धा", "ऑटोमोबाइलयोगी", "राइडर", "स्पीडयात्री",
    "मोटरहेड", "ऑटोएन्थूसियास्ट", "व्हीकललवर", "ड्राइविंगसाधक", "रोडयोद्धा",

    # 摄影摄像
    "फ़ोटोग्राफ़र", "वीडियोग्राफ़र", "कैमरायोद्धा", "शूटिंगयोगी", "फ़ोटोसाधक",
    "वीडियोमेकर", "कंटेंटक्रिएटर", "विज़ुअलस्टोरीटेलर", "फ़ोटोग्राफ़ीयात्री", "कैमरामैन",

    # 神秘灵性
    "रहस्ययात्री", "स्पिरिचुअलयोद्धा", "ध्यानयोगी", "अध्यात्मसाधक", "योगीयोद्धा",
    "मेडिटेशनमास्टर", "स्पिरिचुअलिटी", "इनरपीस", "माइंडफ़ुलनेस", "सोलसर्चर",

    # 自然环保
    "नेचरलवर", "पर्यावरणयोद्धा", "ग्रीनयोगी", "इकोफ़्रेंडली", "सस्टेनेबल",
    "प्लांटलवर", "गार्डनिंगयात्री", "वृक्षप्रेमी", "पशुपक्षीप्रेमी", "प्रकृतिसाधक",

    # 夜间生活
    "नाइटलाइफ़र", "पार्टीयोद्धा", "क्लबिंगयोगी", "डांसफ़्लोरयात्री", "डीजेनाइट",
    "लाइट्सकैमेरा", "म्यूज़िकलाउड", "डांसमैनिया", "पार्टीएनिमल", "नाइटआउल",

    # 地区特色
    "दिल्लीवाला", "मुंबईकर", "बैंगलोरवासी", "चेन्नईयन", "हैदराबादी",
    "कोलकातावासी", "पुणेकर", "अहमदाबादी", "जयपुरी", "लखनऊवाला",
    "पंजाबी", "गुजराती", "मराठी", "बिहारी", "उत्तरप्रदेशी",
    "राजस्थानी", "मध्यप्रदेशी", "छत्तीसगढ़ी", "ओडिशा", "आंध्रवासी",
    "तेलंगाना", "तमिल", "केरलवासी", "कर्नाटक", "गोवन",
    "असमिया", "पूर्वोत्तर", "काश्मीरी", "हिमाचली", "उत्तराखंडी",
    # 男生昵称 (200个)
    "DesiKing", "SherSingh", "BetaJi", "PunjabDaSher", "DilliKaLaunda",
    "Rajputana", "Mumbaikar", "Bangalorean", "ChennaiBoy", "Hyderabadi",
    "DesiRockstar", "BollywoodFan", "CricketLover", "ChaiAddict", "BiryaniKing",
    "GymBro", "TechNerd", "StartupGuy", "CodeWarrior", "GamerBoy",
    "BikeRider", "CarEnthusiast", "TravelBuddy", "Wanderlust", "MountainMan",
    "Yogi", "Meditator", "SpiritualSoul", "KarmaYogi", "DharmaSeeker",
    "ChhoraGangaKinareWala", "GharKaChhora", "MaaKaLaal", "PapaKiPride", "Bhaiyaji",
    "ChhoteSarkar", "Badshah", "Sultan", "Nawab", "RajaBeta",
    "SinghIsKing", "RajputPride", "ThakurSahab", "JatBoy", "Gurjar",
    "MarathaWarrior", "SikhBrother", "MalayaliMacha", "TamilAnnan", "TeluguAbbayi",
    "KannadaGuru", "GujaratiBhai", "MarwariBusiness", "BihariBabua", "UPwala",
    "RajasthaniRaja", "PahadiBoy", "KashmiriPandit", "BengaliBabu", "OriyaBhai",
    "AssameseLad", "GoanSusegad", "NortheastStar", "IndianGuy", "DesiLadka",

    # 更多男生昵称
    "DesiDynamo", "BharatPutra", "Hindustani", "Swadeshi", "Virasat",
    "Parampara", "Sanskar", "Sanskriti", "Kalaakar", "KalaSagar",
    "Geetkaar", "Shayar", "KavitaPremi", "SangeetRasik", "NatyaShilpi",
    "Rangmanch", "PardeKaFankaar", "CameraShy", "SelfieKing", "Instagrammer",
    "YouTuber", "Influencer", "ContentCreator", "DigitalNomad", "RemoteWorker",
    "CorporateWarrior", "OfficeKaHero", "9to5Survivor", "WeekendWarrior", "MondayBlues",
    "ChaiSutta", "CafeHunter", "Foodie", "StreetFoodLover", "DhabaKing",
    "MomosAddict", "SamosaLover", "GolgappaFan", "ChaatKing", "MithaiDukaan",

    # 现代昵称
    "TechieSingh", "CodePunjabi", "DevDesi", "AIEnthusiast", "BlockchainBuddy",
    "CryptoKing", "BitcoinBhai", "NFTCollector", "MetaverseExplorer", "VRAdventurer",
    "GamingPro", "EsportsPlayer", "ConsoleGamer", "MobileGamer", "PUBGPlayer",
    "FreeFireStar", "BGMIExpert", "ValorantPro", "CSGOFan", "FIFAChampion",
    "FantasyLeague", "IPLSupporter", "TeamIndia", "CricketCaptain", "StadiumRoarer",
    "BlueBrigade", "MenInBlue", "IndianArmyFan", "Patriotic", "JaiHind",
    "VandeMataram", "BharatMataKiJai", "Nationalist", "DeshBhakt", "CountryFirst",

    # 传统昵称
    "Dhanyavad", "Kripa", "Ashirwad", "Aashirwad", "Prarthana",
    "Sankalp", "Vachan", "Pratigya", "Kasam", "Saugandh",
    "Imaan", "Vishwas", "Bharosa", "Aitbaar", "Yakeen",
    "Sachai", "Satya", "SatyamevJayate", "Dharma", "Karma",
    "Moksha", "Nirvana", "Shanti", "Ananda", "Sukha",
    "Dukh", "Dard", "Pyar", "Mohabbat", "Ishq",
    "Dil", "Jaan", "Ruh", "Atma", "Chehra",

    # 女生昵称 (300个)
    "DesiQueen", "Punjaban", "Rajkumari", "RaniSahab", "Begum",
    "MumbaiKiRani", "DelhiKiDulhan", "BangaloreBeauty", "ChennaiChelvi", "HyderabadiHaseena",
    "GujaratiGori", "MarathiMulgi", "BengaliBhadramahila", "TamilPonnu", "TeluguAmayi",
    "KannadaHudugi", "MalayaliKutty", "OdiaBou", "AssameseJui", "KashmiriKomal",
    "DesiGirl", "IndianBeauty", "BharatiyaNari", "HindustaniLadki", "SwadeshiSundari",
    "Sanskari", "SanskritiKiRakhwala", "ParamparaKiDharohar", "VirasatKiVaris", "Khandani",
    "GharKiLakshmi", "MaaBeti", "Didi", "BhabhiJi", "ChhotiSi",
    "NanhiKali", "ChandSi", "Sitaara", "Chaand", "SurajMukhi",

    # 现代女生昵称
    "BollywoodDiva", "ScreenQueen", "DramaQueen", "Fashionista", "StyleIcon",
    "MakeupMaven", "BeautyInfluencer", "LifestyleBlogger", "TravelInfluencer", "FoodBlogger",
    "YogaInstructor", "FitnessFreak", "GymAddict", "ZumbaQueen", "MeditationGuru",
    "SpiritualGuide", "WellnessCoach", "MentalHealthAdvocate", "SelfCareQueen", "MindfulBeing",
    "WorkingWoman", "CareerGirl", "CorporateQueen", "Entrepreneur", "StartupFounder",
    "BossLady", "GirlBoss", "SheEO", "BusinessWoman", "Professional",

    # 创意昵称
    "ChaiChai", "SareeLove", "BindiBeauty", "BangleBelle", "MehendiMagic",
    "JhumkaJaisi", "NathNazar", "PayalKiChham", "AnkletAngel", "Mangalsutra",
    "SindoorSringar", "VermilionQueen", "KajalKali", "KohlEyes", "SmokeyEyes",
    "LipstickLover", "BlushBabe", "HighlighterQueen", "ContourGoddess", "SkincareEnthusiast",

    # 食物相关
    "SamosaLover", "ChaatQueen", "GolgappaAddict", "PaniPuriPriya", "DahiBhalle",
    "BhelPuri", "SevPuri", "RagdaPattice", "VadaPav", "PavBhaji",
    "CholeBhature", "RajmaChawal", "DalMakhani", "ButterChicken", "BiryaniQueen",
    "HyderabadiBiryani", "LucknowiBiryani", "KolkataBiryani", "MalabarBiryani", "DumBiryani",
    "MithaiDil", "GulabJamun", "Rasgulla", "Rasmalai", "KajuKatli",
    "Barfi", "Ladoo", "Jalebi", "Imarti", "Peda",

    # 艺术文化
    "ClassicalDancer", "Bharatanatyam", "KathakQueen", "OdissiDiva", "Kuchipudi",
    "Mohiniyattam", "Manipuri", "Sattriya", "Kathakali", "Theyyam",
    "FolkDancer", "BhangraQueen", "GarbaRani", "Lavani", "Bihu",
    "Ghoomar", "Chhau", "Rouf", "DandiyaQueen", "Giddha",
    "MusicLover", "ClassicalSinger", "GhazalQueen", "BhajanSinger", "SufiSoul",
    "QawwaliFan", "FilmiGeet", "BollywoodMusic", "IndieMusic", "FusionArtist",

    # 自然元素
    "Chandni", "Sitaara", "Suraj", "Chaand", "Taara",
    "Badal", "Barish", "Pani", "Jal", "Nadi",
    "Samundra", "Sagar", "Pahar", "Parvat", "Giri",
    "Van", "Jungle", "Ped", "Phool", "Pushp",
    "Gulab", "Kamal", "Champa", "Mogra", "Rajnigandha",
    "Bel", "Tulsi", "Neem", "Peepal", "Bargad",

    # 情感状态
    "SinglePringle", "ForeverAlone", "LoveSeeker", "RelationshipGoals", "Committed",
    "Engaged", "Married", "NewlyWed", "HappilyMarried", "Divorced",
    "SingleMom", "WorkingMom", "HomeMaker", "HouseWife", "HomeManager",
    "FamilyFirst", "KidsFirst", "PetParent", "DogMom", "CatLady",
    "PlantParent", "Gardener", "HomeChef", "KitchenQueen", "RecipeCreator",

    # 地区特色
    "KashmirKiKali", "Himachali", "Uttarakhandi", "PahadiRani", "MountainGirl",
    "ValleyQueen", "DesertRose", "TharKiRani", "SandDune", "Oasis",
    "BeachBabe", "GoanBeauty", "KeralaQueen", "Backwaters", "Houseboat",
    "HillStation", "Shimla", "Manali", "Darjeeling", "Ooty",
    "Munnar", "Coorg", "Ladakh", "Leh", "Spiti",

    # 宗教精神
    "Bhakt", "Devotee", "Spiritualist", "Yogini", "Meditator",
    "TempleGoer", "Mandir", "Gurudwara", "Church", "Mosque",
    "ReligionPeace", "Interfaith", "Secular", "AllReligion", "OmShanti",
    "HarHarMahadev", "JaiShriRam", "Waheguru", "AllahHuAkbar", "JesusLoves",
    "BuddhamSharanam", "Mahavira", "GuruNanak", "Kabir", "Mirabai",

    # 动物相关
    "SherNi", "Baghin", "Hathi", "Gajagamini", "Hastini",
    "Ghoda", "Ashwa", "Ucchaisravas", "Cheetal", "Barasingha",
    "Neelgai", "Blackbuck", "Chinkara", "Langur", "Bandar",
    "Vanar", "Hanuman", "Garuda", "Mayur", "Mor",
    "Peacock", "NationalBird", "Koel", "Cuckoo", "Papiha",
    "Bulbul", "Nightangle", "Maina", "Parrot", "Tota",
    "Kabutar", "Pigeon", "Hans", "Swan", "RajHans",

    # 节日喜庆
    "DiwaliQueen", "Deepawali", "Diya", "MaaLakshmi", "GaneshChaturthi",
    "GanpatiBappa", "Navratri", "DurgaMaa", "MaaDurga", "MaaSaraswati",
    "HoliHai", "RangBarse", "Gulal", "Colors", "Phagwah",
    "EidMubarak", "Ramzan", "Roza", "Iftar", "Sehri",
    "Christmas", "Santa", "NewYear", "NavVarsh", "Ugadi",
    "GudiPadwa", "Pongal", "Baisakhi", "Onam", "Rakhi",

    # 文学艺术
    "Kavita", "Shayari", "Gazal", "Nazm", "Dohe",
    "Chaupai", "Shlok", "Mantra", "Stotra", "Bhajan",
    "Geet", "Song", "Music", "Sangeet", "Raag",
    "Taal", "Lay", "Sur", "Naad", "Shruti",
    "Vadan", "Instrumental", "Sitar", "Tabla", "Harmonium",
    "Flute", "Bansuri", "Shehnai", "Sarangi", "Santoor",

    # 社交媒体风格
    "InstaQueen", "SnapchatAddict", "FacebookFan", "Twitterati", "LinkedInPro",
    "WhatsAppForward", "MemeQueen", "ReelStar", "TikToker", "YouTubeCreator",
    "Podcaster", "AudioCreator", "VoiceArtist", "Anchor", "Host",
    "Moderator", "CommunityManager", "GroupAdmin", "PageAdmin", "Influencer",

    # 简洁现代
    "Desi.Girl", "Indian.Babe", "Bharat.Ki.Beti", "Hindustani.Soul", "Swadeshi.Spirit",
    "Made.In.India", "ProductOfIndia", "IndianByHeart", "GlobalIndian", "NRI",
    "ABCD", "AmericanBornConfusedDesi", "BritishIndian", "CanadianDesi", "AustralianIndian",
    "GulfNRi", "DubaiDiaries", "SingaporeSindhi", "MalaysianIndian", "FijiIndian",

    # 数字组合
    "DesiGirl_99", "IndianQueen_007", "BharatKiBeti_2024", "Swadeshi_1947", "Independence_15Aug",
    "Republic_26Jan", "GandhiJayanti_2Oct", "TeachersDay_5Sep", "ChildrensDay_14Nov", "YouthIcon_12Jan",
    "Kohli_18", "Dhoni_7", "Sachin_10", "Dravid_19", "Ganguly_99",
    "Sehwag_44", "Yuvraj_12", "Zaheer_34", "Bumrah_93", "Shami_11",
    "Rohit_45", "Rahul_1", "Pant_17", "Ashwin_99", "Jadeja_8",

    # 最后一批
    "JaiHind", "VandeMataram", "BharatMataKiJai", "IndiaFirst", "PatrioticIndian",
    "NationalPride", "CulturalHeritage", "UnityInDiversity", "IncredibleIndia", "AtithiDevoBhava",
    "SatyamevJayate", "DharmaChakra", "AshokaStambh", "Tiranga", "NationalFlag",
    "NationalAnthem", "JanaGanaMana", "SareJahanSeAchha", "MeraBharatMahan", "ProudIndian",
    # 时尚美丽
    "सुंदरी", "ख़ूबसूरत", "हसीन", "प्यारी", "मनमोहक",
    "आकर्षक", "मोहिनी", "चंचल", "मुस्कान", "चेहरा",
    "आँखें", "बाल", "होंठ", "मुस्कुराहट", "अदा",
    "अंग", "भव्य", "तेजस्वी", "कांतिमय", "प्रभावशाली",

    # 科技数字
    "टेकडिवा", "डिजिटलदेवी", "ऑनलाइनरानी", "वेबसर्फ़रगर्ल", "इंटरनेटयात्रा",
    "साइबरयोद्धा", "वर्चुअलदेवी", "डाटागर्ल", "कोडसाधिका", "प्रोग्रामवीरा",
    "ऐपनिर्मात्री", "सॉफ़्टवेयरसाध्वी", "हैकरयोगिनी", "डेवलपरऋषिका", "स्टार्टअपतपस्विनी",

    # 社交媒体
    "इंस्टाग्रामरानी", "व्हाट्सऐप्पीगर्ल", "यूट्यूबरानी", "ट्विटरयात्रा", "फ़ेसबुकीबेबे",
    "स्नैपचैटडॉल", "टिकटॉकरानी", "लिंक्डइनप्रो", "सोशलमीडियायोगिनी", "डिजिटलकथाकारा",

    # 音乐舞蹈
    "गायिका", "नृत्यांगना", "संगीतप्रेमी", "रैपरयोगिनी", "डीजेरानी",
    "बीटमेकरगर्ल", "प्लेलिस्टकर्त्री", "म्यूज़िकस्ट्रीमर", "कलाकारयात्रा", "क्रिएटिवसाध्वी",
    "शास्त्रीयनृत्यांगना", "भरतनाट्यम", "कथक", "ओडिसी", "कुचिपुड़ी",
    "मोहिनीअट्टम", "मणिपुरी", "सत्त्रिया", "गरबा", "भांगड़ा",

    # 健身健康
    "योगिनी", "फ़िटनेसदेवी", "जिमरानी", "वर्कआउटयोगिनी", "बॉडीफ़िट",
    "मेडिटेशनमास्टर", "स्वास्थ्यसाध्वी", "वेलनेसगर्ल", "माइंडफ़ुलनेस", "सेल्फ़केयर",
    "आहारविशेषज्ञ", "न्यूट्रिशनिस्ट", "हेल्थकोच", "फ़िटनेसट्रेनर", "योगप्रशिक्षिका",

    # 旅行探险
    "यात्रिका", "ट्रैवलरानी", "वंडरलस्टगर्ल", "एडवेंचरयोद्धा", "एक्सप्लोरर",
    "रोडट्रिपर", "बैकपैकरगर्ल", "हाइकरयात्रा", "माउंटेनियर", "ट्रेकर",
    "बीचगर्ल", "हिलस्टेशन", "कैंपर", "वन्यजीवप्रेमी", "प्रकृतिप्रेमी",

    # 美食烹饪
    "पाककला", "रसोइया", "शेफ़", "पकवानसाधिका", "खानाप्रेमी",
    "स्ट्रीटफ़ूडयात्रा", "रेस्तराँखोजी", "कुकिंगयोगिनी", "रेसिपीरचयित्री", "गैस्ट्रोनोमी",
    "मिठाइयाँ", "नमकीन", "चटपटा", "मसालेदार", "स्वादिष्ट",

    # 影视娱乐
    "फ़िल्मप्रेमी", "सिनेमायात्रा", "ओटीटीयोद्धा", "वेबसीरीज़प्रेमी", "स्ट्रीमिंगयोगिनी",
    "मूवीबफ़", "सीरीज़यात्रा", "एंटरटेनमेंटसाध्वी", "बॉलीवुडफ़ैन", "सिनेमासाधिका",
    "ड्रामाक्वीन", "रोमांसप्रेमी", "एक्शनलवर", "कॉमेडीफ़ैन", "थ्रिलरलवर",

    # 时尚美妆
    "फ़ैशनिस्टा", "स्टाइलिश", "ट्रेंडी", "ग्लैमरस", "शानदार",
    "कपड़ेप्रेमी", "ज्वैलरीलवर", "ब्यूटीगुरु", "मेकअपआर्टिस्ट", "हेयरस्टाइलिस्ट",
    "स्किनकेयर", "ब्यूटीरूटीन", "मेकअपकलेक्शन", "फ़ैशनब्लॉगर", "लाइफ़स्टाइल",

    # 幽默娱乐
    "मेमेक्वीन", "ह्यूमरयोगिनी", "कॉमेडीयात्रा", "जोकर", "फ़नमेकर",
    "लाफ़्टरसाध्वी", "एंटरटेनर", "फ़नयोद्धा", "हास्ययोगिनी", "मज़ाकिया",

    # 阅读学习
    "किताबप्रेमी", "रीडिंगयोद्धा", "पढ़ाकू", "ज्ञानयात्रा", "लर्निंगसाधिका",
    "एजुकेशनयोगिनी", "कोर्सेसप्रेमी", "ऑनलाइनलर्नर", "स्टडीयोद्धा", "नॉलेजसाध्वी",
    "बुकवर्म", "लाइब्रेरीलवर", "बुकस्टोर", "रेडिंगचैलेंज", "बुकक्लब",

    # 商业创业
    "बिज़नेसवुमन", "एंटरप्रेन्योर", "स्टार्टअपयोगिनी", "इन्वेस्टर", "शेयरमार्केटयात्रा",
    "ट्रेडिंगसाधिका", "बिज़नेसमाइंड", "इनोवेटर", "क्रिएटिवबिज़नेस", "व्यापारयोद्धा",
    "बॉसलैडी", "लीडर", "मैनेजर", "एग्ज़ीक्यूटिव", "प्रोफ़ेशनल",

    # 艺术创作
    "चित्रकार", "वास्तुकार", "डिज़ाइनर", "क्राफ़्टर", "हस्तकला",
    "पेंटर", "स्केचआर्टिस्ट", "डिजिटलआर्ट", "क्रिएटिव", "आर्टिस्ट",
    "फ़ोटोग्राफ़र", "वीडियोग्राफ़र", "कंटेंटक्रिएटर", "राइटर", "ब्लॉगर",

    # 灵性修养
    "ध्यानिनी", "योगिनी", "साध्वी", "तपस्विनी", "आध्यात्मिक",
    "मननशील", "चिंतनशील", "विचारशील", "भक्त", "उपासक",
    "प्रार्थना", "साधना", "अभ्यास", "अनुशासन", "संयम",

    # 自然环保
    "प्रकृतिप्रेमी", "पर्यावरणयोद्धा", "ग्रीनयोगिनी", "इकोफ़्रेंडली", "सस्टेनेबल",
    "पौधेप्रेमी", "बगीचाकर्मी", "वृक्षरोपक", "पशुपक्षीप्रेमी", "जैविक",
    "कम्पोस्ट", "रिसाइक्लिंग", "वेस्टमैनेजमेंट", "क्लीनली", "ग्रीनलिविंग",

    # 夜生活娱乐
]

import requests
import httpx
import time
import random
from pathlib import Path

# 初始化
count = 0
page = 30
avatars_dir = Path.cwd() / "avatars"
avatars_dir.mkdir(exist_ok=True)

# 公共headers（可以提取出来复用）
common_headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'referer': 'https://www.pexels.com/zh-cn/search/users/Indian/',
}

while count < 1000:
    # API请求
    api_url = f"https://www.pexels.com/zh-cn/api/v3/search/users?query=Indian&page={page}&per_page=12"

    # 添加更多headers到API请求
    api_headers = common_headers.copy()
    api_headers.update({
        'content-type': 'application/json',
        'secret-key': 'H2jk9uKnhRmL6WPwh89zBezWvr',
        'x-client-type': 'react',
    })

    response = requests.get(api_url, headers=api_headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    users = data['data']
    print(f"本页找到 {len(users)} 个用户")

    for i, user in enumerate(users):
        print(f"处理第 {i + 1} 个用户...")

        # 获取头像URL
        attributes = user.get('attributes', {})
        img_url = attributes.get('avatar', {}).get('medium')

        if not img_url:
            print("未找到头像URL")
            continue

        print(f"头像URL: {img_url}")

        # 休眠避免请求过快
        time.sleep(2)  # 稍微减少休眠时间

        # 下载图片
        try:
            img_response = httpx.get(img_url, headers=common_headers, timeout=30)
            img_response.raise_for_status()
        except Exception as e:
            continue

        # 生成唯一文件名
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        base_name = random.choice(name_list)
        img_name = f"{base_name}_{timestamp}_{random_suffix}"

        file_path = avatars_dir / f'{img_name}.jpg'

        print(f"开始下载: {img_name}.jpg")

        # 保存图片
        with open(file_path, 'wb') as f:
            f.write(img_response.content)

        # 验证文件大小
        file_size = file_path.stat().st_size
        if file_size < 1024:  # 小于1KB的文件可能是无效的
            print(f"警告: 文件太小 ({file_size} 字节)，可能无效，删除")
            file_path.unlink()
            continue

        count += 1
        print(f"✓ 成功下载第 {count} 张图片: {img_name}.jpg")

    page += 1

# print(f"下载完成！总共下载了 {count} 张图片")
# print(f"图片保存在: {avatars_dir.absolute()}")
