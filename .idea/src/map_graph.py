from src.protocol.agentprotocol import Agent


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
                f"The distance between companies should not be less than zero")
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
    def is_company_added(company: Agent, company_list: list[CompanyConnections]) -> bool:
        """Returns True if the company is inside the list of companies"""
        for i in range(len(company_list)):
            comp = company_list[i].company
            if comp == company:
                return True
        return False

    def add_provider(self, provider_company: Agent) -> bool:
        if MapGraph.is_company_added(provider_company, self.provider_companies):
            return False
        self.provider_companies.append(CompanyConnections(provider_company))
        return True

    def add_manufacturer(self, manufacturer_company: Agent) -> bool:
        if MapGraph.is_company_added(manufacturer_company, self.manufacturer_companies):
            return False
        self.manufacturer_companies.append(
            CompanyConnections(manufacturer_company))
        return True

    def add_retailer(self, retailer_company: Agent) -> bool:
        if MapGraph.is_company_added(retailer_company, self.retailer_companies):
            return False
        self.retailer_companies.append(CompanyConnections(retailer_company))
        return True

    def add_storage(self, storage_company: Agent) -> bool:
        if MapGraph.is_company_added(storage_company, self.storage_companies):
            return False
        self.retailer_companies.append(CompanyConnections(storage_company))
        return True

    # region Connections between companies

    def connect_provider_with_another_company(self, provider_company: Agent, other_company):
        pass

    # endregion
