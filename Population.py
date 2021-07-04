from People import People
from utils import get_random
import numpy.random as nrand

class Population:
    def __init__(self):
        self.N_male = 0
        self.N_female = 0
        self.Male_list = []
        self.Female_list = []
        self.Current_generation = 0
        self.N_sex_with_age = None
        self.max_age = 11
        #self.MORTALITY_COEFFICIENT = 2e-12
        self.pop_survival_rate = 1
        #self.update()
        self.N_people_died = 0

    def Add_people(self, people):
        if people.Sex == 0:
            self.Female_list.append(people)
        else:
            self.Male_list.append(people)

    def get_N_sex_with_age(self):
        N_sex_with_age_dict = {'Male': [0] * self.max_age, 'Female': [0] * self.max_age}
        for people in self.Male_list:
            N_sex_with_age_dict['Male'][people.Age-1] += 1
        for people in self.Female_list:
            N_sex_with_age_dict['Female'][people.Age-1] += 1
        return N_sex_with_age_dict

    def reproduce(self, argv):
        Male_mating = []
        Female_mating = []
        for people in self.Male_list:
            if get_random() < people.mating_willingness:
                Male_mating.append(people)
        for people in self.Female_list:
            if get_random() < people.mating_willingness:
                Female_mating.append(people)
        nrand.shuffle(Male_mating)
        for i in range(min(len(Male_mating), len(Female_mating))):
            self.mate2people(Male_mating[i], Female_mating[i], argv)
        self.update(argv)

    def next_generation(self, argv):
        Male_list_new = []
        Female_list_new = []
        for sex, Pop_list in zip(['Male', 'Female'], [self.Male_list, self.Female_list]):
            for people in Pop_list:
                # Survived
                if get_random() < people.survival_rate * self.pop_survival_rate:
                    people.Age += 1
                    people.update(argv)
                    if sex == 'Male':
                        Male_list_new.append(people)
                    else:
                        Female_list_new.append(people)
                else:
                    # Died
                    if people.Mother is not None:
                        people.Mother.N_sons -= 1
                        people.Mother.offspring_list.remove(people)
                        assert people not in people.Mother.offspring_list
                        people.Mother.update(argv)
                    if people.Father is not None:
                        people.Father.N_sons -= 1
                        people.Father.offspring_list.remove(people)
                        assert people not in people.Father.offspring_list
                        people.Father.update(argv)
                    for offspring in people.offspring_list:
                        if sex == 'Male':
                            # offspring.Father_status = False
                            offspring.Father = None
                        else:
                            # offspring.Mother_status = False
                            offspring.Mother = None
                        offspring.update(argv)
                    # people.offspring_list = None
                    for sibling in people.sibling_list:
                        if sex == 'Male':
                            sibling.N_Brother -= 1
                        else:
                            sibling.N_Sister -= 1
                        sibling.sibling_list.remove(people)
                        assert people not in sibling.sibling_list
                        sibling.update(argv)
                    # people.sibling_list = None
                    self.N_people_died += 1
                    # print('people died')

        self.Male_list = Male_list_new
        self.Female_list = Female_list_new
        self.Current_generation += 1
        self.update(argv)

    def mate2people(self, Male, Female, argv):
        Son_prob = (Male.Son_prob + Female.Son_prob) / 2
        if get_random() < Son_prob:
            sex = 1
            Male.N_sons += 1
            Female.N_sons += 1
        else:
            sex = 0
            Male.N_daughters += 1
            Female.N_daughters += 1

        if get_random() < 0.5:
            Paternal_allele = Male.Paternal_allele
        else:
            Paternal_allele = Male.Maternal_allele
        if get_random() < 0.5:
            Maternal_allele = Female.Paternal_allele
        else:
            Maternal_allele = Female.Maternal_allele
        offspring = People(sex, Paternal_allele, Maternal_allele,
                           gen_of_birth=self.Current_generation, argv=argv, age=0,
                           Mother=Female, Father=Male)
        if sex == 0:
            self.Female_list.append(offspring)
            for sibling in {*Male.offspring_list, *Female.offspring_list}:
                sibling.N_Sister += 1
                sibling.sibling_list.append(offspring)
                offspring.sibling_list.append(sibling)
        else:
            self.Male_list.append(offspring)
            for sibling in {*Male.offspring_list, *Female.offspring_list}:
                sibling.N_Brother += 1
                sibling.sibling_list.append(offspring)
                offspring.sibling_list.append(sibling)

        # update Parents
        Male.offspring_list.append(offspring)
        Female.offspring_list.append(offspring)

    def get_allele_dict(self):
        allele_dict = {}
        for Pop in [self.Male_list, self.Female_list]:
            for people in Pop:
                if people.Paternal_allele.index in allele_dict:
                    allele_dict[people.Paternal_allele.index] += 1
                else:
                    allele_dict[people.Paternal_allele.index] = 1
                if people.Maternal_allele.index in allele_dict:
                    allele_dict[people.Maternal_allele.index] += 1
                else:
                    allele_dict[people.Maternal_allele.index] = 1
        return allele_dict

    def update(self, argv):
        self.N_female = len(self.Female_list)
        self.N_male = len(self.Male_list)
        # self.N_sex_with_age = self.get_N_sex_with_age()
        if argv['Population_growth']:
            self.pop_survival_rate = max(0, 1 - (argv['MORTALITY_COEFFICIENT']) * (self.N_female + self.N_male) ** 2)
        else:
            self.pop_survival_rate = 1

    def get_sex_ratio_at_birth(self):
        N_male_at_birth = 0
        N_female_at_birth = 0
        for people in self.Male_list:
            if people.Age == 1:
                N_male_at_birth += 1
        for people in self.Female_list:
            if people.Age == 1:
                N_female_at_birth += 1
        if N_female_at_birth == 0:
            return 0
        return N_male_at_birth / N_female_at_birth