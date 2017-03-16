install:
	python setup.py install
	cp etc/wazo-admin-ui/conf.d/group.yml /etc/wazo-admin-ui/conf.d
	systemctl restart wazo-admin-ui

uninstall:
	pip uninstall wazo-admin-ui-group
	rm /etc/wazo-admin-ui/conf.d/group.yml
	systemctl restart wazo-admin-ui
