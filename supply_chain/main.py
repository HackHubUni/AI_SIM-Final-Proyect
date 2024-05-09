import matplotlib.pyplot as plt

from supply_chain.Building.Builder_agent import *
from supply_chain.Building.Builder_map import BuilderSimMap
from supply_chain.sim_environment import SimEnvironment
from supply_chain.simulation import SupplyChainSimulator
from supply_chain.utils.points_generators import poisson_disc_sampling

points = poisson_disc_sampling(10 + 5 + 5 + 20, (0, 0), (5000, 5000), 20, 20)
plt.scatter([p[0] for p in points], [p[1] for p in points])
print(len(points))
# Now let's create some connections

def create_ware_house_agents(count_want: int, seed, env_visualizer: EnvVisualizer, get_time, add_event):
    build_ware_house_agent = BuildingWareHouseAgent(seed, env_visualizer, get_time, add_event)
    lis = []
    for i in range(1, count_want + 1):
        lis.append(build_ware_house_agent.get_ware_house_agent(f'WareHouse_{i}', 'Matrix', TypeProduction.Blended))
    return lis


def create_Distribution_agent(count_want: int, seed: int, env_visualizer: EnvVisualizer, get_time, add_event):
    lis = []

    for i in range(0, count_want):
        lis.append(BuildingDistributorAgent(seed, env_visualizer, get_time, add_event).create_instance(f'Logistic_{i}'))

    return lis



def create_Manufacturer_agent(count_want:int,seed:int, env_visualizer: EnvVisualizer, get_time, add_event):
    lis=[]

    for i in range(0,count_want):
        lis.append(BuildingManufacturerAgent(seed, env_visualizer, get_time, add_event).create_manufacturer_agent(f'Manufactor_{i}'))
    return lis
def main():
    sim_map_builder=BuilderSimMap(55,40)
    simulation_map=sim_map_builder.create_instance()
    ##Crear el enviroment y el simulador

    environment = SimEnvironment(simulation_map)

    simulator = SupplyChainSimulator(environment, 60 * 60 * 24 * 7)

    get_time = environment.get_time

    add_event = simulator.add_event

    send_msg = environment.send_message

    get_agent_by_name = environment.get_agent_by_name

    seed=1234

    def get_dict_valoracion_inicial() -> dict[TypeCompany, dict[str, float]]:
        dict_return = {}
        dict_2 = {"Matrix": 7}
        dict_return[TypeCompany.Matrix] = dict_2
        return dict_return


    def get_logic_implication() -> list[ImplicationLogicWrapped]:
        cliente_x = ClientWrapped('x')  # Cliente(x)
        valoracion_x_bien = Valoracion("x", ValoracionTag.Bien)  # Valoracion_(x,Bien)

        product_y = ProductWrapped('y')  # Product_(y)

        pedir_precio_hecho = PedirPrecio('x', 'y', NumberWrapped(1))  # Pedir_precio(x,y,1) persona # # producto factor=1

        pedir_cant_suplir_hecho = PedirCantidad('x', 'y', NumberWrapped(1))
        left_part = AndLogicWrapped(
            [cliente_x, valoracion_x_bien, product_y])
        implication_ = ImplicationLogicWrapped(
            [left_part], [pedir_precio_hecho]
        )

        implication_pedir_cant_suplir = ImplicationLogicWrapped(
            [left_part], [pedir_cant_suplir_hecho]
        )
        return [implication_, implication_pedir_cant_suplir]



    env_visualizer=EnvVisualizer(get_time,send_msg,get_dict_valoracion_inicial,get_logic_implication,environment.get_minimum_distance)

    matrix_env_=MatrixEnvVisualizer(get_time,send_msg,get_dict_valoracion_inicial,get_logic_implication,environment.get_minimum_distance,lambda :["Producer_1"],lambda :[],lambda :[],lambda :["Distributor_1"])
    productor_agent=BuildingProducerAgent(seed,env_visualizer, get_time, add_event)



    matrix_Building=BuildingMatrixAgent(seed,matrix_env_,get_time, add_event)

    matrix_ = matrix_Building.create_matrix_for_experiment("Matrix", 1, 2, 1, 3, get_agent_by_name)

    agents_list_in_the_map=create_Distribution_agent(1,seed,env_visualizer,get_time,add_event)

    agents_list_in_the_map.extend(create_Manufacturer_agent(1,seed,env_visualizer,get_time,add_event))

    agents_list_in_the_map.extend(create_ware_house_agents(1,seed,env_visualizer,get_time,add_event))

    agents_list =agents_list_in_the_map+ [matrix_] + matrix_.store_agents
    environment.add_agents(agents_list)
    environment.add_matrix_companies([matrix_.company])
    list_companys_in_the_map = [x.company for x in agents_list_in_the_map] + matrix_.stores_companys
    environment.add_companies_in_map(list_companys_in_the_map)
    simulator.run()

    print(2)



if __name__ == "__main__":

    main()



