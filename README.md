### About

This is an assessment generator used to generate pdfs of exams, quizzes, and writing assignments for the math courses I teach.

### How to use

1. Activate the virtual environment to run the python files using

	source env/bin/activate
	
Note: You may need to reinstall the virtual environment using Python 3.13 and the requirements.txt file stored in this repo's env directory. To do this, with terminal in this directory, run

	python3 -v 3.13 -m venv env
	source env/bin/activate
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
	source env/bin/deactivate
	
Keep in mind that I have a modified version of env/lib/python3.13/site-packages/latexcompiler/utils/compile_text_files.py, which doesn't throw out essential files like .tex and .git in the repository when I compile the assessment.tex file. You should probably replace that file in your environment with this one.

2. Modify the assessment/attributes.csv file. (There are templates for this located in the sample_attribute_csv_files directory; feel free to use any of these for the attributes file.)

3. Run

	python3 [assessment .py file] -g
	
where the brackets is replaced with any of "exam.py," "quiz.py," or "wa.py." (Make sure the one you use is compatible with the attributes csv file!)

4. Run the same command as above but with the following flags:
	- **-p**: This sets the point values of each problem.
	- **-s**: This compiles a single pdf of your assessment.tex file.
	- **-m**: This compiles multiple pdfs of your assessment.tex file (with the Testing Center values modfied). This only works for exams and quizzes.

5. Make changes to the problem_i.tex files as needed, and do step 4 again. (If you make any changes to the attributes csv file, you'll need to do step 3 again before doing steps 4 and 5.)

##### Last updated: November 14, 2025