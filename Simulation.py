import yaml
from Population import Population
from People import People
from Allele import Allele


class Simulation:

    def __init__(self):
        self.argv = None
        self.Pop = None
        self.allele_list_dict = {}
        self.allele_append_dict = {}
        self.N_list = []
        self.sex_ratio_list = []
        self.sex_ratio_at_birth_list = []
        self.N_sex_with_age = {}
        self.load_default_settings()

    def load_default_settings(self):
        with open("options.yml", 'r') as f:
            self.argv = yaml.load(f, Loader=yaml.FullLoader)

    def reset(self):
        self.Pop = None
        self.load_default_settings()
        self.allele_list_dict = {}
        self.allele_append_dict = {}
        self.N_list = []
        self.sex_ratio_list = []
        self.sex_ratio_at_birth_list = []
        self.N_sex_with_age = {}

        self.Pop = Population()
        Allele.N = 0
        People.created_people = 0
        People.destructed_people = 0
        allele_dict = {}
        default_allele = Allele(effect=0)
        allele_dict[1] = Allele(effect=-0.2)
        allele_dict[2] = Allele(effect=-0.1)
        allele_dict[3] = Allele(effect=-0.05)
        allele_dict[4] = Allele(effect=-0.02)
        allele_dict[5] = Allele(effect=-0.01)
        allele_dict[6] = Allele(effect=0.01)
        allele_dict[7] = Allele(effect=0.02)
        allele_dict[8] = Allele(effect=0.04)
        allele_dict[9] = Allele(effect=0.1)
        allele_dict[10] = Allele(effect=0.2)


        for sex in [0, 1]:
            for age in range(10):
                for i in range(1000):
                    people = People(sex=sex, Paternal_allele=default_allele, Maternal_allele=default_allele,
                                    gen_of_birth=-age, argv=self.argv, age=age)
                    self.Pop.Add_people(people)

        for allele_idx in range(1, 6):
            for sex in [0, 1]:
                for age in range(10):
                    for i in range(100):
                        people = People(sex=sex, Paternal_allele=allele_dict[allele_idx], Maternal_allele=allele_dict[11-allele_idx], gen_of_birth=-age,
                                        argv=self.argv, age=age)
                        self.Pop.Add_people(people)

        self.Pop.update(self.argv)

    def next_generation(self):
        self.Pop.reproduce(self.argv)
        self.Pop.next_generation(self.argv)

        if (self.Pop.N_male == 0) or (self.Pop.N_female == 0):
            return False

        allele_dict = self.Pop.get_allele_dict()
        for key, value in allele_dict.items():
            if key in self.allele_list_dict:
                self.allele_list_dict[key].append(value)
            else:
                self.allele_list_dict[key] = [value]

        self.allele_append_dict = allele_dict

        self.N_sex_with_age = self.Pop.get_N_sex_with_age()

        self.N_list.append(self.Pop.N_male + self.Pop.N_female)

        self.sex_ratio_list.append(self.Pop.N_male / self.Pop.N_female)

        self.sex_ratio_at_birth_list.append(self.Pop.get_sex_ratio_at_birth())

        return True
