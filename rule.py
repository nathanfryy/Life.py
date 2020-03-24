import toolbox

class Rule(object):

    neighbor1 = 2
    neighbor2 = 3
    neighbor3 = 3

    ruleSets = {'basic': {'neighbor1': 2, 'neighbor2': 3, 'neighbor3': 3},
                   'Up-One': {'neighbor1': 3, 'neighbor2': 4, 'neighbor3': 4},
                   'Bone-Dry': {'neighbor1': 1, 'neighbor2': 2, 'neighbor3': 2},
                   'Reverse': {'neighbor1': 3, 'neighbor2': 2, 'neighbor3': 2},
                   'Stupid-Big': {'neighbor1': 5, 'neighbor2': 7, 'neighbor3': 7}}

    currentRuleSet = 'basic'

    neighbor1 = ruleSets[currentRuleSet]['neighbor1']
    neighbor2 = ruleSets[currentRuleSet]['neighbor2']
    neighbor3 = ruleSets[currentRuleSet]['neighbor3']

    @classmethod
    def set_rule(cls, ruleSet):
        """
        Given a currentDisplaySet that is a key of the displaySets, change the
        liveChar and deadChar class variables to the corresponding values for that
        displayset.
        :param displaySet: A key to the displaySets
        :return:
        """
        legalValues = cls.ruleSets.keys()
        if ruleSet in legalValues:
            cls.currentRuleSet = ruleSet
            cls.neighbor1 = cls.ruleSets[ruleSet]['neighbor1']
            cls.neighbor2 = cls.ruleSets[ruleSet]['neighbor2']
            cls.neighbor3 = cls.ruleSets[ruleSet]['neighbor3']
        else:
            raise ValueError(f'Rule Set must be in {legalValues}.')




    def get_ruleSet(self):
        return self.__currentRuleSet

