"""
Run this setup file only once from remote_api to fill your database
"""

from tasks import course_processor

def main():
    course_processor.process_xml('courses_data/fall12.xml')
    course_processor.process_xml('courses_data/spring13.xml')

if __name__ == '__main__':
    main()