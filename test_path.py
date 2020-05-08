from Path import Path, Flags


def test_path_is_removable_with_normal_flag():
	path = Path("/home/user/images", Flags.NORMAL)
	assert path.is_removable() is True


def test_path_is_not_removable_with_locked_flag():
	path = Path("/home/user/images", Flags.LOCKED)
	assert path.is_removable() is False


def test_add_used_path_to_path_object():
	used_path = "/home/user/images/"
	path = Path("/home/user/images", Flags.NORMAL)
	path.add_used_path(used_path)
	assert path.used_by_paths[0] is used_path


def test_remove_used_path_of_path_object():
	used_path = "/home/user/images/"
	path = Path("/home/user/images", Flags.NORMAL)
	path.add_used_path(used_path)
	assert path.used_by_paths[0] is used_path
	path.remove_used_path(used_path)
	assert len(path.used_by_paths) == 0


def test_add_used_path_twice_dont_duplicate():
	used_path = "/home/user/images/"
	path = Path("/home/user/images", Flags.NORMAL)
	path.add_used_path(used_path)
	path.add_used_path(used_path)
	assert len(path.used_by_paths) == 1


def test_is_not_removable_while_used_path_is_not_zero():
	used_path = "/home/user/images/"
	path = Path("/home/user/images", Flags.NORMAL)
	path.add_used_path(used_path)
	path.add_used_path(used_path)
	assert len(path.used_by_paths) == 1
	assert path.is_removable() is False
	path.remove_used_path(used_path)
	assert path.is_removable() is True
