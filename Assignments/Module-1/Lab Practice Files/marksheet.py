student_name = input("Enter student name: ")
subject_one_marks = int(input("Enter marks of subject 1: "))
subject_two_marks = int(input("Enter marks of subject 2: "))
subject_three_marks = int(input("Enter marks of subject 3: "))
subject_four_marks = int(input("Enter marks of subject 4: "))
total_marks = 400

if subject_one_marks >= 40 and subject_two_marks >= 40 and subject_three_marks >= 40 and subject_four_marks >= 40:
    #Total marks obtained
    total_marks_obtained = subject_one_marks + subject_two_marks + subject_three_marks + subject_four_marks

    print("Total marks obtained out of 400:", total_marks_obtained)

    #Percentage of the student
    percentage = (total_marks_obtained/total_marks) * 100 #OR if total marks is not declared use total_marks_obtained/4
    print(f"{student_name} got {percentage}%")

    if percentage >=70:
        print(f"{student_name} passed with grade A+")

    elif percentage >= 60:
        print(f"{student_name} passed with Grade A")

    elif percentage >=50:
        print(f"{student_name} passed with Grade B")

    elif percentage >=40:
        print(f"{student_name} passed with Grade C")

else :
    print(f"{student_name} has failed")
