from src.protocol.agentprotocol import Agent
from random import *


class CompanyConnections:
    def __init__(self, companyAgent: Agent) -> None:
        self.company: Agent = companyAgent
        """This represents the current company"""
        self.connections: list[tuple[Agent, float]] = []
        """This is a list of connections of this company. A connection is a tuple
        of a company agent as the first element and a float as second element representing
        the distance from this company to the company of the first element in the tuple"""

    def add_connection(self, company: Agent, distance: float) -> bool:
        """This method returns True if it's possible to add the company as a new connection.
        Returns False if the company is already in the connections"""
        if self.is_company_connected(company):
            return False
        if distance <= 0:
            raise Exception(
                f"The distance between companies should not be less than zero"
            )
        self.connections.append((company, distance))
        return True

    def get_connection(self, other_company: Agent) -> tuple[Agent, float]:
        for i in range(len(self.connections)):
            company, distance = self.connections[i]
            if company == other_company:
                return company, distance
        # TODO: The company agents need names
        raise Exception(f"There is no connection with the given company")

    def is_company_connected(self, other_company: Agent) -> bool:
        """Returns True if the 'other_company is a connection of this company"""
        return any(company == other_company for company, _ in self.connections)

    def remove_connection(self, other_company: Agent) -> bool:
        """Returns True if the 'other_company" is a connection of this company and the connection is removed.
        Returns False if the 'other_company' was not found as a connection"""
        for i in range(len(self.connections)):
            company, distance = self.connections[i]
            if company == other_company:
                self.connections.remove((company, distance))
                return True
        return False

    def get_distance_to_company(self, other_company: Agent) -> float:
        return self.get_connection(other_company=other_company)[1]


class MapGraph:
    def __init__(self) -> None:
        self.provider_companies: list[CompanyConnections] = []
        self.manufacturer_companies: list[CompanyConnections] = []
        self.retailer_companies: list[CompanyConnections] = []
        self.storage_companies: list[CompanyConnections] = []

    @staticmethod
    def is_company_added(
        company: Agent, company_list: list[CompanyConnections]
    ) -> tuple[bool, CompanyConnections]:
        """Returns True if the company is inside the list of companies"""
        for i in range(len(company_list)):
            comp = company_list[i].company
            if comp == company:
                return True, company_list[i]
        return False, None

    def add_provider(self, provider_company: Agent) -> bool:
        if MapGraph.is_company_added(provider_company, self.provider_companies)[0]:
            return False
        self.provider_companies.append(CompanyConnections(provider_company))
        return True

    def add_manufacturer(self, manufacturer_company: Agent) -> bool:
        if MapGraph.is_company_added(manufacturer_company, self.manufacturer_companies)[
            0
        ]:
            return False
        self.manufacturer_companies.append(CompanyConnections(manufacturer_company))
        return True

    def add_retailer(self, retailer_company: Agent) -> bool:
        if MapGraph.is_company_added(retailer_company, self.retailer_companies)[0]:
            return False
        self.retailer_companies.append(CompanyConnections(retailer_company))
        return True

    def add_storage(self, storage_company: Agent) -> bool:
        if MapGraph.is_company_added(storage_company, self.storage_companies)[0]:
            return False
        self.retailer_companies.append(CompanyConnections(storage_company))
        return True

    def get_provider_connections(self, provider_company: Agent) -> CompanyConnections:
        return MapGraph.is_company_added(provider_company, self.provider_companies)[1]

    def get_manufacturer_connections(
        self, manufacturer_company: Agent
    ) -> CompanyConnections:
        return MapGraph.is_company_added(
            manufacturer_company, self.manufacturer_companies
        )[1]

    def get_retailer_connections(self, retailer_company: Agent) -> CompanyConnections:
        return MapGraph.is_company_added(retailer_company, self.retailer_companies)[1]

    def get_storage_connections(self, storage_company: Agent) -> CompanyConnections:
        return MapGraph.is_company_added(storage_company, self.storage_companies)[1]

    # region Connections between companies

    def connect_provider_with_manufacturer(
        self,
        provider_company: Agent,
        manufacturer_company: Agent,
        distance: float,
    ) -> bool:
        provider_result = MapGraph.is_company_added(
            provider_company, self.provider_companies
        )
        if not provider_result[0]:
            return False
        manufacturer_result = MapGraph.is_company_added(
            manufacturer_company, self.manufacturer_companies
        )
        if not manufacturer_result[0]:
            return False
        provider_connection = provider_result[1]
        manufacturer_connection = manufacturer_result[1]
        provider_connection.add_connection(
            manufacturer_connection.company, distance=distance
        )
        manufacturer_connection.add_connection(
            provider_connection.company, distance=distance
        )
        return True

    def connect_manufacturer_with_storage(
        self,
        manufacturer_company: Agent,
        storage_company: Agent,
        distance: float,
    ) -> bool:
        manufacturer_result = MapGraph.is_company_added(
            manufacturer_company, self.manufacturer_companies
        )
        if not manufacturer_result[0]:
            return False
        storage_result = MapGraph.is_company_added(
            storage_company, self.storage_companies
        )
        if not storage_result[0]:
            return False
        manufacturer_connection = manufacturer_result[1]
        storage_connection = storage_result[1]
        manufacturer_connection.add_connection(
            storage_connection.company, distance=distance
        )
        storage_connection.add_connection(
            manufacturer_connection.company, distance=distance
        )
        return True

    def connect_storage_with_retailer(
        self,
        storage_company: Agent,
        retailer_company: Agent,
        distance: float,
    ) -> bool:
        storage_result = MapGraph.is_company_added(
            storage_company, self.storage_companies
        )
        if not storage_result[0]:
            return False
        retailer_result = MapGraph.is_company_added(
            retailer_company, self.retailer_companies
        )
        if not retailer_result[0]:
            return False
        storage_connection = storage_result[1]
        retailer_connection = retailer_result[1]
        storage_connection.add_connection(
            retailer_connection.company, distance=distance
        )
        retailer_connection.add_connection(
            storage_connection.company, distance=distance
        )
        return True

    # endregion


