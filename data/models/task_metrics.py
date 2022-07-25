from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, String, JSONB

from data.models.base_model import BaseDbModel
from data.utils.dttm import utc_now


class TaskMetric(BaseDbModel):

    __tablename__ = "task_metrics"

    dag = Column(String, primary_key=True, nullable=False, index=True)
    task = Column(String, primary_key=True, nullable=False, index=True)
    run_date = Column(String, index=True)
    run_status = Column(String, nullable=False)
    extra_data = Column(JSONB)
    created_at = Column(DateTime)

    def __init__(
        self,
        dag: str,
        task: str,
        run_date: str,
        run_status: str,
        extra_data: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = utc_now(),
    ):
        self.dag = dag
        self.task = task
        self.run_date = run_date
        self.run_status = run_status
        self.extra_data = extra_data
        self.created_at = created_at

    def __repr__(self):
        return f"{self.dag}__{self.task}__{self.run_date}__{self.run_status}"
