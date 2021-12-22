from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # тип тренировки
    duration: float  # длительность тренировки в часах
    distance: float  # дистанция, преодолённая за тренировку в км
    speed: float  # средняя скорость движения в км/ч
    calories: float  # потраченные за время тренировки ккал

    INFO_MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Вернуть информационное сообщение с параметрами тренировки."""
        return self.INFO_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1_000  # метров в 1 км
    LEN_STEP: float = 0.65  # длина 1 шага в м
    MIN_IN_HR: int = 60  # минут в 1 часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action  # количество действий (шагов, гребков)
        self.duration: float = duration  # длительность тренировки в часах
        self.weight: float = weight  # вес спортсмена в кг

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Метод "get_spent_calories" для класса наследника'
            f'{self.__class__.__name__} не определен'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIES_1: int = 18  # коэфф. для расчета затраченных ккал
    COEFF_CALORIES_2: int = 20  # коэфф. для расчета затраченных ккал

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIES_1 * self.get_mean_speed()
             - self.COEFF_CALORIES_2) * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_HR)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIES_3: float = 0.035  # коэфф. для расчета затраченных ккал
    COEFF_CALORIES_4: float = 0.029  # коэфф. для расчета затраченных ккал

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height  # рост спортсмена в см

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIES_3 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.COEFF_CALORIES_4 * self.weight)
            * self.duration * self.MIN_IN_HR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # длина 1 гребка в м
    COEFF_CALORIES_5: float = 1.1  # коэфф. для расчета затраченных ккал
    COEFF_CALORIES_6: int = 2  # коэфф. для расчета затраченных ккал

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool  # длина бассейна в метрах
        self.count_pool: float = count_pool  # количество переплытых басейнов

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIES_5)
            * self.COEFF_CALORIES_6
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_trainings: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in type_trainings:
        raise ValueError(f'Тип тренировки "{workout_type}" не релевантен')
    return type_trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
