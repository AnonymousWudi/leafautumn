# coding=utf-8

from django.contrib.auth.models import Permission
from leafautumn.leafautumn.functions import get_object_or_None

PERMISSION_LIST = [
	('Can login dashboard', 10, 'login_dashboard')
]

def main():
	for p in PERMISSION_LIST:
		if get_object_or_None(Permission, name=p[0]):
			continue
		else:
			permission = Permission()
			permission.name            = p[0]
			permission.content_type_id = p[1]
			permission.codename        = p[2]
			permission.save()

if __name__ == '__main__':
	main()