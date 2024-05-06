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
def main():
    sim_map_builder=BuilderSimMap(55,40)
    simulation_map=sim_map_builder.create_instance()
    ##Crear el enviroment y el simulador

    environment = SimEnvironment(simulation_map)

    simulator = SupplyChainSimulator(environment, 60 * 60 * 24 * 7)

    get_time = environment.get_time

    add_event = simulator.add_event

    send_msg = environment.send_message

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

    distributor_building = BuildingDistributorAgent(seed, env_visualizer, get_time, add_event)

    productor_1=productor_agent.create_instance("Producer_1")

    matrix_=matrix_Building.create_matrix_agent("Matrix",["Tienda_1"])

    distributor_1 = distributor_building.create_instance("Distributor_1")

    environment.add_agents([productor_1, matrix_, distributor_1])
    environment.add_matrix_companies([matrix_.company])
    environment.add_companies_in_map([productor_1.company, distributor_1.company])

    msg=StoreWantRestock(company_from="Tienda_1",
                         company_from_type=TypeCompany.Store,
                         company_destination_name="Matrix",
                         company_destination_type=TypeCompany.Matrix,
                         product_want_name="Cheese",
                         count_want_restock=20
                         )


    send_msg(msg)


if __name__ == "__main__":

    main()



