import networkx as nx
from networkx import DiGraph


class MatrixOptimizer:
    def __init__(self):
        self.fake_sink = 'sink'
        self.source = 'source'

    def _append_in_the_list_to_create_graph(self, companys_dic: dict[str, dict[str, float]], count_want: int):
        """
        Crea la lista que necesita para llenar el grafo se pasa un tipo de empresa por decision
         (fuente,prove_1, {"capacity":9, "weight": 0}),
        :return:
        """
        lis = []
        for company_offer_id in companys_dic.keys():
            # Devuelve el diccionario de cada oferta de cada empresa de esta forma
            # {"capacity":cant maxima a sumnistrar,"weight": 0})
            company_condiction = companys_dic[company_offer_id]
            # Añade la arista que tiene el precio y la cant maxima a suministrar desde un alamcen a la fuente falsa

            lis.append((company_offer_id, self.fake_sink, company_condiction))

            # Añade la arista desde la fuenta hasta cada almacen
            lis.append((self.source, company_offer_id, {"capacity": count_want, "weight": 0}))
        return lis


    def create_graph(self, sink_name: str, count_want: int, lis_companys: list[dict[str, dict[str, float]]]

                     ):
        """
        Recibe por cada tipo de empresa un diccionario donde viene el nombre de la oferta y el diccionario de restricciones
        :param sink_name:
        :param count_want:
        :param lis_companys:
        :return:
        """

        G = nx.DiGraph()
        lis = [(self.fake_sink, sink_name, {"capacity": count_want, "weight": 0})]

        for item in lis_companys:
            # Añadir la lista por cada tipo de empresa
            lis.extend(self._append_in_the_list_to_create_graph(item,count_want))

        G.add_edges_from(lis)

        return G

    def _get_min_cost_after_flow_solution(self, G: DiGraph, mincostFlow: dict):
        """
        Dado el grafo y el diccionario que representa el flujo maximo de costo minimo me devuelve el coste de este
        :param G:
        :param mincostFlow:
        :return:
        """
        # costo de la red
        mincost = nx.cost_of_flow(G, mincostFlow)
        return mincost

    def get_list_offer_to_acept_with_count_to_want(self, mincostFlow: dict, companys_offer_lis: list[str]) -> dict[
        str, int]:
        """
        Dado el diccionario con el flujo maximo de costo minimo devuelve la lista de cosas que se aceptaron
        :param mincostFlow:
        :return:
        """

        dic_return: dict[str, int] = {}

        if not self.source in mincostFlow:
            raise Exception(f' En el diccionario no esta la source {self.source} diccionario: {mincostFlow}')
        # Se ve cuanto se envio de la fuente a cada empresa que es lo mismo que envio cada empresa hasta el receptor
        offer_to_see = mincostFlow[self.source]

        for offer_id in companys_offer_lis:
            if not offer_id in offer_to_see:
                raise Exception(f'La oferta {offer_id} no está entre las que salen de la fuente')
            val = offer_to_see[offer_id]
            if not isinstance(val, int):
                raise Exception(
                    f'Para la oferta {offer_id} se esperaba que el valor fuera entero pero {val} es de tipo {type(val)}')
            # Si no es mayor que cero sigo a la siguente iteración
            if val < 1:
                continue
            # Lo añado solo si es mayor que cero
            dic_return[offer_id] = val

        return dic_return
    def _get_all_offers_ids(self, lis_companys: list[dict[str, dict[str, float]]])->list[str]:
        lis:list[str]=[]

        for item in lis_companys:
            lis.extend(item.keys())

        return lis

    def solve_normal_solution(self, store_name: str, count_want: int, lis_companys: list[dict[str, dict[str, float]]])->tuple[dict[str, int], float]:
        """
        Llamar a este metodo para resolver el problema grande
        :param store_name:
        :param count_want:
        :param lis_companys:
        :return: El diccionario con los contratos aceptar y el float con el costo de todo
        """
        graph = self.create_graph(store_name, count_want, lis_companys)
        mincostFlow=self.solve_graph(graph,store_name)
        oferts_id=self._get_all_offers_ids(lis_companys)
        list_return=self.get_list_offer_to_acept_with_count_to_want(mincostFlow,oferts_id)
        min_cost=self._get_min_cost_after_flow_solution(graph,mincostFlow)
        return list_return,min_cost
    def solve_graph(self, G: DiGraph, store_name: str):
        """
        Dado el grafo de NetworkNx devuelve el diccionario con la red de flujo
        y el coste minimo de todo
        :param G:
        :param store_name:
        :return:
        """

        mincostFlow = nx.max_flow_min_cost(G, self.source, store_name)
        return mincostFlow
