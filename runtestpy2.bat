rd /s /q cover
del .coverage
nosetests-2.7 new_test -s -e \w*.owl --with-coverage --cover-package ./airtest --cover-html --cover-inclusive
pause
start cover/index.html
