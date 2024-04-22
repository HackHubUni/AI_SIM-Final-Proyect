def infer_belief(self, rule):
        # Check if the rule's antecedents are already in the belief base
        antecedents = rule.antecedents
        beliefs_met = False
        for antecedent in antecedents:
            if not any(belief.proposition == antecedent and belief.value == True for belief in self.belief_base):
                beliefs_met = True
                break

        if beliefs_met:
            # Apply the rule if all antecedents are met
            consequent = rule.consequent
            existing_belief = next((belief for belief in self.belief_base if belief.proposition == consequent), None)
            if existing_belief:
                existing_belief.value = True
            else:
                self.add_belief(Belief(consequent, True))


from random import random
from time import sleep

# Distribución exponencial con media de 100 milisegundos
lambda_exp = 1 / 0.1

# Generar 10 tiempos de arribo
tiempos_arribo = []
for i in range(10):
    # Número aleatorio entre 0 y 1
    u = random()

    # Función inversa de la distribución exponencial
    tiempo_arribo = -math.log(u) / lambda_exp

    # Retardo en milisegundos
    sleep(tiempo_arribo * 1000)

    tiempos_arribo.append(tiempo_arribo)

print(tiempos_arribo)
