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
                id      serial PRIMARY KEY,
                name    character varying(100) UNIQUE NOT NULL,
                gpa     numeric(10, 2),
                birth   timestamp with time zone);
            ''')

            curs.execute('''CREATE TABLE IF NOT EXISTS course (
                id      serial PRIMARY KEY,
                name    character varying(100) NOT NULL);
            ''')

            curs.execute('''CREATE TABLE IF NOT EXISTS student_course (
                id serial PRIMARY KEY,
                student_id integer REFERENCES student(id) ON DELETE CASCADE,
                course_id integer REFERENCES course(id) ON DELETE CASCADE);
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
                try:
                    curs.execute('''INSERT INTO student (name, gpa, birth)
                        VALUES (%(name)s, %(gpa)s, %(birth)s) ON CONFLICT (name) DO NOTHING RETURNING id;
                    ''', student)

                    student_id = curs.fetchone()[0]

                    curs.execute('''INSERT INTO student_course (course_id, student_id)
                        VALUES (%s, %s)
                    ''', (course_id, student_id))
                except psycopg2.Error as err:
                    return 1, err
    return 0, 'Ok'


# просто создает студента
def add_student(conn, student):
    with conn:
        with conn.cursor() as curs:
            try:
                curs.execute('''INSERT INTO student (name, gpa, birth)
                            VALUES (%(name)s, %(gpa)s, %(birth)s)
                            ON CONFLICT (name) DO NOTHING RETURNING id;
                            ''', student)
                return 0, curs.fetchone()[0]
            except psycopg2.Error as err:
                return 1, err


def get_student(student_id):
    pass


def main():
    try:
        conn = psycopg2.connect(dbname='testdb', user='testdb',
                                password='Klevo982', host='localhost')
        # create_db(conn)
        # student = {'name': 'Ипап221', 'gpa': 0, 'birth': '1943-11-05'}
        # result = add_student(conn, student)
        # print(f'ERROR: {result[1]}') if result[0] else print('Запись успешно внесена в БД.')

        # students = [{'name': 'Aавапв вава', 'gpa': 0, 'birth': '1990-02-24'},
        #             {'name': 'Bbb уцуцу', 'gpa': 0, 'birth': '1990-02-24'}]
        # result = add_students(conn, 2, students)
        # print(f'ERROR: {result[1]}') if result[0] else print('Запись успешно внесена в БД.')

        print(get_students(conn, 2))
    finally:
        conn.close()


if __name__ == '__main__':
    import sys

    sys.exit(main())