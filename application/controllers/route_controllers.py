from typing import List
from fastapi import APIRouter, FastAPI


class RouteRegisterController:

    def __init__(self, app: FastAPI, router_list: List[APIRouter]):
        self.router_list = router_list
        self.app = app

    def register_routes(self):
        for router in self.router_list:
            self.app.include_router(router)
        return self.app
