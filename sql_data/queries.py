from .sql import session, Employee


class QueriesGet:

    def __init__(self):
        self._session = session

    async def get_users(self) -> list:
        with self._session as ses:
            auth_employees = ses.query(Employee.last_name).all()
            auth_employees = [name[0] for name in auth_employees]
            return auth_employees
