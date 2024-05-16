from ..sim_event import SimEvent


class ShopSellEvent(SimEvent):
    def __init__(
        self,
        time: int,
    ) -> None:
        super().__init__(time, 0)
        
    
