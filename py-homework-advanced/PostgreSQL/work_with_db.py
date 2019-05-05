#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# work_with_db.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
# Домашнее задание к лекции 2.3 "Database.PostgreSQL"
#

import psycopg2


# создает таблицы
def create_db(conn):
    with conn:
        with conn.cursor() as curs:
            curs.execute('''CREATE TABLE IF NOT EXISTS student (
                id      serial,
                name    character varying(100),
                gpa     numeric(10, 2),
                birth   timestamp with time zone,
                PRIMARY KEY (id, name));
            ''')

            curs.execute('''CREATE TABLE IF NOT EXISTS course (
                id      serial PRIMARY KEY,
                name    character varying(100) NOT NULL);
            ''')

            curs.execute('''CREATE TABLE IF NOT EXISTS student_course (
                student_id integer REFERENCES student(id) ON DELETE CASCADE,
                course_id integer REFERENCES course(id) ON DELETE CASCADE,
                grade integer,
                PRIMARY KEY (student_id, course_id));
            ''')


# возвращает студентов определенного курса
def get_students(conn, course_id):
    with conn:
        with conn.cursor() as curs:
            try:
                curs.execute('''SELECT c.id, c.name, s.name FROM student_course sc
                            JOIN student s ON s.id = sc.student_id
                            JOIN course c ON c.id = sc.course_id
                            WHERE sc.course_id = %s 
                            ''', (course_id,))
                return 0, curs.fetchall()
            except psycopg2.Error as err:
                return 1, err


def insert_student(cursor, student):
    try:
        cursor.execute('''INSERT INTO student (name, gpa, birth)
            VALUES (%(name)s, %(gpa)s, %(birth)s) ON CONFLICT (name) DO NOTHING RETURNING id;
        ''', student)
        return 0, cursor.fetchone()[0]
    except psycopg2.Error as err:
        return 1, err


# Третья версия создания студента.
def add_student(conn, student):
    with conn:
        with conn.cursor() as curs:
            insert_student(curs, student)


def add_students(conn, course_id, students):
    """
    Создает студентов и записывает их на курс.
    :param conn: коннект к базе данных
    :param course_id: Integer - номер курса
    :param students: Лист словарей параметров студентов.
    :return:
    """
    with conn:
        with conn.cursor() as curs:
            for student in students:
                err, student_id = insert_student(curs, student)
                if err:
                    return 1, student_id
                try:
                    curs.execute('''INSERT INTO student_course (course_id, student_id)
                        VALUES (%s, %s)
                    ''', (course_id, student_id))
                except psycopg2.Error as err:
                    return 1, err
    return 0, 'Ok'


def get_student(conn, student_id):
    with conn:
        with conn.cursor() as curs:
            try:
                curs.execute('''SELECT s.id, s.name, s.birth, s.gpa, c.name FROM student s
                            LEFT JOIN student_course sc ON sc.student_id = s.id
                            LEFT JOIN course c ON c.id = sc.course_id
                            WHERE s.id = %s
                            ''', (student_id,))
                return 0, curs.fetchall()
            except psycopg2.Error as err:
                return 1, err


def main():
    try:
        conn = psycopg2.connect(dbname='testdb', user='testdb',
                                password='Klevo982', host='localhost')
        # Создаём таблицы
        create_db(conn)

        # Добавляем студента
        student = {'name': 'Ипап221', 'gpa': 0, 'birth': '1943-11-05'}
        result = add_student(conn, student)
        print(f'ERROR: {result[1]}') if result[0] else print('Запись успешно внесена в БД.')

        # Добавляем студентов и записываем их на курс №2
        students = [{'name': 'Aавапв вава', 'gpa': 0, 'birth': '1990-02-24'},
                    {'name': 'Bbb уцуцу', 'gpa': 0, 'birth': '1990-02-24'}]
        result = add_students(conn, 2, students)
        print(f'ERROR: {result[1]}') if result[0] else print('Запись успешно внесена в БД.')

        # Получаем студентов определённого курса
        print(get_students(conn, 2)[1])

        # Получаем все сведения о студенте
        print(get_student(conn, 3)[1])
    finally:
        conn.close()


if __name__ == '__main__':
    import sys

    sys.exit(main())
