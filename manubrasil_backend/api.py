from ninja_extra import NinjaExtraAPI
from dotenv import load_dotenv
from my_auth.api import router as auth_router
from state.api import router as state_router
from city.api import router as city_router
from town_hall.api import router as town_hall_router
from team.api import router as team_router
from neighborhood.api import router as neighborhood_router
from problem.api import router as problem_router
from called.api import router as called_router
from daily.api import router as daily_router
from service_order.api import router as so_router


from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI(title="ManuBrasil API",)
api.register_controllers(NinjaJWTDefaultController)



load_dotenv()

api.add_router("/auth/", auth_router)
api.add_router("/state/", state_router)
api.add_router("/city/", city_router)
api.add_router("/neighborhood/", neighborhood_router)
api.add_router("/town-hall/", town_hall_router)
api.add_router("/team/", team_router)
api.add_router("/problem/", problem_router)
api.add_router("/called/", called_router)
api.add_router("/daily/", daily_router)
api.add_router("/service-order/", so_router)

