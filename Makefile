
install: 
	mkdir -p ~/local/bin
	ln -sfn $(PWD)/scripts/dndws ~/local/bin/dndws
	ln -sfn $(PWD)/scripts/fenc ~/local/bin/fenc
	ln -sfn $(PWD)/scripts/fplay ~/local/bin/fplay
	ln -sfn $(PWD)/scripts/fdnd ~/local/bin/fdnd
	ln -sfn $(PWD)/scripts/froland ~/local/bin/froland
	ln -sfn $(PWD)/scripts/fdfil ~/local/bin/fdfil
	ln -sfn $(PWD)/scripts/gtrack ~/local/bin/gtrack
	ln -sfn $(PWD)/scripts/monmake ~/local/bin/monmake
	ln -sfn $(PWD)/scripts/json2fplay ~/local/bin/json2fplay 
	ln -sfn $(PWD)/scripts/fplay2json ~/local/bin/fplay2json
	ln -sfn $(PWD)/scripts/fplay2pdf ~/local/bin/fplay2pdf
	ln -sfn $(PWD)/scripts/spells2pdf ~/local/bin/spells2pdf
	ln -sfn $(PWD)/scripts/fcf ~/local/bin/fcf
	ln -sfn $(PWD)/scripts/fcf2pdf ~/local/bin/fcf2pdf
	ln -sfn $(PWD)/scripts/fdl ~/local/bin/fdl
	rm -f $(PWD)/ddgen.zip
	cd $(PWD)/ddgen && zip -r ../ddgen.zip *
	echo '#!/usr/bin/env python3' | cat - $(PWD)/ddgen.zip > $(HOME)/local/bin/ddgen
	chmod +x ~/local/bin/ddgen
