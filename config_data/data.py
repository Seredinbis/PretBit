from dataclasses import dataclass, fields


@dataclass()
class Position:

    lead_enginer: str = 'Ведущий инженер'
    enginer: str = 'Инженер'
    head_crew: str = 'Начальник осветительской службы'
    head_day: str = 'Начальник смены'
    technical: str = 'Техник'
    light: str = 'Осветитель'
    light_operator: str = 'Светооператор'

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)
