
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore


class StudentSubjectsScoreAPIView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        # Retrieve data from request payload
        student_first_name = request.data.get("first_name")
        student_last_name = request.data.get("last_name")
        subject_title = request.data.get("subject_title")
        score_value = request.data.get("score")

        # Check if payload data is complete
        if None in [student_first_name, student_last_name, subject_title, score_value]:
            return Response({"error": "Payload data incomplete"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if all fields are of correct data types
        if not all(isinstance(field, str) for field in [student_first_name, student_last_name, subject_title]):
            return Response({"error": "All names and subject title must be strings"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            score = float(score_value)
            if not (0 <= score <= 100):
                raise ValueError("Score must be between 0 and 100")
        except ValueError:
            return Response({"error": "Score must be a number between 0 and 100"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the student exists
        try:
            student = Personnel.objects.get(first_name=student_first_name, last_name=student_last_name)
        except Personnel.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the subject exists
        try:
            subject = Subjects.objects.get(title=subject_title)
        except Subjects.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the credit associated with the subject
        try:
            student_score = StudentSubjectsScore.objects.get(student=student, subjects=subject)
            credit = student_score.credit  # Get the existing credit
        except StudentSubjectsScore.DoesNotExist:
            return Response({"error": "Score entry not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the student's score for this subject already exists
        try:
            student_score = StudentSubjectsScore.objects.get(student=student, subjects=subject)
            # If it exists, update the score
            student_score.score = score
            student_score.save()
            # Return success response with credit
            response_data = {
                "first_name": student_first_name,
                "last_name": student_last_name,
                "subject_title": subject_title,
                "score": score,
                "credit": credit
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except StudentSubjectsScore.DoesNotExist:
            # If it doesn't exist, create a new entry
            StudentSubjectsScore.objects.create(student=student, subjects=subject, score=score, credit=credit)
            # Return success response with credit
            response_data = {
                "first_name": student_first_name,
                "last_name": student_last_name,
                "subject_title": subject_title,
                "score": score,
                "credit": credit
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


class StudentSubjectsScoreDetailsAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        student_id = kwargs.get("id", None)

        try:
            # Retrieve the student details
            student = Personnel.objects.get(id=student_id)
            student_data = {
                "id": student.id,
                "full_name": f"{student.first_name} {student.last_name}",
                "school": student.school_class.school.title
            }

            # Retrieve the scores for the student's subjects
            student_scores = StudentSubjectsScore.objects.filter(student_id=student_id)

            subject_details = []
            total_grade_points = 0
            total_credits = 0

            # Iterate through each score entry
            for score in student_scores:
                # Calculate grade based on score
                if score.score >= 80:
                    grade = 'A'
                elif 75 <= score.score < 80:
                    grade = 'B+'
                elif 70 <= score.score < 75:
                    grade = 'B'
                elif 65 <= score.score < 70:
                    grade = 'C+'
                elif 60 <= score.score < 65:
                    grade = 'C'
                elif 55 <= score.score < 60:
                    grade = 'D+'
                elif 50 <= score.score < 55:
                    grade = 'D'
                else:
                    grade = 'F'

                # Add subject details to the list
                subject_details.append({
                    "subject": score.subjects.title,
                    "credit": score.credit,
                    "score": score.score,
                    "grade": grade
                })

                # Calculate grade points for GPA
                grade_point = StudentSubjectsScoreDetailsAPIView.grade_to_grade_point(grade)
                total_grade_points += score.credit * grade_point
                total_credits += score.credit

            # Calculate GPA
            if total_credits != 0:
                gpa = total_grade_points / total_credits
            else:
                gpa = 0

            # Construct the response data
            response_data = {
                "student": student_data,
                "subject_detail": subject_details,
                "grade_point_average": round(gpa, 2)
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Personnel.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def grade_to_grade_point(grade):
        # Map grades to grade points
        grade_point_mapping = {
            'A': 4.0,
            'B+': 3.5,
            'B': 3.0,
            'C+': 2.5,
            'C': 2.0,
            'D+': 1.5,
            'D': 1.0,
            'F': 0.0
        }
        return grade_point_mapping.get(grade, 0.0)


class PersonnelDetailsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        school_title = kwargs.get("school_title", None)
        if not school_title:
            return Response("School title is required.", status=status.HTTP_400_BAD_REQUEST)

        # Fetching personnel details filtered by the school's title
        personnel_details = Personnel.objects.filter(school_class__school__title__iexact=school_title).order_by(
            'personnel_type', 'school_class__class_order', 'first_name', 'last_name')

        result = []
        for idx, personnel in enumerate(personnel_details, start=1):
            # Capitalizing school title and personnel name
            school_name = school_title.capitalize()
            person_name = f"{personnel.first_name.capitalize()} {personnel.last_name.capitalize()}"
            # Mapping personnel type integer to string
            role_mapping = {
                0: 'Teacher',
                1: 'Head of the room',
                2: 'Student'
            }
            role = role_mapping.get(personnel.personnel_type)

            # Constructing the result pattern
            result_pattern = f"{idx}. school: {school_name}, role: {role}, class: {personnel.school_class.class_order}, name: {person_name}."
            result.append(result_pattern)

        return Response(result, status=status.HTTP_200_OK)


class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):

        # Retrieve all schools
        schools = Schools.objects.all()
        result = []

        # Loop through each school
        for school in schools:
            school_data = {
                "school": school.title,
            }

            classes = Classes.objects.filter(school=school)

            class_data = {}
            # Loop through each class in the school
            for class_obj in classes:
                class_teacher = Personnel.objects.filter(school_class=class_obj, personnel_type=0).first()
                head_of_room = Personnel.objects.filter(school_class=class_obj, personnel_type=1).first()
                students = Personnel.objects.filter(school_class=class_obj, personnel_type=2)

                class_teacher_data = {f"Teacher: {class_teacher.first_name} {class_teacher.last_name}": []} if class_teacher else None
                head_of_room_data = {f"Head of the room": f"{head_of_room.first_name} {head_of_room.last_name}"} if head_of_room else None

                students_data = [{f"Student": f"{student.first_name} {student.last_name}"} for student in students]

                if class_teacher_data:
                    class_teacher_data[f"Teacher: {class_teacher.first_name} {class_teacher.last_name}"].append(head_of_room_data)
                    class_teacher_data[f"Teacher: {class_teacher.first_name} {class_teacher.last_name}"].extend(students_data)

                class_data[f"class {class_obj.class_order}"] = class_teacher_data

            school_data.update(class_data)
            result.append(school_data)

        return Response(result, status=status.HTTP_200_OK)


class SchoolStructureAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):

        # Initialize your_result
        result = []

        # Fetch all root SchoolStructure objects
        root_school_structures = SchoolStructure.objects.filter(parent=None)

        # Iterate over root SchoolStructure objects
        for root_structure in root_school_structures:
            # Create a dictionary to hold the structure data
            root_data = {
                "title": root_structure.title,
                "sub": []
            }
            # Populate sub-structures recursively
            SchoolStructureAPIView.populate_sub_structure(root_structure, root_data["sub"])
            # Append the root data to your_result
            result.append(root_data)

        # Return your_result
        return Response(result, status=status.HTTP_200_OK)

    @staticmethod
    def populate_sub_structure(parent_structure, sub_data):

        # Fetch all child SchoolStructure objects for the given parent_structure
        child_structures = SchoolStructure.objects.filter(parent=parent_structure)
        # Iterate over child SchoolStructure objects
        for child_structure in child_structures:
            # Create a dictionary to hold the child structure data
            child_data = {
                "title": child_structure.title,
                "sub": []  # Add an empty list for subgroups
            }
            # If the child is a classroom, populate its subgroups
            if child_structure.title.startswith("ม."):
                # Fetch all subgroups for the classroom
                subgroups = SchoolStructure.objects.filter(parent=child_structure)
                # Iterate over subgroups and append to the child data
                for subgroup in subgroups:
                    child_data["sub"].append({"title": subgroup.title})
            # Append the child data to sub_data
            sub_data.append(child_data)