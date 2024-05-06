import matplotlib.pyplot as plt

from supply_chain.Building.building_companys import *
from supply_chain.map_search_problem import MapSearchProblem
from supply_chain.sim_ai.search_problem.search_algorithms import *
from supply_chain.sim_environment import SimEnvironment
from supply_chain.sim_map import SimMap
from supply_chain.simulation import SupplyChainSimulator
from supply_chain.utils.points_generators import poisson_disc_sampling
from supply_chain.Building.Builder_agent import *
points = poisson_disc_sampling(10 + 5 + 5 + 20, (0, 0), (5000, 5000), 20, 20)
plt.scatter([p[0] for p in points], [p[1] for p in points])
print(len(points))
# Now let's create some connections
def main():
    number_of_connections = 50
    connections: list[tuple[tuple[float, float], tuple[float, float]]] = []

    simulation_map: SimMap = SimMap()

    for _ in range(number_of_connections):
        p1, p2 = rnd.sample(points, 2)
        connections.append((p1, p2))
        simulation_map.add_bidirectional_connection_with_random_distance(p1, p2, 50, True)


    def map_heuristic(
            actual_position: tuple[float, float], final_position: tuple[float, float]
    ) -> float:
        return distance_between_points(actual_position, final_position)


    def path(node: SearchNode) -> tuple[list[float], list[float]]:
        result = node.get_path()
        x_coordinates = [p[0] for p in result]
        y_coordinates = [p[1] for p in result]
        return (x_coordinates, y_coordinates)


    initial_position, final_position = rnd.sample(points, 2)

    map_problem = MapSearchProblem(
        initial_position=initial_position,
        final_position=final_position,
        city_map=simulation_map,
    )
    found, final_node = a_star_search(
        map_problem, lambda node: map_heuristic(node.state, final_position)
    )

    if found:
        print(f"A path was found")
        original_path = final_node.get_path()
        for state in original_path:
            print(state)
        #plot_map(points, connections, path(final_node))
        print(f"The distance is {final_node.path_cost:2f}")
        # plt.show()
    else:
        print("A path was not found")

    ##Crear el enviroment y el simulador

    environment = SimEnvironment(simulation_map)

    simulator = SupplyChainSimulator(environment, 60 * 60 * 24 * 7)

    get_time = environment.get_time

    add_event = simulator.add_event

    send_msg = environment.send_message

    seed=1234

    def get_dict_valoracion_inicial() -> dict[TypeCompany, dict[str, float]]:
        dict_return = {}
        dict_2 = {"Matrix_1": 7}
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

    matrix_env_=MatrixEnvVisualizer(get_time,send_msg,get_dict_valoracion_inicial,get_logic_implication,environment.get_minimum_distance,lambda :["Producer_1"],lambda :[],lambda :[],lambda :[])
    productor_agent=BuildingProducerAgent(seed,env_visualizer, get_time, add_event)



    matrix_Building=BuildingMatrixAgent(seed,matrix_env_,get_time, add_event)


    productor_1=productor_agent.create_Producer_Agent("Producer_1")

    matrix_=matrix_Building.create_matrix_agent("Matrix",["Tienda_1"])

    environment.add_agents([productor_1,matrix_])
    environment.add_matrix_companies([matrix_.company])
    environment.add_companies_in_map([productor_1.company])

    msg=StoreWantRestock(company_from="Tienda_1",
                         company_from_type=TypeCompany.Store,
                         company_destination_name="Matrix",
                         company_destination_type=TypeCompany.Matrix,
                         product_want_name="Pizza",
                         count_want_restock=20
                         )


    send_msg(msg)


if __name__ == "__main__":

    main()



