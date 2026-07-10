from fastapi import APIRouter

from app.monitoring.metrics_service import (

    MetricsService

)

router = APIRouter(

    prefix="/metrics",

    tags=["Metrics"]

)


@router.get("/")
def metrics():

    statistics = MetricsService.statistics()

    requests = MetricsService.all_metrics()

    return {

        "statistics": statistics,

        "recent_requests":

            requests[-20:]

    }