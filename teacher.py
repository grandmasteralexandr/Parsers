# -*- coding: utf-8 -*-
from random import choice

# Скрипт для случайного выбора учеников для проверяющего учителя, но учитель так же является учеником для других учеников
# тоесть каждый проверяет 3 человека и его тоже проверяют 3 человека, по типу проверки в школе Ш++

# создаем класс учителя
class Teacher:
    # определяем конструктор для каждого экземпляра
    def __init__(self, name):
        self.name = name # имя учителя
        self.learner = [] # список его учеников (кого он проверит)
        self.teacher_count = 0 # количество проверяющих этого ученика (его учителей)

# защита при импорте файла (будет импортироватся только класс, код ниже не выполнится)
if __name__ == "__main__":
    # задаем список учителей
    teacher_list = ["Alexandr Zalenskiy", "Dmitro Napoleon", "Alex Memfis", "Coca Cola", "Anton Pepsi",
                    "Adron Kolaider", "Marina Volochkova", ]
    # ученики являются теми же учетилями, но этот список мы будем постоянно менять так что делаем копию
    remain_learners = list(teacher_list)
    # задаем пустой массив для объектов класса
    teacher_obj = []
    # задаем сколько человек нужно каждому проверить
    review_count = 3

# создаем обьекты
    for name in teacher_list:
        teacher = Teacher(name)
        teacher_obj.append(teacher)

# для каждого обьекта назначаем учеников которые он должен проверить
    i = 0
    for name in teacher_list:
        # убираем текущего учителя из списков учеников
        if name in remain_learners:
            remain_learners.remove(name)
        # может получится что оставшихся учеников меньше чем нужно проверить
        if len(remain_learners) < review_count:
            review_count = len(remain_learners)

        # рандомно выбираем из списка учеников review_count шт.
        j = 0
        old_random = []
        while j < review_count:
            # выбираем случайное значение из массива оставшихся учеников
            learner_name = choice(remain_learners)
            # проверяем чтобы не попался тот же ученик что и на предыдущей итерации, если попался то повторяем рандомный выбор
            if learner_name in old_random:
                continue
            # запоминаем кого мы выбрали учеником
            old_random.append(learner_name)
            j = j + 1
            # добавляем в объект учителя его ученика
            teacher_obj[i].learner.append(learner_name)
            # увеличиваем счетчик проверяющих учителей у ученика
            for obj in teacher_obj:
                if obj.name == learner_name:
                    obj.teacher_count = obj.teacher_count + 1
                    # проверяем что количество учителей не превысило допустимый лимит
                    if obj.teacher_count >= review_count:
                        # если привысило то этого ученика больше не нужно выводить в списке учеников
                        remain_learners.remove(obj.name)

        # возвращаем текущего учителя в список учеников для следуйщей итерации где он уже будет учеником
        # но проверяем что у него не должно быть слишком много учителей, иначе не добавляем
        if teacher_obj[i].teacher_count < review_count:
            remain_learners.append(name)
        i = i + 1

    # выводим список учителей и их учеников
    for t in teacher_obj:
        print(t.name + " review " + str(t.learner))
