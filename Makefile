all: input.tsv_motor_script.txt README.html
# Prevent make from looking for a file called 'all'
.PHONY : all

input.tsv_motor_script.txt : input.tsv tsv-to-motor.py target_motor_script.txt Te_Li2C2Te.001 Te_Li2C2Te.002 Te_Li2C2Te.003
	python tsv-to-motor.py input.tsv
	diff input.tsv_motor_script.txt target_motor_script.txt > diff.txt
# Diff returns 1 if the files are different, so make throw this error:\
# make: *** [input.tsv_motor_script.txt] Error 1

README.html : README.rst
	rst2html --generator --date --source-link README.rst > README.html

# Keep make from looking for a file called 'clean'
.PHONY: clean
clean:
	rm --force input.tsv_motor_script.txt
	rm --force README.html