class RandomMapGenerator:
    def __init__(
        self,
        provider_companies: list[Agent],
        manufacturer_companies: list[Agent],
        storage_companies: list[Agent],
        retailer_companies: list[Agent],
        minimum_distance: float,
        maximum_distance: float,
    ) -> None:
        self.minimum_distance: float = minimum_distance
        self.maximum_distance: float = maximum_distance
        self.provider_companies: list[Agent] = provider_companies
        self.manufacturer_companies: list[Agent] = manufacturer_companies
        self.storage_companies: list[Agent] = storage_companies
        self.retailer_companies: list[Agent] = retailer_companies

    def get_random_distance(self):
        return uniform(self.minimum_distance, self.maximum_distance)

    def generate_random_map(self) -> MapGraph:
        map_graph = MapGraph()
        for provider in self.provider_companies:
            map_graph.add_provider(provider)
        for manufacturer in self.manufacturer_companies:
            map_graph.add_manufacturer(manufacturer)
        for storage in self.storage_companies:
            map_graph.add_storage(storage)
        for retailer in self.retailer_companies:
            map_graph.add_retailer(retailer)
        for provider in self.provider_companies:
            for manufacturer in self.manufacturer_companies:
                map_graph.connect_provider_with_manufacturer(
                    provider,
                    manufacturer,
                    distance=self.get_random_distance(),
                )
        for manufacturer in self.manufacturer_companies:
            for storage in self.storage_companies:
                map_graph.connect_manufacturer_with_storage(
                    manufacturer,
                    storage,
                    distance=self.get_random_distance(),
                )
        for storage in self.storage_companies:
            for retailer in self.retailer_companies:
                map_graph.connect_storage_with_retailer(
                    storage,
                    retailer,
                    distance=self.get_random_distance(),
                )
        return map_graph
