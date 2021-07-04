import utils
import Allele

class People:
    destructed_people = 0
    created_people = 0

    def __init__(self, sex, Paternal_allele, Maternal_allele, gen_of_birth, argv, age=0,
                 N_sons=0, N_daughters=0, N_brothers=0, N_sisters=0, Mother=None, Father=None):
        self.Gen_of_birth = gen_of_birth
        self.Age = age
        self.Sex = sex  # 0-female, 1-male
        self.Paternal_allele = Paternal_allele
        self.Maternal_allele = Maternal_allele
        self.Son_prob = 0.5 + self.Paternal_allele.effect + self.Maternal_allele.effect
        self.Daughter_prob = 1 - self.Son_prob
        self.N_sons = N_sons
        self.N_daughters = N_daughters
        self.offspring_list = []
        self.Mother = Mother
        self.Father = Father

        self.N_Brother = N_brothers
        self.N_Sister = N_sisters
        self.sibling_list = []
        self.survival_rate = self.get_survival_rate(argv)
        self.mating_willingness = self.get_mating_willingness(argv)
        # self.uid = self.get_uid(self)
        People.created_people += 1

    def update(self,argv):
        self.survival_rate = self.get_survival_rate(argv)
        self.mating_willingness = self.get_mating_willingness(argv)

    def get_survival_rate(self, argv):
        if self.Sex == 0:
            _survival_rate = 1 - argv['Primary_mortality_with_age_female'][self.Age]
        else:
            _survival_rate = 1 - argv['Primary_mortality_with_age_male'][self.Age]

        if argv['Parental_investment']:
            for offspring in self.offspring_list:
                if offspring.Sex == 0:
                    _survival_rate *= (1+argv['PI_daughter_coef'][offspring.Age])
                else:
                    _survival_rate *= (1+argv['PI_son_coef'][offspring.Age])

        if argv['Parental_care']:
            if self.Father is not None:
                _survival_rate = _survival_rate * (1 + argv['Father_coef'])
            if self.Mother is not None:
                _survival_rate = _survival_rate * (1 + argv['Mother_coef'])

        if argv['Sibling_effect']:
            _survival_rate = _survival_rate * (1 + argv['Bro_coef'] * self.N_Brother) * \
                             (1 + argv['Sis_coef'] * self.N_Sister)

        return max(0, min(1, _survival_rate))  # ensure return 0<=_survival_rate<=1

    def get_mating_willingness(self, argv):
        if self.Sex == 0:
            _mating_willingness = argv['Primary_reproduction_rate_with_age_female'][self.Age]
        else:
            _mating_willingness = argv['Primary_reproduction_rate_with_age_male'][self.Age]

        if argv['Mating_willingness']:
            _mating_willingness = _mating_willingness * (1 + argv['MW_son_coef'] * self.N_sons) * \
                                  (1 + argv['MW_daughter_coef'] * self.N_daughters)

        return max(0, min(1, _mating_willingness))

    def __del__(self):
        # print('__del__')
        People.destructed_people += 1
