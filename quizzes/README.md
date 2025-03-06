## Exam generator for MTH 176

## Generating a template only from the exams_attribute.csv file
1. activate the virtual environment with "source wcc_python_env/bin/activate"

(Note: This environment uses a modified version of the library "latexcompiler" because for some reason,
the original library deletes the main.py file, this README file, and the requirements file. We don't want
this.)

2. run "python3 main.py -g"

This option will generate a template **exam.tex** file, along with template **problem_i.tex** files in the folder midterm/ if
those files don't exist. If some of them do exist, you will be prompted for (y/n) if you want to replace them with
the template problem format.

3. deactivate the environment with "deactivate"

## Modifying the exam
Only modify the files in the "midterm" folder! 

## Generating copies of your exam
1. activate the virtual environment with "source wcc_python_env/bin/activate"

(Note: This environment uses a modified version of the library "latexcompiler" because for some reason,
the original library deletes the main.py file, this README file, and the requirements file. We don't want
this.)

2. run "python3 main.py" following with an argument of either "-s" or "-m" flags, e.g. "python3 main.py -s"

The "-s" or single flag will generate **exam.pdf** in the folder to_be_printed/ from your exams_attribute.csv and
problem files in the folder midterm/.

The "-m" or multiple flag will generate **exam_content_print_x_copies.pdf** and **exam_first_two_pages.pdf** 
in the folder to_be_printed/ from your exams_attribute.csv and problem files in the folder midterm/.

3. deactivate the environment with "deactivate"