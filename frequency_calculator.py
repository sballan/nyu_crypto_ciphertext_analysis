from collections import Counter

message_1 = "underwaists wayfarings fluty analgia refuels transcribing nibbled okra buttonholer venalness hamlet " \
            "praus apprisers presifted cubital walloper dissembler bunting wizardries squirrel preselect befitted " \
            "licensee encumbrances proliferations tinkerer egrets recourse churl kolinskies ionospheric docents " \
            "unnatural scuffler muches petulant acorns subconscious xyster tunelessly boners slag amazement " \
            "intercapillary manse unsay embezzle stuccoer dissembles batwing valediction iceboxes ketchups phonily con "
message_2 = "rhomb subrents brasiers render avg tote lesbian dibbers jeopardy struggling urogram furrowed hydrargyrum " \
            "advertizing cheroots goons congratulation assaulters ictuses indurates wingovers relishes briskly " \
            "livelihoods inflatable serialized lockboxes cowers holster conciliating parentage yowing restores " \
            "conformities marted barrettes graphically overdevelop sublimely chokey chinches abstracts rights " \
            "hockshops bourgeoisie coalition translucent fiascoes panzer mucus capacitated stereotyper omahas produ "
message_3 = "yorkers peccaries agenda beshrews outboxing biding herons liturgies nonconciliatory elliptical " \
            "confidants concealable teacups chairmanning proems ecclesiastically shafting nonpossessively doughboy " \
            "inclusion linden zebroid parabolic misadventures fanciers grovelers requiters catmints hyped necklace " \
            "rootstock rigorously indissolubility universally burrowers underproduced disillusionment wrestling " \
            "yellowbellied sherpa unburnt jewelry grange dicker overheats daphnia arteriosclerotic landsat jongleur "
message_4 = "cygnets chatterers pauline passive expounders cordwains caravel antidisestablishmentarianism syllabubs " \
            "purled hangdogs clonic murmurers admirable subdialects lockjaws unpatentable jagging negotiated " \
            "impersonates mammons chumminess semi pinner comprised managership conus turned netherlands temporariness " \
            "languishers aerate sadists chemistry migraine froggiest sounding rapidly shelving maligning shriek " \
            "faeries misogynist clarities oversight doylies remodeler tauruses prostrated frugging comestible "
message_5 = "ovulatory geriatric hijack nonintoxicants prophylactic nonprotective skyhook warehouser paganized " \
            "brigading european sassier antipasti tallyho warmer portables selling scheming amirate flanker " \
            "photosensitizer multistage utile paralyzes indexer backrests tarmac doles siphoned casavas mudslinging " \
            "nonverbal weevil arbitral painted vespertine plexiglass tanker seaworthiness uninterested anathematizing " \
            "conduces terbiums wheelbarrow kabalas stagnation briskets counterclockwise hearthsides spuriously s "


def frequency_calculator(message):
    print("Letter Frequency for message is : ")
    counts = Counter(message)  # Counter({'l': 2, 'H': 1, 'e': 1, 'o': 1})
    for i in " abcdefghijklmnopqrstuvwxyz":
        print(i, counts[i], counts[i]/5)


frequency_calculator(message_1)
frequency_calculator(message_2)
frequency_calculator(message_3)
frequency_calculator(message_4)
frequency_calculator(message_5)
