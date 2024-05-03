from supply_chain.Company.companies_types.Matrix_Company import MatrixCompany
from supply_chain.agents.AgentWrapped import *
from supply_chain.Building.create_planner import *

class MatrixAgent(AgentWrapped):
    def __init__(self,
                 name: str,
                 company: MatrixCompany,
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name,company,env_visualizer)
        self.company:MatrixCompany=company
        self.planner:PlanningProblem=get_planing_Type()


    def computate_msg(self,msg):
        self.planner.convert(msg)



    def recive_msg(self, msg: Message):

        if isinstance(msg, ResponseOfertProductMessaage):

         self.msg = self.computate_msg(msg)
        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)


