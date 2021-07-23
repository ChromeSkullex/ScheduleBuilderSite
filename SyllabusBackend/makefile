PYTHON = py

MAIN = src/main.py
DEBUG = src/scheduleAJAX.py
DEPENDENCIES = src/main.py      \
               src/syllabus.py  \
               src/scheduler.py \
               src/scheduleAJAX.py \
               src/parsepdf.py

syllabus: $(DEPENDENCIES)
	$(PYTHON) $(MAIN) syllabus

schedule: $(DEPENDENCIES)
	$(PYTHON) $(MAIN) schedule

scheduleDebug: $(DEPENDENCIES)
	$(PYTHON) $(DEBUG) scheduleDebug

install:
	pip install bs4
	pip install docxcompose
	pip install pypandoc
	pip install python-docx
	pip install requests

clean:
	rm ./docx/*.docx
