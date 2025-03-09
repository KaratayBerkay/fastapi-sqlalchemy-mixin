import os

from sqlalchemy import text
from sqlalchemy.orm import scoped_session


class AlembicController:

    def __init__(self, session: scoped_session):
        self.session = session

    def update_alembic(self):
        try:
            result = self.session.execute(
                text(
                    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = "
                    "'alembic_version') AS table_existence;"
                )
            )
            alembic_table_existence = result.first()
            if alembic_table_existence[0]:
                self.session.execute(text("delete from alembic_version;"))
                self.session.commit()
        except Exception as e:
            print(f"Error @Alembic initialize: {e}")
        finally:
            run_command = "python -m alembic stamp head;"
            run_command += "python -m alembic revision --autogenerate;"
            run_command += "python -m alembic upgrade head;"
            os.system(run_command)
